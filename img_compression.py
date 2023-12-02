import variables
from PIL import Image, ImageDraw
from img_ops import *
from huffman import *

import tkinter as tk
import numpy as np

def run_length_coding(self):
    print("Run length skrt skrt")

    # Convert to list if it's a NumPy array
    data = np.array(variables.image_data).flatten().tolist()

    encoded_data = []
    current_value = data[0]
    count = 1

    compressed_img = Image.new('L', (variables.img_width, variables.img_height), 255)
    draw_compressed_img = ImageDraw.Draw(compressed_img)

    for value in data[1:]:
        if value == current_value:
            count += 1
        else:
            encoded_data.append((count, current_value))
            count = 1
            current_value = value

    encoded_data.append((count, current_value))

    # Save the compressed image
    drawImage(self, draw_compressed_img, encoded_data)  # Replace self with the actual reference to your class or instance
    compressed_img.save("compressed_image.bmp")  # Save the compressed image

    # Decode and display the compressed image
    decoded_img = decode_run_length_compression(encoded_data)
    decoded_img.show()

    return encoded_data

def decode_run_length_compression(compressed_data):
    print(compressed_data)
    decoded_data = []

    for i in range(0, len(compressed_data), 2):
        run_length = compressed_data[i]
        color = compressed_data[i + 1]

        # Extend the decoded data with the run of the specified color
        decoded_data.extend([color] * run_length)

    # Create a new image using the decoded data
    decoded_img = Image.new('RGB', (variables.img_width, variables.img_height))
    draw = ImageDraw.Draw(decoded_img)
    drawImage(None, draw, decoded_data)  # Assume drawImage is a function for drawing image data

    return decoded_img
    
def get_color_code(color):
    # Placeholder function to convert color information to a code
    # Customize this based on your specific color coding scheme

    color_codes = {
        (255, 255, 255): 'W',  # White
        (255, 0, 0): 'R',      # Red
        (0, 0, 255): 'B',      # Blue
        (255, 255, 0): 'Y',    # Yellow
        (0, 0, 0): 'K',        # Black
        # Add more color mappings as needed
    }

    # Check if the exact color is in the dictionary
    if color in color_codes:
        return color_codes[color]

    # If the color is not in the dictionary, you may choose a default code or handle it differently
    return 'U'  # 'U' for Unknown or Unmapped color


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
    
    self.btn_hist.config(state="disabled")