from PIL import Image

def convert_tiff_to_bmp_and_get_pixels(input_path):
    try:
        # Open the TIFF image
        tiff_image = Image.open(input_path)

        # Convert the image to BMP format
        bmp_image = tiff_image.convert('RGB')

        # Access pixel data
        pixels = list(bmp_image.getdata())

        print("Pixel data:", pixels)

        return bmp_image

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
input_tiff_path = 'motion/motion01.512.tiff'

bmp_image = convert_tiff_to_bmp_and_get_pixels(input_tiff_path)

if bmp_image:
    # Save the BMP image
    output_bmp_path = 'output_image.bmp'
    bmp_image.save(output_bmp_path)
    print(f"Conversion successful. BMP image saved at {output_bmp_path}")
