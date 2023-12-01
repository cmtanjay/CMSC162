import variables
from PIL import Image, ImageDraw
from img_ops import *

def run_length_coding():
    print()

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
    
def huffman_coding(self):
    if not variables.image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        colors = []
        count = []
        i=0      
        before_compress = len(variables.image_data)
        
        while(i < len(variables.image_data)):
            if variables.image_data[i] not in colors:
                colors.append(variables.image_data[i])
                count.append([len(colors)-1, 1])
            else:
                count[colors.index(variables.image_data[i])][1] += 1
            # print(i)
            i += 1

        # Sort the 2D array based on the values in the second column
        sorted_array = sorted(count, key=lambda x: x[1])
            
        nodes = sorted_array
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

        print(huffmanCode)

        coded = ""

        for color in variables.image_data:
            code = colors.index(color)
            coded = coded + huffmanCode[code]
        
        # print(f"huf_len: {len(coded)}")
            
        after_compress = (len(coded) + 7) // 8
        
        print(f"before: {before_compress}")
        print(f"after: {after_compress}")
        
        deets = decode_huffman(coded, huffmanCode)
        print(deets)
        
        # Calculate the number of bytes needed (ceil(len(huffman_coded_image) / 8))
        num_bytes = (len(deets) + 7) // 8

        # Convert the binary string to bytes
        byte_array = bytearray([int(deets[i:i+8], 2) for i in range(0, len(deets), 8)])
        
        # Fill the last byte with zeros if needed
        if len(byte_array) < num_bytes:
            byte_array.extend([0] * (num_bytes - len(byte_array)))

        # Combine the headers and the encoded data
        bmp_content = bytes(byte_array)
        
        huffman_array = b''
        for symbol, code in huffmanCode.items():
            print(f"symbol: {symbol}")
            new_code = bytearray([int(code[i:i+8], 2) for i in range(0, len(code), 8)])
            byte_length = (symbol.bit_length() + 7) // 8  # Calculate the number of bytes needed
            byte_representation = symbol.to_bytes(byte_length, 'big')
            huffman_array += byte_representation + new_code

        # Calculate the size of the Huffman codes data
        huffman_codes_size = len(huffman_array)
        
        new = bmp_content + huffman_array

        # Write to the BMP file
        with open('output.bmp', 'wb') as bmp_file:
            bmp_file.write(new)
        
        #  # Create a blank image with a white background for the opened image
        # img_pcx = Image.new('RGB', (variables.img_width, variables.img_height), (255, 255, 255))
        
        # draw_orig = ImageDraw.Draw(img_pcx)
        
        # drawImage1DArray(self, deets, draw_orig, variables.palette)
        # show_image(self, img_pcx, " ")     # Displays the opened PCX image to the GUI
        # variables.curr_img = img_pcx
        # print("Na show na")
        
def decode_huffman(huffman_coded, codes):
    decoded_data = []
    current_code = ""
    
    for bit in huffman_coded:
        current_code += bit
        if current_code in codes.values():
            decoded_data.append([key for key, value in codes.items() if value == current_code][0])
            current_code = ""
            
    return decoded_data