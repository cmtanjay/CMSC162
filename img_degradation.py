import numpy as np
import math
from statistics import *

from PIL import Image
import random

import variables
from img_ops import *

def salt_and_pepper_noise(self):
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        Ps = 0.02
        Pp = 0.03
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
        variables.isDegraded = True
    
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

        deg_img = []
        corrupted_img = []

        # # Ensure flat_gray_orig is a NumPy array
        # flat_gray_orig = np.array(flat_gray_orig)

        # Apply Gaussian noise to the image
        # corrupted_img = flat_gray_orig + noise

        # Apply Gaussian noise to each pixel
        for x in range(variables.img_height):
            row = []
            for y in range(variables.img_width):
                pixel_value = gray[x][y]
                noise = int(random.gauss(avg, sigma))
                noisy_value = max(0, min(255, pixel_value + noise))
                row.append(noisy_value)
                # img_Gaussian.putpixel((x, y), noisy_value)
            corrupted_img.append(row)
       

        print(corrupted_img)

        # Draw the corrupted image
        drawImage(self, draw_Gaussian, corrupted_img)
        show_image(self, img_Gaussian, "Corrupted Image")

        variables.curr_img = img_Gaussian
        variables.curr_image_data = deg_img
        variables.isDegraded = True