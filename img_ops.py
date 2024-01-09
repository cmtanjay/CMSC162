# This is where the basic operations for images like opening, saving, and displaying is implemented.
import variables
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import cv2

from bmp_extract import *
from progressBar import *

# This is the function that opens the image file
def open_img_file(self):
    filepath = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])
    if not filepath:
        return
    
    variables.orig_img = None
    variables.curr_img = None
    variables.red_channel = []
    variables.green_channel = []
    variables.blue_channel = []
    variables.pcx_image_data = []
    variables.palette = []
    variables.isDegraded = False
    
    if os.path.basename(filepath).split('.')[-1] == "bmp": # if a bmp file is opened
        image, bmp_info = openBMP(self,filepath)
    else: # if other image types (jpg, png, tiff, etc) are opened
        image = Image.open(filepath)
    
    self.rightsidebar.destroy()
    self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
    self.rightsidebar.grid(row=1, column=3, sticky="nsew")
    
    # Create a progress bar window
    self.progress_window = tk.Toplevel(self)
    self.progress_window.title("Progress")

    # Create a progress bar in the progress window
    progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
    progress_bar.pack(pady=10)
    
    update_progress(self, 0)
    
    show_image(self, image, " ")
    
    update_progress(self, 100)
    
    # Create the canvas in the right sidebar
    create_right_sidebar_canvas(self, 1,300)
    
    if os.path.basename(filepath).split('.')[-1] == "bmp": # if a bmp file is opened:
        # Add text to the canvas in the right side bar
        add_text_to_right_sidebar(self,"Image Information", x=76,y=30,fill="white",font=("Arial", 11, "bold"))
        add_text_to_right_sidebar(self, f"Width: {bmp_info['width']}", x=68, y=70, fill="white", font=("Arial", 11))
        add_text_to_right_sidebar(self, f"Height: {bmp_info['height']}", x=69, y=90, fill="white", font=("Arial", 11))
        add_text_to_right_sidebar(self, f"Color Planes: {bmp_info['color_planes']}", x=80, y=110, fill="white", font=("Arial", 11))
        add_text_to_right_sidebar(self, f"Bits per pixel: {bmp_info['bits_per_pixel']}", x=85, y=130, fill="white", font=("Arial", 11))
    
    # Destroys the status bar
    self.statusbar.destroy()
    self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
    self.statusbar.grid(row=2, columnspan=4, sticky="ew")
    self.create_statusbar_canvas()

    # Extract the filename from the full filepath
    filename = os.path.basename(filepath)
    self.add_text_to_statusbar(f"Status: {filename} loaded", x=120, y=20, fill="white", font=("Arial", 9,))

def openBMP(self,filepath):
    with open(filepath, "rb") as file:
        content = file.read()

    header_info = read_bmp_header(content)
    bmp_info = read_bmp_info(content)
    variables.bits_per_pixel = bmp_info['bits_per_pixel']
    variables.palette = read_bmp_palette(content, 54, bmp_info['colors_used'])
    bitmap_data = read_bmp_data(content, header_info['data_offset'], bmp_info['width'], bmp_info['height'], bmp_info['bits_per_pixel'])

    # print("Header:", header_info)
    # print("BMP Info:", bmp_info)

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

    variables.pcx_image_data = arranged_color
    variables.image_data = arranged_color
    variables.img_width = bmp_info["width"]
    variables.img_height = bmp_info["height"]

    # Create a blank image with a white background for the opened image
    img_bmp = Image.new('RGB', (bmp_info["width"], bmp_info["height"]), (255, 255, 255))

    draw = ImageDraw.Draw(img_bmp)

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
        
    variables.orig_img = img_bmp

    # Print or use the extracted information as needed
   
    # print("Color Palette:", color_palette)
    # print("Bitmap Data:", len(bitmap_data))
    
    # Draw the colored blocks on the image
    for i, color in enumerate(variables.pcx_image_data):
        rgb = list(color)
        variables.red_channel.append(rgb[0])
        variables.green_channel.append(rgb[1])
        variables.blue_channel.append(rgb[2])

    return img_bmp, bmp_info

