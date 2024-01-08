import variables
import cv2
import numpy as np
from tkinter import filedialog as ff

# Use glob to get a list of image files in a directory
import glob
import re

from img_seq_ops import *

def dense_optical(self):
    print("dense")
    
    if variables.file_type == 2:
        print("dense image sequence")
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
            
    elif variables.file_type == 3:
        print("dense video")
        variables.is_filtered = True

        # Use the current working directory as the output directory
        output_directory = os.getcwd()

        # Join the directory and file name to get the full file path
        output_video_filepath = os.path.join(output_directory, "output_video.avi")

        # Create a VideoWriter object for the output video
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        output_video = cv2.VideoWriter(output_video_filepath, fourcc, 10, (variables.img_width, variables.img_height))

        # The video feed is read in as a VideoCapture object
        cap = cv2.VideoCapture(variables.video_filepath)

        # ret = a boolean return value from getting the frame, first_frame = the first frame in the entire video sequence
        ret, first_frame = cap.read()
        # Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
        prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        # Creates an image filled with zero intensities with the same dimensions as the frame
        mask = np.zeros_like(first_frame)
        # Sets image saturation to maximum
        mask[..., 1] = 255

        while cap.isOpened():
            # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
            ret, frame = cap.read()
            if not ret:
                break

            # Converts each frame to grayscale - we previously only converted the first frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Calculates dense optical flow by Farneback method
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            # Computes the magnitude and angle of the 2D vectors
            magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            # Sets image hue according to the optical flow direction
            mask[..., 0] = angle * 180 / np.pi / 2
            # Sets image value according to the optical flow magnitude (normalized)
            mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
            # Converts HSV to RGB (BGR) color representation
            rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

        
            cv2.imshow("dense optical flow", rgb)
            video = cv2.VideoCapture(rgb) 

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            variables.img_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            variables.img_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        

            # Write the frame to the output video
            output_video.write(rgb)

            # Updates previous frame
            prev_gray = gray

            # Frames are read by intervals of 1 millisecond. The program breaks out of the while loop when the user presses the 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # The following frees up resources and closes all windows
        cap.release()
        cv2.destroyAllWindows()



    output_video.release()

    # Pass the entire sequence of processed frames to show_frame
    show_image(self, variables.img_seq[0], " ")
    
def sparse_optical(self):
    print("sparse")