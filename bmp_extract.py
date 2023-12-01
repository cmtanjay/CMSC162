import struct
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw #pip install pillow

import variables
from img_ops import *

def read_bmp_header(content):
    header = struct.unpack('<2sIHHI', content[:14])
    magic_word, file_size, _, _, data_offset = header
    return {
        'magic_word': magic_word,
        'file_size': file_size,
        'data_offset': data_offset
    }

def read_bmp_info(content):
    info = struct.unpack('<IiiHHIIIIII', content[14:54])
    return {
        'header_size': info[0],
        'width': info[1],
        'height': info[2],
        'color_planes': info[3],
        'bits_per_pixel': info[4],
        'compression': info[5],
        'image_size': info[6],
        'x_pixels_per_meter': info[7],
        'y_pixels_per_meter': info[8],
        'colors_used': info[9],
        'colors_important': info[10]
    }

def read_bmp_palette(content, offset, colors_used):
    palette_data = content[offset:offset + colors_used * 4]
    palette = [struct.unpack('<BBBx', palette_data[i:i+4]) for i in range(0, len(palette_data), 4)]
    return palette

def read_bmp_data(content, offset, width, height, bits_per_pixel):
    # Assuming bits_per_pixel is 8 (8 bits per pixel, grayscale) for simplicity
    # You may need to modify this part based on your specific BMP file format
    # if width % 4 == 0:
    #     data = content[offset:]
    # else:
    row_size = ((width * bits_per_pixel + 31) // 32) * 4
    
    # Extract pixel data
    pixel_data = content[offset:]
    
    data = []
    
    # Iterate over each row
    for i in range(height):
        # Calculate start and end index for each row
        start_index = i * row_size
        end_index = start_index + row_size

        # Read row data
        row_data = pixel_data[start_index:end_index]

        # Unpack pixel values
        pixels = struct.unpack('<{}B'.format(row_size), row_data)

        # Add pixel values to image data
        data.extend(pixels[:width * (bits_per_pixel // 8)])
            
    return data

def openBMP(filepath):
    with open(filepath, "rb") as file:
        content = file.read()

    header_info = read_bmp_header(content)
    bmp_info = read_bmp_info(content)
    variables.palette = read_bmp_palette(content, 54, bmp_info['colors_used'])
    bitmap_data = read_bmp_data(content, header_info['data_offset'], bmp_info['width'], bmp_info['height'], bmp_info['bits_per_pixel'])

    print("Header:", header_info)
    print("BMP Info:", bmp_info)

    colors = []
    i=0        

    while(i < len(bitmap_data)):
        colors.append((bitmap_data[i+2], bitmap_data[i+1], bitmap_data[i]))
        i += 3
        
    arranged_color = []

    row = []
    for i, color in enumerate(colors):
        row.append(color)
        
        if len(row) == bmp_info["width"]:
            arranged_color = row + arranged_color
            row = []

    variables.pcx_image_data = arranged_color
    variables.image_data = arranged_color
    variables.img_width = bmp_info["width"]
    variables.img_height = bmp_info["height"]

    # Create a blank image with a white background for the opened image
    img_pcx = Image.new('RGB', (bmp_info["width"], bmp_info["height"]), (255, 255, 255))

    draw = ImageDraw.Draw(img_pcx)

    block_size = 1
            
    # Draw the colored blocks on the image
    for i, color in enumerate(arranged_color):
        if i % bmp_info["width"] == 0:
            x1 = 0
            y1 = (i // bmp_info["width"])
            x2 = x1 + block_size
            y2 = y1 + block_size
        else:
            x1 = (i % bmp_info["width"]) * block_size
            y1 = (i // bmp_info["width"]) * block_size
            x2 = x1 + block_size
            y2 = y1 + block_size
        
        draw.rectangle([x1, y1, x2, y2], fill=color)
        
    variables.orig_img = img_pcx

    # Print or use the extracted information as needed
   
    # print("Color Palette:", color_palette)
    print("Bitmap Data:", len(bitmap_data))
    
    # Draw the colored blocks on the image
    for i, color in enumerate(variables.pcx_image_data):
        rgb = list(color)
        variables.red_channel.append(rgb[0])
        variables.green_channel.append(rgb[1])
        variables.blue_channel.append(rgb[2])

    return img_pcx
