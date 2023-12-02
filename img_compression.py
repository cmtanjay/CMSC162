import variables
from PIL import Image, ImageDraw
from img_ops import *
from huffman import *

import tkinter as tk
import numpy as np

def run_length_coding(self, save_path="compressed_image.bmp"):
    print("RLE ni wiiiieee")
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
        return

    data = variables.image_data
    compressed_data = []

    for row in data:
        run_length = 1
        current_color = row[0]

        for j in range(1, len(row)):
            if row[j] == current_color:
                run_length += 1
            else:
                compressed_data.extend([run_length, current_color])
                run_length = 1
                current_color = row[j]

        # Append the last run for the current row
        compressed_data.extend([run_length, current_color])

    # Save the compressed data to a file
    with open(save_path, 'wb') as file:
        for item in compressed_data:
            file.write(bytes([item]))

    # Display the compressed image
    compressed_img = decode_run_length_compression(compressed_data)
    show_image(self, compressed_img, "Compressed Image")

    # Updates status
    self.statusbar.destroy()
    self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
    self.statusbar.grid(row=2, columnspan=3, sticky="ew")
    self.create_statusbar_canvas()
    self.add_text_to_statusbar(f"Status: Compressed image saved to {save_path}", x=220, y=20, fill="white",
                               font=("Arial", 9,))

def decode_run_length_compression(compressed_data):
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