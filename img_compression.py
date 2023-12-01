import variables
from PIL import Image, ImageDraw
from img_ops import *
from huffman import *

def run_length_coding():
    print()

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