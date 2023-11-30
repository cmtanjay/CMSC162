import json

# Your Huffman coded image as a binary string
huffman_coded_image = "0101010101010101"

# Your dictionary variable
my_dict = {'key1': 'value1', 'key2': 'value2'}

# Convert the dictionary to bytes
dict_bytes = json.dumps(my_dict).encode('utf-8')

# Calculate the number of bytes needed for the Huffman coded image
num_bytes_huffman = (len(huffman_coded_image) + 7) // 8

# Convert the Huffman coded image to bytes
byte_array_huffman = bytearray([int(huffman_coded_image[i:i+8], 2) for i in range(0, len(huffman_coded_image), 8)])

# Fill the last byte with zeros if needed
if len(byte_array_huffman) < num_bytes_huffman:
    byte_array_huffman.extend([0] * (num_bytes_huffman - len(byte_array_huffman)))

# Calculate the number of bytes needed for the dictionary
num_bytes_dict = len(dict_bytes)

# Combine the headers, Huffman coded image, and the dictionary
bmp_content = b'BM' + int.to_bytes(14 + 40 + num_bytes_huffman + num_bytes_dict, 4, 'little') + b'\0\0\0\0' + b'\x36\x00\x00\x00' + \
              b'\x28\x00\x00\x00' + int.to_bytes(num_bytes_huffman, 4, 'little') + b'\x00\x00\x00\x00' + int.to_bytes(num_bytes_huffman, 4, 'little') + \
              b'\x01\x00' + b'\x01\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x13\x0B' + b'\x00\x00\x13\x0B' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + \
              b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00' + \
              bytes(byte_array_huffman) + dict_bytes

# Write to the BMP file
with open('output_image.bmp', 'wb') as bmp_file:
    bmp_file.write(bmp_content)