def extract_bmp(self, filepath):
    with open(filepath, "rb") as file:
        content = file.read()

    header_info = read_bmp_header(content)
    bmp_info = read_bmp_info(content)
    bitmap_data = read_bmp_data(content, header_info['data_offset'], bmp_info['width'], bmp_info['height'], bmp_info['bits_per_pixel'])
    
    colors = [(bitmap_data[i+2], bitmap_data[i+1], bitmap_data[i]) for i in range(0, len(bitmap_data), 3)]

    arranged_color = [colors[i:i + bmp_info["width"]] for i in range(0, len(colors), bmp_info["width"])]
    arranged_color = [color for row in arranged_color[::-1] for color in row]

    variables.pcx_image_data = arranged_color
    variables.image_data = arranged_color
    variables.img_width = bmp_info["width"]
    variables.img_height = bmp_info["height"]

    # # Create a blank image with a white background for the opened image
    # img_bmp = Image.new('RGB', (bmp_info["width"], bmp_info["height"]), (255, 255, 255))
    # draw = ImageDraw.Draw(img_bmp)

    # drawImage1DArray(self, variables.image_data, draw, variables.palette)
        
    # variables.orig_img = img_bmp

    # return img_bmp

# Function that displays an image to the UI    
def show_image(self, image, string):
    if(image == None):
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        variables.curr_img = variables.pcx_image_data
        
        # Opens the image using PIL
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()
        
        # Define the padding size
        padding_x = 20  # Horizontal padding
        padding_y = 20  # Vertical padding

        # Calculate the available space for the image within the label
        available_width = label_width - (2 * padding_x)
        available_height = label_height - (2 * padding_y)
        
        image = img_resize_aspectRatio(self, image, available_width, available_height)

        # Convert the PIL image to a PhotoImage object
        image_tk = ImageTk.PhotoImage(image)

        self.image_label.config(image=image_tk)
        self.image_label.image = image_tk  # Keep a reference to avoid garbage collection

