# The reading and extraction of data of a bitmap (BMP) file is implemented.
import struct

# Function that gets the header information of a bitmap image
def read_bmp_header(content):
    header = struct.unpack('<2sIHHI', content[:14])
    magic_word, file_size, _, _, data_offset = header
    return {
        'magic_word': magic_word,
        'file_size': file_size,
        'data_offset': data_offset
    }

# Function that gets the data section of a bitmap image
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

# Function that gets the palette of a bitmap image (if any)
def read_bmp_palette(content, offset, colors_used):
    palette_data = content[offset:offset + colors_used * 4]
    palette = [struct.unpack('<BBBx', palette_data[i:i+4]) for i in range(0, len(palette_data), 4)]
    return palette

# Function that gets the image data of a bitmap image
def read_bmp_data(content, offset, width, height, bits_per_pixel):
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