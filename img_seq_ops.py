import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from glob import glob
import re
import keyboard

from img_ops import *
from progressBar import *
from variables import *

def open_zip_file(self):
    directory = filedialog.askdirectory()
    
    if directory:
        variables.file_type = 2
        
        images = os.listdir(directory)
        images.sort(key=natural_sort_key)
        variables.image_paths = [os.path.join(directory, item) for item in images]
        
        # Extract the folder name from the first image path (assuming all images are in the same folder)
        folder_name = os.path.basename(os.path.dirname(variables.image_paths[0]))
        
        self.add_text_to_statusbar(f"Status: Folder {folder_name} is loaded", x=200, y=20, fill="white", font=("Arial", 9,))
        
        self.paused = True
        self.current_frame = 0
        variables.is_filtered = False
        
        show_frame(self)
        
        # show_image(self, variables.img_sequence[self.current_frame], " ")
        
        self.prev_btn = tk.Button(self.rightsidebar, text="Show Previous Frame", command=lambda: prev_frame(self), state="disabled")
        self.prev_btn.grid(row=0, column=0, pady=5,  padx=10, sticky="ew")
        
        self.next_btn = tk.Button(self.rightsidebar, text="Show Next Frame", command=lambda: next_frame(self))
        self.next_btn.grid(row=0, column=1, pady=5,  padx=10, sticky="ew")

        self.play_imgs_button = tk.Button(self.rightsidebar, text="Play Image Sequence", command=lambda: toggle(self))
        self.play_imgs_button.grid(row=1, column=0, padx=10, sticky="ew")

        # self.reverse_button = tk.Button(self.rightsidebar, text="Play in Reverse", command=lambda: reverse_imgs(self))
        # self.reverse_button.grid(row=1, column=1, padx=10, sticky="ew")
        
        self.reset_button = tk.Button(self.rightsidebar, text="Reset", command=lambda: reset(self))
        self.reset_button.grid(row=1, column=1, padx=10, sticky="ew")

def show_frame(self):
    image_path = variables.image_paths[self.current_frame]
    img = Image.open(image_path)
    
    # Opens the image using PIL
    label_width = self.image_label.winfo_width()
    label_height = self.image_label.winfo_height()
    
    # Define the padding size
    padding_x = 20  # Horizontal padding
    padding_y = 20  # Vertical padding

    # Calculate the available space for the image within the label
    available_width = label_width - (2 * padding_x)
    available_height = label_height - (2 * padding_y)
    
    image = img_resize_aspectRatio(self, img, available_width, available_height)
    
    img_tk = ImageTk.PhotoImage(image)
    self.image_label.img = img_tk
    self.image_label.config(image=img_tk)
    
def next_frame(self):
    if self.current_frame == len(variables.image_paths)-2:
        self.next_btn.config(state="disabled")
        self.prev_btn.config(state="normal")
    else:
        self.next_btn.config(state="normal")
        self.prev_btn.config(state="normal")
    
    self.current_frame += 1
    
    if not variables.is_filtered:
        show_frame(self)
    else:
        show_image(self, variables.img_seq[self.current_frame], " ")
    
def prev_frame(self):
    if self.current_frame == 1:
        self.prev_btn.config(state="disabled")
        self.next_btn.config(state="normal")
    else:
        self.prev_btn.config(state="normal")
        self.next_btn.config(state="normal")
        
    self.current_frame -= 1
    
    if not variables.is_filtered:
        show_frame(self)
    else:
        show_image(self, variables.img_seq[self.current_frame], " ")

def toggle(self):
    if self.paused:
        self.paused = not self.paused
        self.play_imgs_button.config(text="Pause")
        self.prev_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        play_imgs(self)
    else:
        self.paused = not self.paused
        
        if self.current_frame == 0 or self.current_frame == len(variables.image_paths)-1:
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="normal")
        else:
            self.prev_btn.config(state="normal")
            self.next_btn.config(state="normal")
        
        self.play_imgs_button.config(text="Play Image Sequence")
    
def play_imgs(self):   
    if not self.paused and self.current_frame < len(variables.image_paths)-1:
        if not variables.is_filtered:
            show_frame(self)
        else:
            show_image(self, variables.img_seq[self.current_frame], " ")
            
        self.current_frame += 1
        self.after(50, lambda: play_imgs(self))  # Delay of 3000 milliseconds (3 seconds)
    elif self.current_frame == len(variables.image_paths)-1:
        self.current_frame = 0
        
        if not variables.is_filtered:
            show_frame(self)
        else:
            show_image(self, variables.img_seq[self.current_frame], " ")
   
        if not self.paused:
            self.after(50, lambda: play_imgs(self))

def reset(self):
    self.current_frame = 0
    self.prev_btn.config(state="disabled")
    self.next_btn.config(state="normal")
    
    if not variables.is_filtered:
        show_frame(self)
    else:
        show_image(self, variables.img_seq[self.current_frame], " ")

def reverse_imgs(self):
    # self.current_frame = len(variables.image_paths)
    if self.current_frame > 0:
        if not variables.is_filtered:
            show_frame(self)
        else:
            show_image(self, variables.img_seq[self.current_frame], " ")
            
        self.current_frame -= 1
        self.after(50, lambda: reverse_imgs(self))  # Delay of 3000 milliseconds (3 seconds)
    elif self.current_frame == 0:
        self.current_frame = len(variables.image_paths)-1
        
        if not variables.is_filtered:
            show_frame(self)
        else:
            show_image(self, variables.img_seq[self.current_frame], " ")
        
        self.after(50, lambda: reverse_imgs(self))