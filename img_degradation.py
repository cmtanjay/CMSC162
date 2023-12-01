import numpy as np
import math
from statistics import *
import tkinter as tk #pip install tk
from tkinter import ttk

from PIL import Image
import random

import variables
from img_ops import *

import matplotlib.pyplot as plt

def salt_and_pepper_noise(self):
    # Function that pops up a window that lets the user input the gamma value    
    def open_popup():
        window = tk.Toplevel()
        window.geometry("400x200+500+300")
        window.title("Salt and Pepper Noise")
        window.resizable(False, False)
        
        window.columnconfigure(0, weight=2)
        window.columnconfigure(1, weight=5)
        
        salt_prob = tk.DoubleVar()
        pepper_prob = tk.DoubleVar()

        # Detects the value inside the text box
        def entry_changed(event):
            salt_value = salt_text_box.get()  # Get the value from the entry box
            pepper_value = pepper_text_box.get()
            if (float(salt_value) >= 0 and float(salt_value) <= 1) and (float(pepper_value) >= 0 and float(pepper_value) <= 1) and (float(salt_value) + float(pepper_value) >= 0 and float(salt_value) + float(pepper_value) <= 1): 
                salt_prob.set(float(salt_value))  # Set the slider value to the entry value
            else:
                err_window = tk.Toplevel()
                err_window.geometry("400x130+500+300")
                err_window.title("Salt and Pepper Noise")
                err_window.resizable(False, False)
                ttk.Label(err_window, text='Both probabilities must be within and equate in range 0-1', font=('Arial 8 bold')).place(x=50, y=35)
                btn_ok = tk.Button(err_window, command=err_window.destroy, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
                btn_ok.place(x=80, y=85)

        # Function that executes when OK button is clicked
        def on_click():
            window.destroy()

        # current value label
        ttk.Label(window, text='Input Salt Noise Probability:', font=('Arial 10 bold')).place(x=150, y=35)
        
        salt_text_box = tk.Entry(window, bg="white", textvariable=salt_prob, width=5, font=('Arial 13'))
        salt_text_box.place(x=160, y=55)
        salt_text_box.bind("<KeyRelease>", entry_changed)
        
        # current value label
        ttk.Label(window, text='Input Pepper Noise Probability:', font=('Arial 10 bold')).place(x=150, y=105)
        
        pepper_text_box = tk.Entry(window, bg="white", textvariable=pepper_prob, width=5, font=('Arial 13'))
        pepper_text_box.place(x=160, y=125)
        pepper_text_box.bind("<KeyRelease>", entry_changed)
        
        btn = tk.Button(window, command=on_click, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn.place(x=165, y=155)
        
        window.wait_window(window)  # Wait for the window to be destroyed
        
        return salt_prob.get(), pepper_prob.get()
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded Damn")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        Ps, Pp = open_popup()
        Psp = 1 - (Ps + Pp)    
        
        gray = get_grayscale_img(self) # transforms image to grayscale
        flat_gray_orig = [element for row in gray for element in row]
        
        # Create a blank image with a white background
        img_SP = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_SP = ImageDraw.Draw(img_SP)
        
        deg_img = []
        row = []
        
        # Salt and pepper process
        for i, color in enumerate(flat_gray_orig):
            random = np.random.random()
            
            if random < Pp:
                row.append(0)
            elif random > (1-Ps):
                row.append((2**variables.bits_per_pixel)-1)
            else:
                row.append(color)
                
            if len(row) == variables.img_width:
                deg_img.append(row)
                row = []
        
        drawImage(self, draw_SP, deg_img)
        show_image(self, img_SP, " ")
        variables.curr_img = img_SP
        variables.curr_image_data = deg_img
        variables.pcx_image_data = deg_img
        variables.degraded_image_data = deg_img
        variables.isDegraded = True

        # Call show histogram function after applying salt and pepper noise
        show_histogram(variables.degraded_image_data, 'Salt and Pepper Noise Histogram')
    
# Function for applying Gaussian noise to an image
def gaussian_noise(self):
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        gray = get_grayscale_img(self)  # transforms image to grayscale
        flat_gray_orig = [element for row in gray for element in row]

        avg = mean(flat_gray_orig)
        sigma = pstdev(flat_gray_orig)

        # Create a blank image with a white background
        img_Gaussian = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_Gaussian = ImageDraw.Draw(img_Gaussian)

        corrupted_img = []

        # Apply Gaussian noise to each pixel
        for x in range(variables.img_height):
            row = []
            for y in range(variables.img_width):
                pixel_value = gray[x][y]
                noise = int(np.random.randn() * sigma)
                noisy_value = max(0, min(255, pixel_value + noise))
                row.append(noisy_value)
            corrupted_img.append(row)

        print(corrupted_img)

        # Draw the corrupted image
        drawImage(self, draw_Gaussian, corrupted_img)
        show_image(self, img_Gaussian, "Corrupted Image")

        variables.curr_img = img_Gaussian
        variables.curr_image_data = corrupted_img
        variables.isDegraded = True
        variables.degraded_image_data = corrupted_img

        # Call show histogram function after applying Gaussian noise
        show_histogram(variables.degraded_image_data, 'Gaussian Noise Histogram')

def rayleigh_noise(self):
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        gray = get_grayscale_img(self)  # transforms image to grayscale
        flat_gray_orig = [element for row in gray for element in row]

        # Set the scale parameter/ sigma for the Rayleigh distribution
        scale_param = 20.0

        # Create a blank image with a white background
        img_Rayleigh = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_Rayleigh = ImageDraw.Draw(img_Rayleigh)

        corrupted_img = []

        # Apply Rayleigh noise to each pixel
        for x in range(variables.img_height):
            row = []
            for y in range(variables.img_width):
                pixel_value = gray[x][y]
                
                # Using the random module to generate Rayleigh-distributed noise
                noise = int(np.random.rayleigh(scale=scale_param))
                
                noisy_value = max(0, min(255, pixel_value + noise))
                row.append(noisy_value)
            corrupted_img.append(row)

        # Draw the corrupted image
        drawImage(self, draw_Rayleigh, corrupted_img)
        show_image(self, img_Rayleigh, "Corrupted Image")

        variables.curr_img = img_Rayleigh
        variables.curr_image_data = corrupted_img
        variables.isDegraded = True
        variables.degraded_image_data = corrupted_img
        # Call histogram function
        show_histogram(variables.degraded_image_data, 'Rayleigh Noise Histogram')

# Function for showing histogram for Image degradation
def show_histogram(image_data, title):
    flat_image_data = [element for row in image_data for element in row]

    plt.hist(flat_image_data, bins=256, range=(0, 256), density=True, color='gray', alpha=0.75)
    plt.title(title)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

