import variables
from PIL import Image, ImageDraw
from img_ops import *
from huffman import *

import tkinter as tk
import numpy as np

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

    return encoded_data, len(data)*3, len(encoded_data),

def run_length_coding(self):
    print("Run length skrt skrt")

    encoded_data, original_img_size, compress_img_size = run_length_encode(variables.image_data)
    # print(encoded_data)

    print(len(encoded_data))

    # # Convert binary string to bytes
    # encoded_bytes = bytearray()
    # for i in range(0, len(encoded_data), 8):
    #     byte = encoded_data[i:i+8]
    #     encoded_bytes.append(int(byte, 2))

    # # Save compressed data to a binary file
    # with open('RLE_image.bin', 'wb') as compressed_file:
    #     compressed_file.write(bytes(encoded_bytes))

    # Decode and display the compressed image
    decoded_data = decode(self, encoded_data)
    decoded_img = Image.new('RGB', (variables.img_width, variables.img_height))
    draw = ImageDraw.Draw(decoded_img)
    drawImage1DArray(self,decoded_data, draw, variables.palette)
    show_image(self, decoded_img, " ")
    
    open_popup(original_img_size, compress_img_size)

def huffman_coding(self):
        
    output_compressed_path = 'huffman_compressed_image.bmp'

    # Compress image
    huffman_tree, original_img_size, compress_img_size = compress_image(self, output_compressed_path)
    print(f"orig: {original_img_size}, comp: {compress_img_size}")

    # Decompress image
    decompress_image(self, output_compressed_path, huffman_tree)
    
    open_popup(original_img_size, compress_img_size)
    
    self.btn_hist.config(state="disabled")
    
# Function that pops up a window that lets the user input the gamma value    
def open_popup(orig_size, compress_size):
    window = tk.Toplevel()
    window.geometry("400x130+500+300")
    window.title("Successful Image Compression!")
    window.resizable(False, False)
    tk.Label(window, text= f"Original Image Size: {orig_size} bytes", font=('Arial 13')).place(x=20,y=30)
    tk.Label(window, text= f"Compressed Image Size: {compress_size} bytes", font=('Arial 13')).place(x=20,y=50)
    tk.Label(window, text= f"Compression Ratio: {orig_size/compress_size} bytes", font=('Arial 13')).place(x=20,y=70)