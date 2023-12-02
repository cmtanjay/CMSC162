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
            encoded_data.append((count, current_value))
            count = 1
            current_value = value

    encoded_data.append((count, current_value))

    return encoded_data

def run_length_decode_all(encoded_data):
    decoded_data = []
    
    for count, value in encoded_data:
        decoded_data.extend([value] * count)

    return decoded_data

def run_length_coding(self):
    print("Run length skrt skrt")

    # Convert to list if it's a NumPy array
    data = np.array(variables.image_data).flatten().tolist()

    encoded_data = run_length_encode(data)

    compressed_img = Image.new('L', (variables.img_width, variables.img_height), 255)
    draw_compressed_img = ImageDraw.Draw(compressed_img)

    for count, value in encoded_data:
        draw_compressed_img.point((count, value), fill=0)  # Modify based on your drawImage function

    compressed_img.save("compressed_image.bmp")

    # Decode and display the compressed image
    decoded_data = run_length_decode_all(encoded_data)
    decoded_img = Image.new('RGB', (variables.img_width, variables.img_height))
    draw = ImageDraw.Draw(decoded_img)
    drawImage(None, draw, decoded_data)  # Assume drawImage is a function for drawing image data
    decoded_img.show()

    return encoded_data


def huffman_coding(self):
    # Function that pops up a window that lets the user input the gamma value    
    def open_popup(orig_size, compress_size):
        window = tk.Toplevel()
        window.geometry("400x130+500+300")
        window.title("Successful Image Compression!")
        window.resizable(False, False)
        tk.Label(window, text= f"Original Image Size: {orig_size} bytes", font=('Arial 13')).place(x=20,y=30)
        tk.Label(window, text= f"Compressed Image Size: {compress_size} bytes", font=('Arial 13')).place(x=20,y=50)
        tk.Label(window, text= f"Compression Ratio: {orig_size/compress_size} bytes", font=('Arial 13')).place(x=20,y=70)
        
    output_compressed_path = 'huffman_compressed_image.bmp'

    # Compress image
    huffman_tree, original_img_size, compress_img_size = compress_image(self, output_compressed_path)
    print(f"orig: {original_img_size}, comp: {compress_img_size}")

    # Decompress image
    decompress_image(self, output_compressed_path, huffman_tree)
    
    open_popup(original_img_size, compress_img_size)