import heapq
from collections import defaultdict
from PIL import Image
import pickle

def get_frequency(image_path):
    img = Image.open(image_path).convert('L')
    pixel_values = list(img.getdata())
    frequency = defaultdict(int)
    for pixel in pixel_values:
        frequency[pixel] += 1
    return frequency, img.width, img.height

def build_huffman_tree(frequency):
    heap = [[weight, [pixel, ""]] for pixel, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return heap[0]

def generate_huffman_codes(tree):
    codes = {}
    for pair in tree[1:]:
        pixel, code = pair
        codes[pixel] = code
    return codes

def encode_image(image_path, huffman_codes):
    img = Image.open(image_path).convert('L')
    encoded_data = []
    for pixel in img.getdata():
        encoded_data.extend(huffman_codes[pixel])
    return encoded_data

def save_compressed_image(encoded_data, output_path, huffman_tree):
    with open(output_path, 'wb') as output_file:
        pickle.dump(huffman_tree, output_file)
        output_file.write(bytes(encoded_data))

def load_compressed_image(input_path):
    with open(input_path, 'rb') as input_file:
        huffman_tree = pickle.load(input_file)
        encoded_data = input_file.read()
    return huffman_tree, encoded_data

def decode_image(huffman_tree, encoded_data, width, height):
    decoded_data = []
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        for pixel, code in huffman_tree[1:]:
            if current_code == code:
                decoded_data.append(pixel)
                current_code = ""
                break
    decoded_img = Image.new('L', (width, height))
    decoded_img.putdata(decoded_data)
    return decoded_img

# Example usage for compression
image_path = 'snail.bmp'
output_path = 'compressed_image.bin'

# Step 1: Get frequency
frequency, width, height = get_frequency(image_path)

# Step 2: Build Huffman tree
huffman_tree = build_huffman_tree(frequency)

# Step 3: Generate Huffman codes
huffman_codes = generate_huffman_codes(huffman_tree)

# Step 4: Encode image
encoded_data = encode_image(image_path, huffman_codes)

# Step 5: Save compressed image
save_compressed_image(encoded_data, output_path, huffman_tree)

# Example usage for decompression
input_path = 'compressed_image.bin'

# Step 6: Load compressed image
loaded_huffman_tree, loaded_encoded_data = load_compressed_image(input_path)

# Step 7: Decode image
decoded_img = decode_image(loaded_huffman_tree, loaded_encoded_data, width, height)
decoded_img.show()
