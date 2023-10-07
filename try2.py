from PIL import Image
import matplotlib.pyplot as plt

# Open the PCX image using Pillow
pcx_image = Image.open("scene.pcx")

# Convert the PCX image to grayscale if it's not already
pcx_image = pcx_image.convert("RGB")

# Calculate the histogram
histogram = pcx_image.histogram()

# Split the histogram into three color channels (R, G, B)
red_channel = histogram[0:256]
green_channel = histogram[256:512]
blue_channel = histogram[512:768]

# Plot the histograms
plt.figure(figsize=(8, 4))
plt.subplot(131)
plt.title("Red Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(range(256), red_channel, color="red", alpha=0.7)

plt.subplot(132)
plt.title("Green Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(range(256), green_channel, color="green", alpha=0.7)

plt.subplot(133)
plt.title("Blue Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(range(256), blue_channel, color="blue", alpha=0.7)

plt.tight_layout()
plt.show()
