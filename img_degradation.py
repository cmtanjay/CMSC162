import numpy as np
import math

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
        
        for i, color in enumerate(flat_gray_orig):
            random = np.random.random()
            
            if random < Pp:
                deg_img.append(0)
            elif random > (1-Ps):
                deg_img.append((2**variables.bits_per_pixel)-1)
            else:
                deg_img.append(color)
        
        drawImage1DArray(self, deg_img, draw_SP, [])
        show_image(self, img_SP, " ")
        variables.curr_img = img_SP
    