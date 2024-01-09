import variables
import cv2
import numpy as np
from tkinter import filedialog as ff

# Use glob to get a list of image files in a directory
import glob
import re

from img_seq_ops import *

def dense_optical(self):
    if variables.file_type == 2:
        variables.is_filtered = True
        variables.img_seq = []
        
        # Create a VideoWriter object for output video
        height, width, _ = cv2.imread(variables.image_paths[0]).shape
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        output_video = cv2.VideoWriter("output.avi", fourcc, 10, (width, height))

        # Read the first frame
        frame1 = cv2.imread(variables.image_paths[0])
        prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frame1)
        hsv[..., 1] = 255
        
        processed_frames = []  # Collect processed frames
        
        for image_path in variables.image_paths[1:]:
            frame2 = cv2.imread(image_path)
            next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            # Calculate optical flow
            flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            # Compute magnitude and angle of 2D vectors
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

            # Set image hue according to the optical flow direction
            hsv[..., 0] = ang * 180 / np.pi / 2

            # Set image value according to the optical flow magnitude (normalized)
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

            # Convert HSV to BGR color representation
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
            image = Image.fromarray(cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB))
            # Overlay the RGB image onto the optical flow visualization
            # result = cv2.addWeighted(rgb, 0.5, frame2, 0.5, 0)

            print(image)

            # Collect processed frame
            variables.img_seq.append(image)

            # Write the frame to the output video
            output_video.write(rgb)

            # Check for 'q' key to set exit_flag
            key = cv2.waitKeyEx(1)
            if key == ord('q') or key == 27:  # 'q' key or Esc key
                exit_flag = True
                break

            prvs = next
            
        # Pass the entire sequence of processed frames to show_frame
        show_image(self, variables.img_seq[0], " ")
            
    elif variables.file_type == 3:
        variables.video_filepath = variables.orig_video_filepath
        video = cv2.VideoCapture(variables.video_filepath) 
        
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        variables.img_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        variables.img_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Use the current working directory as the output directory
        output_directory = os.getcwd()

        # Join the directory and file name to get the full file path
        output_video_filepath = os.path.join(output_directory, "video_output.avi")
        
        output_video = cv2.VideoWriter(output_video_filepath, fourcc, int(video.get(cv2.CAP_PROP_FPS)), (variables.img_width, variables.img_height))
        
        # Create a progress bar window
        self.progress_window = tk.Toplevel(self)
        self.progress_window.title("Progress")

        # Create a progress bar in the progress window
        progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
        progress_bar.pack(pady=10)
        
        value = 0
        num = 0
        self.progress_var.set(value)
        self.progress_window.update()
        
        current_frame = 0
        thumbnail = None
        
        # Read the first frame
        status, frame1 = video.read()
        prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frame1)
        hsv[..., 1] = 255

        exit_flag = False
        
        while not exit_flag:
            status, frame2 = video.read() 
            
            if not status:
                break
            
            next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            # Calculate optical flow
            flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            # Compute magnitude and angle of 2D vectors
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

            # Set image hue according to the optical flow direction
            hsv[..., 0] = ang * 180 / np.pi / 2

            # Set image value according to the optical flow magnitude (normalized)
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

            # Convert HSV to BGR color representation
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            
            # Write the frame to the output video
            output_video.write(rgb)
            
            if current_frame == 0:
                # Convert frame to RGB format
                frame1 = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
                
                # Convert frame to PhotoImage
                img = Image.fromarray(frame1)
                
                # Opens the image using PIL
                label_width = self.image_label.winfo_width()
                label_height = self.image_label.winfo_height()
                
                # Define the padding size
                padding_x = 20  # Horizontal padding
                padding_y = 50  # Vertical padding

                # Calculate the available space for the image within the label
                available_width = label_width - (2 * padding_x)
                available_height = label_height - (2 * padding_y)
                
                thumbnail = img_resize_aspectRatio(self, img, available_width, available_height)
                
            value += (1/total_frames)*100
            self.progress_var.set(value)
            self.progress_window.update()
            
            num += 1
                
            current_frame += 1
            
            prvs = next
        
        self.progress_window.destroy()
        
        img_tk = ImageTk.PhotoImage(thumbnail)
        # Update label with the new frame
        self.image_label.img = img_tk
        self.image_label.config(image=img_tk)
        variables.video_filepath = output_video_filepath