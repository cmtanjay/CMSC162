# This is where the image compression processes are implemented.
import variables
from PIL import Image, ImageDraw
from img_ops import *
from huffman import *

import tkinter as tk
import numpy as np

# Function that executes the run length encoding by getting the pixel value and its frequency
# 192 is added to pixel count in order for the user to use the run length decode function in img_ops
def run_length_encode(data):
    encoded_data = []
    current_value = data[0]
    count = 1

    for value in data[1:]:
        if value == current_value:
            count += 1
        else:
            encoded_data.append(count+192)
            encoded_data.append(current_value)
            count = 1
            current_value = value

    return encoded_data, len(data), len(encoded_data),

# Function that starts the Run-Length Encoding process
def run_length_coding(self):
    if variables.file_type == 1:
        encoded_data, original_img_size, compress_img_size = run_length_encode(variables.image_data)

        # Decode and display the compressed image
        decoded_data = decode(self, encoded_data)
        decoded_img = Image.new('RGB', (variables.img_width, variables.img_height))
        draw = ImageDraw.Draw(decoded_img)
        drawImage1DArray(self,decoded_data, draw, variables.palette)
        show_image(self, decoded_img, " ")
        
        # Shows the previous and resulting image size after compression and the compression rate
        open_popup(original_img_size, compress_img_size)

# Function that starts the Huffman coding process
def huffman_coding(self):
    if variables.file_type == 1:
        output_compressed_path = 'huffman_compressed_image.bmp'

        # Compress image
        huffman_tree, original_img_size, compress_img_size = compress_image(self, output_compressed_path)
        print(f"orig: {original_img_size}, comp: {compress_img_size}")

        # Decompress image
        decompress_image(self, output_compressed_path, huffman_tree)
        
        open_popup(original_img_size, compress_img_size)
        
        self.btn_hist.config(state="disabled")
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Image compressed through Huffman coding.", x=330, y=20, fill="white", font=("Arial", 9,))
        
    elif variables.file_type == 2:
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Image compression not allowed for image sequence.", x=330, y=20, fill="white", font=("Arial", 9,))
    else:
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Image compression not allowed for video.", x=330, y=20, fill="white", font=("Arial", 9,))
    
# Function that pops up a window that lets the user see the previous and resulting image size and its compression rate   
def open_popup(orig_size, compress_size):
    window = tk.Toplevel()
    window.geometry("400x130+500+300")
    window.title("Successful Image Compression!")
    window.resizable(False, False)
    tk.Label(window, text= f"Original Image Size: {orig_size} bytes", font=('Arial 13')).place(x=20,y=30)
    tk.Label(window, text= f"Compressed Image Size: {compress_size} bytes", font=('Arial 13')).place(x=20,y=50)
    tk.Label(window, text= f"Compression Ratio: {orig_size/compress_size} bytes", font=('Arial 13')).place(x=20,y=70)