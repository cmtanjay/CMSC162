import numpy as np #Download numpy
import matplotlib.pyplot as plt #Download matplotlib
from skimage import io

def read_pcx_file(file_path):
    with open(file_path, "rb") as f:
        # Read and validate the PCX header
        header = f.read(128)
        if header[0] != 10:
            raise ValueError("Not a valid PCX file.")
        
        # Extract image dimensions from the header
        print(f"Manufacturer: {header[0]}")
        print(f"Version: {header[1]}")
        
        x_min = header[4] + header[5] * 256
        y_min = header[6] + header[7] * 256
        x_max = header[8] + header[9] * 256
        y_max = header[10] + header[11] * 256
        
        width = x_max - x_min + 1
        height = y_max - y_min + 1
        
        print(f"Width: {width}, Height: {height}")
        
        # Read the palette (256 RGB color entries)
        f.seek(-768, 2)  # Go to the end of the file and move back 768 bytes
        palette = f.read(768)
        
        # Read the image data
        f.seek(128, 0)  # Move to the beginning of the image data
        image_data = f.read()
        
        print(len(palette))
        i = 0
        
        while(i < len(palette)):
            print(f"data {palette[i], palette[i+1], palette[i+2]}")
            plt.imshow([palette[i], palette[i+1], palette[i+2]])
            i += 3
        
        
        # print(f"data {palette[0], palette[1], palette[2]}")
        # print(f"data {palette[3], palette[4], palette[5]}")
        

if __name__ == "__main__":
    pcx_file_path = "scene.pcx"
    read_pcx_file(pcx_file_path)
