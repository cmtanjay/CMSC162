import heapq
import os
from PIL import Image
import variables
from PIL import Image, ImageDraw
from img_ops import *

class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(value, freq) for value, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_node = HuffmanNode(None, node1.freq + node2.freq)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(heap, merged_node)

    return heap[0]

def build_freq_dict(data):
    freq_dict = {}
    for symbol in data:
        freq_dict[symbol] = freq_dict.get(symbol, 0) + 1
    return freq_dict

def build_codewords_mapping(node, current_code="", mapping=None):
    if mapping is None:
        mapping = {}

    if node is not None:
        if node.value is not None:
            mapping[node.value] = current_code
        build_codewords_mapping(node.left, current_code + "0", mapping)
        build_codewords_mapping(node.right, current_code + "1", mapping)

    return mapping

def encode_data(data, codewords_mapping):
    encoded_data = ''.join(codewords_mapping[symbol] for symbol in data)
    return encoded_data

def compress_image(self, output_compressed_path):
    # Load image
    # image = Image.open(input_image_path)
    pixel_data = variables.image_data

    # Build frequency dictionary
    freq_dict = build_freq_dict(pixel_data)

    # Build Huffman tree
    huffman_tree = build_huffman_tree(freq_dict)

    # Build codewords mapping
    codewords_mapping = build_codewords_mapping(huffman_tree)

    # Encode data
    encoded_data = encode_data(pixel_data, codewords_mapping)

    # Convert binary string to bytes
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        encoded_bytes.append(int(byte, 2))

    # Save compressed data to a binary file
    with open(output_compressed_path, 'wb') as compressed_file:
        compressed_file.write(bytes(encoded_bytes))

    return huffman_tree, len(pixel_data), (len(encoded_data) + 7) // 8

def decode_data(encoded_data, huffman_tree):
    decoded_data = []
    current_node = huffman_tree

    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.value is not None:
            decoded_data.append(current_node.value)
            current_node = huffman_tree

    return decoded_data

def decompress_image(self, input_compressed_path, huffman_tree):
    # Load compressed data
    with open(input_compressed_path, 'rb') as compressed_file:
        compressed_data = compressed_file.read()

    # Convert compressed data to binary string
    encoded_data = ''.join(format(byte, '08b') for byte in compressed_data)

    # Decode data
    decoded_data = decode_data(encoded_data, huffman_tree)

    # Save decompressed data as a new image
    img_decompress = Image.new('RGB', (variables.img_width, variables.img_height), (255,255,255))
    draw_decompress = ImageDraw.Draw(img_decompress)
    
    drawImage1DArray(self, decoded_data, draw_decompress, variables.palette)
    show_image(self, img_decompress, " ")
    