# Function that opens a PCX file
def open_pcx_file(self):
    filepath = askopenfilename(filetypes=[("PCX Files", "*.pcx")])
    
    if not filepath:
        print("Not a PCX file")
                    
        return
    
    # Create a progress bar window
    self.progress_window = tk.Toplevel(self)
    self.progress_window.title("Progress")

    # Create a progress bar in the progress window
    progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
    progress_bar.pack(pady=10)
    
    update_progress(self, 0)
    
    with open(filepath, "rb") as file:
        # content = file.read()
        # print(len(content))
        variables.orig_img = None
        variables.curr_img = None
        variables.red_channel = []
        variables.green_channel = []
        variables.blue_channel = []
        variables.pcx_image_data = []
        variables.palette = []
        variables.isDegraded = False
    
        # Extract the filename from the full filepath
        filename = os.path.basename(filepath)

        self.add_text_to_statusbar(f"Status: PCX Image \" {filename} \" loaded", x=150, y=20, fill="white", font=("Arial", 9,))
        
        self.header = file.read(128)
        
        file.seek(0)
        size = len(file.read())

        file.seek(128)
        image_data = file.read(size-128-768)
        
        file.seek(-768, 2)  # Go to the end of the file and move back 768 bytes
        color_data = file.read(768)
        
        i=0
        
        
        while(i < len(color_data)):
            variables.palette.append((color_data[i], color_data[i+1], color_data[i+2]))
            i += 3
        
        if self.header[0] != 10:
            raise ValueError("Not a valid PCX file.")
            
        else:
            # Extracts header information of the PCX file
            content = file.read()
            
            variables.manufacturer = self.header[0]
            variables.version = self.header[1]
            variables.encoding = self.header[2]
            variables.bits_per_pixel = self.header[3]
            x_min = self.header[4] + self.header[5] * 256
            y_min = self.header[6] + self.header[7] * 256
            x_max = self.header[8] + self.header[9] * 256
            y_max = self.header[10] + self.header[11] * 256
            
            variables.img_width = x_max - x_min + 1
            variables.img_height = y_max - y_min + 1
            print(f"{variables.img_width}x{variables.img_height}")
            
            variables.hdpi = self.header[12]
            variables.vdpi = self.header[14]
            variables.nplanes = self.header[65]
            variables.bytesperline = self.header[66] + self.header[67] * 256
            variables.paletteinfo = self.header[68]
            
            variables.pcx_image_data = decode(self, image_data)
            variables.image_data = variables.pcx_image_data
            variables.curr_img = variables.pcx_image_data
            print(f"addada: {len(variables.pcx_image_data)}")
            
            # Create a blank image with a white background for the opened image
            img_pcx = Image.new('RGB', (variables.img_width, variables.img_height), (255, 255, 255))
            
            draw_orig = ImageDraw.Draw(img_pcx)
            
            drawImage1DArray(self, variables.pcx_image_data, draw_orig, variables.palette)
            get_img_channels(self) # Extracts color channels
            
            variables.orig_img = img_pcx 
            show_image(self, img_pcx, " ")     # Displays the opened PCX image to the GUI
            
            # Create a blank image with a white background for the color palette
            img_palette = Image.new('RGB', (256, 256), (255, 255, 255))
            draw = ImageDraw.Draw(img_palette)

            # Define the size of each color block
            block_size = 16

            # Draw the colored blocks on the image
            for i, color in enumerate(variables.palette):
                if i%16 == 0:
                    x1 = 0
                    y1 = i
                    x2 = x1 + block_size
                    y2 = y1 + block_size
                else:
                    x1 = (i%16) * block_size
                    y1 = (i//16) * block_size
                    x2 = x1 + block_size
                    y2 = y1 + block_size
                    
                draw.rectangle([x1, y1, x2, y2], fill=color)

            # Resize the image to 128x128
            img_palette = img_palette.resize((128, 128), Image.LANCZOS)

            # Convert the PIL image to a PhotoImage object
            image_tk_palette = ImageTk.PhotoImage(img_palette)

            # Create a blank image with a white background
            img_pcx_small = Image.new('RGB', (variables.img_width, variables.img_height), (255, 255, 255))
            draw_orig_small = ImageDraw.Draw(img_pcx_small)
            
            # Define the size of each color block
            block_size = 1

            drawImage1DArray(self, variables.pcx_image_data, draw_orig_small, variables.palette)
            
            img_pcx_small = img_resize_aspectRatio(self, img_pcx_small, 256, 150)

            # Convert the PIL image to a PhotoImage object
            image_tk_orig = ImageTk.PhotoImage(img_pcx_small)

            # Create the canvas in the right sidebar
            create_right_sidebar_canvas(self, 1,50)

            add_text_to_right_sidebar(self, "Original Image ", x=65, y=30, fill="white", font=("Arial", 11, "bold"))
            display_image_on_right_sidebar(self, image_tk_orig, 2)

            # Create the canvas in the right sidebar
            create_right_sidebar_canvas(self, 3,300)

            # Add text to the canvas in the right sidebar
            add_text_to_right_sidebar(self, "Header Information", x=76, y=30, fill="white", font=("Arial", 11, "bold"))
            add_text_to_right_sidebar(self, f"Manufacturer: {variables.manufacturer}", x=68, y=70, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Version: {variables.version}", x=47, y=90, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Resolution: {variables.img_width} x {variables.img_height}", x=85, y=110, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Encoding: {variables.encoding}", x=53, y=130, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Bits Per Pixel: {variables.bits_per_pixel}", x=65, y=150, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"HDPI: {variables.hdpi}", x=43, y=170, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"VDPI: {variables.vdpi}", x=43, y=190, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Number of Color Planes: {variables.nplanes}", x=100, y=210, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Bytes Per Line: {variables.bytesperline}", x=78, y=230, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, f"Palette Info: {variables.paletteinfo}", x=60, y=250, fill="white", font=("Arial", 11))
            add_text_to_right_sidebar(self, "Color Palette", x=58, y=290, fill="white", font=("Arial", 11, "bold"))

            # Display the image on the canvas

            display_image_on_right_sidebar(self, image_tk_palette, 4)
            
    update_progress(self, 100)

# Function that resizes an image based on aspect ratio
def img_resize_aspectRatio(self, img, available_width, available_height):
    # Calculate the aspect ratio of the image
    aspect_ratio = img.width / img.height

    # Checks if the aspect ratio of the image is greater than the aspect ratio of the space available for the image to display
    if aspect_ratio > available_width/available_height:
        wpercent = available_width/float(img.width)
        hsize = int((img.height)*float(wpercent))
        img = img.resize((available_width, hsize))
    else:
        hpercent = available_height/float(img.height)
        wsize = int((img.width)*float(hpercent))
        img = img.resize((wsize, available_height))
    
    return img

# This is a function that executes the run length encoding that gets the index of colors from the palette in image data
def decode(self, data):
    decoded_data = []
    i = 0
    
    while i < len(data):
        if data[i] >= 192:
            run_length = data[i] - 192
            pixel_value = data[i+1]
            decoded_data.extend([pixel_value]*run_length)
            i += 2
        else:
            decoded_data.append(data[i])
            i += 1
            
    return decoded_data

# Function to create canvas for the right sidebar
def create_right_sidebar_canvas(self,row,height):
    # Create the canvas in the right sidebar
    self.canvas = tk.Canvas(self.rightsidebar, width=250, height=height, bg="#2B2B2B", highlightthickness=0)
    self.canvas.grid(row=row, column=2, sticky="nsew")

# Function to add text onto the canvas of the right side bar
def add_text_to_right_sidebar(self, text, x, y, fill, font):
    # Use the previously created canvas
    self.canvas.create_text(x, y, text=text, fill=fill, font=font)

# Function to display the generated color palette to the right side bar
def display_image_on_right_sidebar(self, image_tk, row):
    canvas = tk.Canvas(self.rightsidebar, width=256, height=150, bg="#2B2B2B", highlightthickness=0)
    canvas.grid(row=row, column=2, sticky="nsew")

    # Calculate the coordinates to center the image
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()
    image_width = image_tk.width()
    image_height = image_tk.height()
    
    x = (canvas_width - image_width) // 2
    y = (canvas_height - image_height) // 2

    # Create an image item on the canvas at the center
    canvas.create_image(x, y, anchor=tk.NW, image=image_tk)
    canvas.image = image_tk  # Keep a reference to avoid garbage collection
    
# Function that separates the image into the red, green, and blue channels
def get_img_channels(self):
    # Draw the colored blocks on the image
    for i, color in enumerate(variables.pcx_image_data):
        rgb = list(variables.palette[color])
        variables.red_channel.append(rgb[0])
        variables.green_channel.append(rgb[1])
        variables.blue_channel.append(rgb[2])
        
# Function that shows the histogram of a color channel in a pop up window    
def show_hist(self, channel, string):
    plt.close()
    channel = np.array(channel)
            
    plt.hist(channel, bins=256, color=string, alpha=0.7, rwidth=0.85)
    
    # Customize the plot (optional)
    plt.title(f"Histogram of the {string} channel of the image")
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    # Show the histogram
    plt.show()

# Function for showing histogram after applying different image processing techniques
def show_histogram(image_data, title):
    plt.hist(image_data, bins=256, range=(0, 256), density=True, color='gray', alpha=0.75)
    plt.title(title)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Function that displays the color channel in the UI    
def show_channel(self, channel, string):
    if not channel and variables.file_type == 1:
        print("WALAAAAA")
        
    elif variables.file_type == 2:
        variables.is_filtered = True
        variables.img_seq = []
        
        # Create a progress bar window
        self.progress_window = tk.Toplevel(self)
        self.progress_window.title("Progress")

        # Create a progress bar in the progress window
        progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
        progress_bar.pack(pady=10)
        
        value = 0
        num = 0
        self.progress_var.set(value)
        self.progress_window.update()
        
        for path in variables.image_paths:
            extract_bmp(self, path)
            
            color_channel = []
            
            if(string == "red"):
                for pixel in variables.pcx_image_data:
                    color_channel.append((pixel[0], 0, 0))
            elif(string == "green"):
                for pixel in variables.pcx_image_data:
                    color_channel.append((0, pixel[1], 0))
            elif(string == "blue"):
                for pixel in variables.pcx_image_data:
                    color_channel.append((0, 0, pixel[2]))
            
            # Creates output image
            channel_img = Image.new('RGB', (variables.img_width, variables.img_height), (255, 255, 255))
            draw_channel_img = ImageDraw.Draw(channel_img)
            
            drawImage1DArray(self, color_channel, draw_channel_img, [])
            variables.img_seq.append(channel_img)
            
            value += (1/len(variables.image_paths))*100
            self.progress_var.set(value)
            self.progress_window.update()
            
            num += 1
            print(num)
        
        self.progress_window.destroy()
        show_image(self, variables.img_seq[0], " ")
        
    elif variables.file_type == 3:
        variables.video_filepath = variables.orig_video_filepath
        video = cv2.VideoCapture(variables.video_filepath) 
        
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        variables.img_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        variables.img_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Use the current working directory as the output directory
        output_directory = os.getcwd()

        # Join the directory and file name to get the full file path
        output_video_filepath = os.path.join(output_directory, "video_output.avi")
        print(output_video_filepath)
        
        output_video = cv2.VideoWriter(output_video_filepath, fourcc, 10, (variables.img_width, variables.img_height))
        
        # Create a progress bar window
        self.progress_window = tk.Toplevel(self)
        self.progress_window.title("Progress")

        # Create a progress bar in the progress window
        progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
        progress_bar.pack(pady=10)
        
        value = 0
        num = 0
        self.progress_var.set(value)
        self.progress_window.update()
        
        current_frame = 0
        thumbnail = None
        
        while True:
            status, frame = video.read() 
            
            print(current_frame)
            if status:
                
                # Convert the frame to BMP format
                bmp_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Access pixel data
                frame_pixels = list(bmp_image.getdata())
                
                color_channel = []
                
                if(string == "red"):
                    for pixel in frame_pixels:
                        color_channel.append((pixel[0], 0, 0))
                elif(string == "green"):
                    for pixel in frame_pixels:
                        color_channel.append((0, pixel[1], 0))
                elif(string == "blue"):
                    for pixel in frame_pixels:
                        color_channel.append((0, 0, pixel[2]))
                
                # Creates output image
                channel_img = Image.new('RGB', (variables.img_width, variables.img_height), (255, 255, 255))
                draw_channel_img = ImageDraw.Draw(channel_img)
                
                drawImage1DArray(self, color_channel, draw_channel_img, [])
                
                new_frame = cv2.cvtColor(np.array(channel_img), cv2.COLOR_RGB2BGR)
                
                # Write the frame to the output video
                output_video.write(new_frame)
                
                if current_frame == 0:
                    # Convert frame to RGB format
                    frame1 = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
                    
                    # Convert frame to PhotoImage
                    img = Image.fromarray(frame1)
                    
                    # Opens the image using PIL
                    label_width = self.image_label.winfo_width()
                    label_height = self.image_label.winfo_height()
                    
                    # Define the padding size
                    padding_x = 20  # Horizontal padding
                    padding_y = 50  # Vertical padding

                    # Calculate the available space for the image within the label
                    available_width = label_width - (2 * padding_x)
                    available_height = label_height - (2 * padding_y)
                    
                    thumbnail = img_resize_aspectRatio(self, img, available_width, available_height)
                    
                value += (1/total_frames)*100
                self.progress_var.set(value)
                self.progress_window.update()
                
                num += 1
                    
                current_frame += 1
                    
            else:
                break
            
        self.progress_window.destroy()
        
        img_tk = ImageTk.PhotoImage(thumbnail)
        # Update label with the new frame
        self.image_label.img = img_tk
        self.image_label.config(image=img_tk)
        variables.video_filepath = output_video_filepath
            
    else:
        # Creates output image
        channel_img = Image.new('RGB', (variables.img_width, variables.img_height), (255, 255, 255))
        draw_channel_img = ImageDraw.Draw(channel_img)
        
        # Define the size of each color block
        block_size = 1

        # Draw the colored blocks on the image
        for i, color in enumerate(variables.pcx_image_data):
            if i % variables.img_width == 0:
                x1 = 0
                y1 = i // variables.img_width
                x2 = x1 + block_size
                y2 = y1 + block_size
            else:
                x1 = (i % variables.img_width) * block_size
                y1 = (i // variables.img_width) * block_size
                x2 = x1 + block_size
                y2 = y1 + block_size
        
            if(string == "red"):
                draw_channel_img.rectangle([x1, y1, x2, y2], fill=(channel[i], 0, 0))    
            elif(string == "green"):
                draw_channel_img.rectangle([x1, y1, x2, y2], fill=(0, channel[i], 0))
            elif(string == "blue"):
                draw_channel_img.rectangle([x1, y1, x2, y2], fill=(0, 0, channel[i]))

        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=4, sticky="ew")
        self.create_statusbar_canvas()
        
        if(string == "red"):
            self.add_text_to_statusbar("Status: Extracted Red Channel Filter to Image", x=180, y=20, fill="white", font=("Arial", 9,))
        elif(string == "green"):
            self.add_text_to_statusbar("Status: Extracted Green Channel Filter to Image", x=180, y=20, fill="white", font=("Arial", 9,))
        elif(string == "blue"):
            self.add_text_to_statusbar("Status: Extracted Blue Channel Filter to Image", x=180, y=20, fill="white", font=("Arial", 9,))
            
        show_image(self, channel_img, " ")
        show_hist(self, channel, string)
    
    

# Function for transforming the colored (RGB) image to grayscale
def get_grayscale_img(self):
    # Transforms image to grayscale
    row = []
    gray = []
    for i, color in enumerate(variables.pcx_image_data):
        if variables.palette == []:
            rgb = list(color)
        else:
            rgb = list(variables.palette[color])
            
        grayscale_value = (int)((rgb[0] + rgb[1] + rgb[2]) / 3)
        row.append(grayscale_value)

        if len(row) == variables.img_width:
            gray.append(row)
            row = []
            
    return gray

# Function that draws the passed pixel values to an image where the said pixel values are stored in a 2D array    
def drawImage(self, draw, gray):
    # Define the size of each color block
    block_size = 1

    for i, row in enumerate(gray):
        for j, color in enumerate(row):
            x1 = j
            y1 = i
            x2 = x1 + 1
            y2 = y1 + 1

            draw.rectangle([x1, y1, x2, y2], fill=color)

# Function that draws the passed pixel values to an image where the said pixel values are stored in a 1D array            
def drawImage1DArray(self, array, draw, palette):
    block_size = 1
        
    # Draw the colored blocks on the image
    for i, color in enumerate(array):
        if i % variables.img_width == 0:
            x1 = 0
            y1 = i // variables.img_width
            x2 = x1 + block_size
            y2 = y1 + block_size
        else:
            x1 = (i % variables.img_width) * block_size
            y1 = (i // variables.img_width) * block_size
            x2 = x1 + block_size
            y2 = y1 + block_size
        
        if palette == []:
            draw.rectangle([x1, y1, x2, y2], fill=color)
        else:
            draw.rectangle([x1, y1, x2, y2], fill=palette[color])
            
def natural_sort_key(s):
    # Custom sorting key for natural sorting
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]