from PIL import Image, ImageDraw

# Define the palette of colors as RGB tuples
palette = [(255, 0, 0),  # Red
           (0, 255, 0),  # Green
           (0, 0, 255),  # Blue
           (255, 255, 0),  # Yellow
           (255, 0, 255),  # Magenta
           (0, 255, 255)]  # Cyan

# Create a blank image with a white background
img = Image.new('RGB', (200, 200), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Define the size of each color block
block_size = 40

# Draw the colored blocks on the image
for i, color in enumerate(palette):
    x1 = i * block_size
    y1 = 0
    x2 = x1 + block_size
    y2 = 200
    draw.rectangle([x1, y1, x2, y2], fill=color)

# Show the image
img.show()
