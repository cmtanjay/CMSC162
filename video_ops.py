import time
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

import cv2

from img_ops import *
from variables import *

def open_vid_file(self):
    variables.video_filepath = askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
    variables.orig_video_filepath = variables.video_filepath
    
    if variables.video_filepath:
        variables.file_type = 3
        
        self.pause_button = tk.Button(self.rightsidebar, text="Play", command=lambda: play_video(self))
        self.pause_button.grid(row=0, column=0, pady=5,  padx=10, sticky="ew")
        
        self.stop_button = tk.Button(self.rightsidebar, text="Stop", command=lambda: stop_video(self), state="disabled")
        self.stop_button.grid(row=0, column=1, pady=5,  padx=10, sticky="ew")

        self.restart_button = tk.Button(self.rightsidebar, text="Restart", command=lambda: res_video(self), state="disabled")
        self.restart_button.grid(row=1, column=0, padx=10, sticky="ew")

        self.close_button = tk.Button(self.rightsidebar, text="Close", command=lambda: close_video(self))
        self.close_button.grid(row=1, column=1, padx=10, sticky="ew")
        
        self.cap = cv2.VideoCapture(variables.video_filepath)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.elapsed_time = 0
        self.start_time = time.time()
        self.paused = False
        
        self.current_frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        
        self.success, self.frame = self.cap.read()
        
        img_tk = get_thumbnail(self)
        # Update label with the new frame
        self.image_label.img = img_tk
        self.image_label.config(image=img_tk)
    
def play_video(self):
    self.pause_button.config(text="Pause", command=lambda: pause_video(self))
    self.restart_button.config(state="normal")
    self.stop_button.config(state="normal")
    
    self.cap = cv2.VideoCapture(variables.video_filepath)
    self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
    self.elapsed_time = 0
    self.start_time = time.time()
    self.paused = False
    
    self.current_frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
    
    self.success, self.frame = self.cap.read()
    
    img_tk = get_thumbnail(self)
    # Update label with the new frame
    self.image_label.img = img_tk
    self.image_label.config(image=img_tk)
    
    if self.success:
        update_video(self)  
    else:
        self.cap.release()

def update_video(self):
    self.success, frame = self.cap.read()
    if not self.paused:
        # Convert frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert frame to PhotoImage
        img = Image.fromarray(frame_rgb)
        
        frame = get_frame(self, img)
        
        img_tk = ImageTk.PhotoImage(frame)
        # Update label with the new frame
        self.image_label.img = img_tk
        self.image_label.config(image=img_tk)

        current_time = time.time() - self.start_time
        self.elapsed_time = int(current_time)
        total_time = self.total_frames // self.fps

        print(f"Elapsed Time: {self.elapsed_time} seconds / Total Time: {total_time} seconds", end='\r')
        

        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.total_frames - 1:
            # Video has reached the end, restart it
            restart_video(self)
        else:
            self.after(25, lambda: update_video(self))  # Update every 25 milliseconds

def get_frame(self, frame):
    # Opens the image using PIL
    label_width = self.image_label.winfo_width()
    label_height = self.image_label.winfo_height()
    
    # Define the padding size
    padding_x = 20  # Horizontal padding
    padding_y = 50  # Vertical padding

    # Calculate the available space for the image within the label
    available_width = label_width - (2 * padding_x)
    available_height = label_height - (2 * padding_y)
    
    resized_frame = img_resize_aspectRatio(self, frame, available_width, available_height)
    
    return resized_frame

def get_thumbnail(self):
    # Convert frame to RGB format
    frame1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    
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
    
    image = img_resize_aspectRatio(self, img, available_width, available_height)
    
    img_tk = ImageTk.PhotoImage(image)
    
    return img_tk

def pause_video(self):
    self.paused = not self.paused
    if self.paused:
        print("0")
        self.current_frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.pause_button.config(text="Resume", command=lambda: pause_video(self))
        self.stop_button.config(state="disabled")
    else:
        print("1")
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_index)
        self.pause_button.config(text="Pause", command=lambda: pause_video(self))
        self.stop_button.config(state="normal")

def restart_video(self):
    if self.cap:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.current_frame_index = 0  # Update the current frame index
        self.start_time = time.time()
        img_tk = get_thumbnail(self)
        self.image_label.img = img_tk
        self.image_label.config(image=img_tk)
        update_video(self)
        
def res_video(self):
    if self.cap:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
def stop_video(self):
    if self.cap:
        self.cap.release()
        self.pause_button.config(text="Play", command=lambda: play_video(self))
        self.restart_button.config(state="disabled")
        self.stop_button.config(state="disabled")

def close_video(self):
    if self.cap:
        self.cap.release()
        # Removes image in the image panel
        self.image_label.destroy()
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=2, sticky="nsew")
        
        # Reverts right sidebar to its original form
        self.rightsidebar.destroy()
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=3, sticky="nsew")
        self.rightsidebar.grid_columnconfigure(0, minsize=125)
        self.rightsidebar.grid_columnconfigure(1, minsize=125)