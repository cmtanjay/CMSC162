import heapq
import os
from PIL import Image
import numpy as np

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

def compress_image(image_path):
    # Load image
    image = Image.open(image_path)
    data = np.array(image)

    # Separate color channels
    channels = [data[:, :, i].ravel() for i in range(data.shape[2])]

    compressed_channels = []
    for channel in channels:
        # Build frequency dictionary
        freq_dict = build_freq_dict(channel)

        # Build Huffman tree
        huffman_tree = build_huffman_tree(freq_dict)

        # Build codewords mapping
        codewords_mapping = build_codewords_mapping(huffman_tree)

        # Encode data
        encoded_data = ''.join(codewords_mapping[symbol] for symbol in channel)

        # Convert binary string to bytes
        encoded_bytes = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            encoded_bytes.append(int(byte, 2))

        compressed_channels.append(encoded_bytes)

    # Save compressed image
    compressed_path = 'compressed_' + os.path.basename(image_path)
    with open(compressed_path, 'wb') as compressed_file:
        for channel in compressed_channels:
            compressed_file.write(bytes(channel))

    return image, compressed_path

def main():
    # Replace 'input_image.bmp' with your BMP image file path
    input_image_path = 'snail.bmp'

    # Compress image
    original_image, compressed_path = compress_image(input_image_path)

    # Display images
    original_image.show(title='Original Image')
    compressed_image = Image.open(compressed_path)
    compressed_image.show(title='Compressed Image')
    compressed_image.save('compressed_image.bmp')

if __name__ == "__main__":
    main()
