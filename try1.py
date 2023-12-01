import struct
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw #pip install pillow
from collections import Counter
import json

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

# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# Main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}

    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

filepath = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])

with open(filepath, "rb") as file:
    content = file.read()

header_info = read_bmp_header(content)
bmp_info = read_bmp_info(content)
color_palette = read_bmp_palette(content, 54, bmp_info['colors_used'])
bitmap_data = read_bmp_data(content, header_info['data_offset'], bmp_info['width'], bmp_info['height'], bmp_info['bits_per_pixel'])

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

# # Print or use the extracted information as needed
# print("Header:", header_info)
# print("BMP Info:", bmp_info)
# print("Color Palette:", color_palette)
print("Bitmap Data:", len(bitmap_data))

colors = []
binary = []
i=0        

while(i < len(bitmap_data)):
    colors.append([bitmap_data[i+2], bitmap_data[i+1], bitmap_data[i]])
    binary.append(bin(bitmap_data[i+2])[2:].zfill(8)+bin(bitmap_data[i+1])[2:].zfill(8)+bin(bitmap_data[i])[2:].zfill(8))
    i += 3

colors.reverse()

j=0
dec=[]
while(j < len(binary)):
    dec.append(int(binary[j], 2))
    j +=1

# print(dec)

value_counts = Counter(dec)

# Sort the counts in descending order
sorted_value_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)

# print(sorted_value_counts)

nodes = sorted_value_counts
i = 0
while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    print(i)
    i+=1

huffmanCode = huffman_code_tree(nodes[0][0])

# print(huffmanCode)

coded = ""

for code in dec:
    coded = coded + huffmanCode[code]

print(f"orig_len: {len(binary)*24}")
print(f"huf_len: {len(coded)}")

# print(' Char | Huffman code ')
# print('----------------------')
# for (char, frequency) in sorted_value_counts:
#     print(' %-4r |%12s' % (char, huffmanCode[char]))
    
# for value, count in sorted_value_counts:
#     print(f"Value {value} occurs {count} times.")

# Calculate the number of bytes needed (ceil(len(huffman_coded_image) / 8))
num_bytes = (len(coded) + 7) // 8

# Convert the binary string to bytes
byte_array = bytearray([int(coded[i:i+8], 2) for i in range(0, len(coded), 8)])

# Fill the last byte with zeros if needed
if len(byte_array) < num_bytes:
    byte_array.extend([0] * (num_bytes - len(byte_array)))
    
# print(len(byte_array))

# Combine the headers and the encoded data
bmp_content = bytes(byte_array)

# huffman_codes_bytes = json.dumps(huffmanCode).encode('utf-8')

huffman_array = b''
for symbol, code in huffmanCode.items():
    new_code = bytearray([int(code[i:i+8], 2) for i in range(0, len(code), 8)])
    huffman_array += new_code + str(symbol).encode('utf-8')

# Calculate the size of the Huffman codes data
huffman_codes_size = len(huffman_array)
# print(huffman_array)

prev_offset = header_info['data_offset']

new_offset = int(header_info['data_offset'] ) + huffman_codes_size

byte_offset = new_offset.to_bytes(4, 'little')

# print(f"new: {new_offset}")
# print(f"off: {byte_offset}")

new = content[:10] + byte_offset + content[14:prev_offset] + huffman_array + bmp_content

# new = bmp_content + huffman_array

# Write to the BMP file
with open('output_image.bmp', 'wb') as bmp_file:
    bmp_file.write(new)
    

# print(bmp_content)