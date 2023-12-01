from PIL import Image
import random

def apply_gaussian_noise(image_path, sigma):
    # Open the image
    img = Image.open(image_path).convert('L')  # Convert to grayscale if not already

    # Get image dimensions
    width, height = img.size

    # Create a new image with the same size
    noisy_img = Image.new('L', (width, height))

    # Apply Gaussian noise to each pixel
    for x in range(width):
        for y in range(height):
            pixel_value = img.getpixel((x, y))
            noise = int(random.gauss(0, sigma))
            noisy_value = max(0, min(255, pixel_value + noise))
            noisy_img.putpixel((x, y), noisy_value)

    # Save the noisy image
    noisy_img.save('noisy_image.pcx')

# Example: Apply Gaussian noise with sigma=20 to 'original_image.png'
apply_gaussian_noise('scene.pcx', 20)
