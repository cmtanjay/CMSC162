from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
from tkinter import ttk
from customtkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import matplotlib.pyplot as plt
import numpy as np
import os

from ToolTip import CreateToolTip

# This is the class constructor for the Image Processing App
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.orig_img = None
        self.curr_img = None
        self.red_channel = []
        self.green_channel = []
        self.blue_channel = []
        self.n = 3

        # Configures the app window
        self.title("Image Processor")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        

        # Gets the screen width and height
        screen_width = self.winfo_screenwidth() - 10
        screen_height = self.winfo_screenheight() - 100

        # Sets window size with screen dimension
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Configures the top bar of the App GUI
        self.topbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=1, relief="solid")
        self.topbar.grid(row=0, columnspan=3, sticky="ew") 
        
        # Configures the side bar of the App GUI
        self.sidebar = tk.Frame(self, width=100, bg="#2B2B2B")
        self.sidebar.grid(row=1, column=0, rowspan=4, sticky="nsew")
        
        # Configures the right side bar of the App GUI
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=2, sticky="nsew")
        
        # Configures the status bar of the App GUI
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        
        # Create the canvas in the right sidebar
        self.create_statusbar_canvas()

        #Adds items to the status bar
        self.add_text_to_statusbar("Status: No image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
        
        # Configures the Menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Creates the File Menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # Adds menu items to the File menu
        file_menu.add_command(label='New')
        file_menu.add_separator()
        
        # Adds menu items to the File menu
        file_menu.add_command(label='Save as', command=self.save_file_as)
        file_menu.add_separator()

        # Adds Exit menu item
        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        # Add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )
        # Create the Help Menu
        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        # Adds items on Help menu
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # Adds the Help menu to the menubar
        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )
        
        # Configures the portion of the GUI where the image will reside
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=1, sticky="nsew")

        img_pcx = Image.open("assets\pcx.png")
        img_pcx = img_pcx.resize((35,35))
        icon_pcx = ImageTk.PhotoImage(img_pcx)
    
        # Configures open PCX file button
        btn_open_pcx = tk.Button(self.topbar, image=icon_pcx, command=self.open_pcx_file, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_open_pcx.photo = icon_pcx
        btn_open_pcx.grid(row=1, column=1, sticky="ew")
        CreateToolTip(btn_open_pcx, "Open PCX")

        img = Image.open("assets\img.png")
        img = img.resize((35,35))
        icon_img = ImageTk.PhotoImage(img)

        # Configures open image file button
        btn_open_img = tk.Button(self.topbar, image=icon_img, command=self.open_img_file, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_open_img.photo = icon_img
        btn_open_img.grid(row=1, column=2, sticky="ew")
        CreateToolTip(btn_open_img, "Open Image")

        img_close = Image.open("assets\close.png")
        img_close = img_close.resize((35,35))
        icon_close = ImageTk.PhotoImage(img_close)

        # Configures close file button
        btn_close_file = tk.Button(self.topbar, image=icon_close, command=self.close_img, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_close_file.photo = icon_close
        btn_close_file.grid(row=1, column=3, sticky="ew")
        CreateToolTip(btn_close_file, "Close File")
        
        img_orig_img = Image.open("assets\\revert.png")
        img_orig_img = img_orig_img.resize((35,35))
        icon_orig_img = ImageTk.PhotoImage(img_orig_img)

        # Configures orig image button
        btn_orig_img = tk.Button(self.topbar, image=icon_orig_img, command=lambda: self.show_image(self.orig_img), background="#2F333A", relief="ridge", borderwidth=0)
        btn_orig_img.photo = icon_orig_img
        btn_orig_img.grid(row=1, column=4, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_orig_img, "Revert to Original Image")
        
        # Configures red channel button
        btn_red_channel = tk.Button(self.topbar,  text="     ", command=lambda: self.show_channel(self.red_channel, "red"), font=("Arial", 10), background="#FF0000", foreground="white",relief="ridge", borderwidth=2)
        btn_red_channel.grid(row=1, column=5, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_red_channel, "Red Channel")
        
        # Configures green channel button
        btn_green_channel = tk.Button(self.topbar,  text="     ", command=lambda: self.show_channel(self.green_channel, "green"), font=("Arial", 10), background="#00FF00", foreground="white",relief="ridge", borderwidth=2)
        btn_green_channel.grid(row=1, column=6, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_green_channel, "Green Channel")
        
        # Configures blue channel button
        btn_blue_channel = tk.Button(self.topbar,  text="     ", command=lambda: self.show_channel(self.blue_channel, "blue"), font=("Arial", 10), background="#0000FF", foreground="white",relief="ridge", borderwidth=2)
        btn_blue_channel.grid(row=1, column=7, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_blue_channel, "Blue Channel")
        
        img_grayscale = Image.open("assets\grayscale.png")
        img_grayscale = img_grayscale.resize((35,35))
        icon_grayscale = ImageTk.PhotoImage(img_grayscale)
        
        # Configures grayscale button
        btn_grayscale = tk.Button(self.topbar, image=icon_grayscale, command=self.grayscale_transform, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_grayscale.photo = icon_grayscale
        btn_grayscale.grid(row=1, column=8, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_grayscale, "Grayscale Transform (R+G+B)/3")
        
        img_negative = Image.open("assets\\negative.png")
        img_negative = img_negative.resize((35,35))
        icon_negative = ImageTk.PhotoImage(img_negative)
        
        # Configures negative button
        btn_negative = tk.Button(self.topbar, image=icon_negative, command=self.negative_transform, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_negative.photo = icon_negative
        btn_negative.grid(row=1, column=9, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_negative, "Negative")
        
        img_BW = Image.open("assets\BW.png")
        img_BW = img_BW.resize((35,35))
        icon_BW = ImageTk.PhotoImage(img_BW)
        
        # Configures B/W button
        btn_BW = tk.Button(self.topbar, image=icon_BW, command=self.BW_manual_thresholding, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_BW.photo = icon_BW
        btn_BW.grid(row=1, column=10, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_BW, "Black and White w/ Thresholding")
        
        img_gamma = Image.open("assets\gamma.png")
        img_gamma = img_gamma.resize((35,35))
        icon_gamma = ImageTk.PhotoImage(img_gamma)
        
        # Configures Power-Law button
        btn_gamma = tk.Button(self.topbar, image=icon_gamma, command=self.Power_law_transform, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_gamma.photo = icon_gamma
        btn_gamma.grid(row=1, column=11, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_gamma, "Power-Law (Gamma) Transform")
        
        img_avg = Image.open("assets\\avg.png")
        img_avg = img_avg.resize((30,30))
        icon_avg = ImageTk.PhotoImage(img_avg)
        
        # Configures Power-Law button
        btn_avg_filter = tk.Button(self.sidebar, image=icon_avg, command=self.average_filter, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_avg_filter.photo = icon_avg
        btn_avg_filter.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_avg_filter, "Averaging Filter")
        
        img_mdn = Image.open("assets\median.png")
        img_mdn = img_mdn.resize((30,30))
        icon_mdn = ImageTk.PhotoImage(img_mdn)
        
        btn_median = tk.Button(self.sidebar, image=icon_mdn, command=self.median_filter, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_median.photo = icon_mdn
        btn_median.grid(row=1, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_median, "Median Filter")
        
        img_highpass = Image.open("assets\highpass.png")
        img_highpass = img_highpass.resize((30,30))
        icon_highpass = ImageTk.PhotoImage(img_highpass)
        
        btn_laplacian = tk.Button(self.sidebar, image=icon_highpass, command=self.laplacian_filter, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_laplacian.photo = icon_highpass
        btn_laplacian.grid(row=2, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_laplacian, "Highpass Filter (Laplacian Operator)")

        img_unsharp = Image.open("assets\mask.png")
        img_unsharp = img_unsharp.resize((30,30))
        icon_unsharp = ImageTk.PhotoImage(img_unsharp)

        btn_unsharp = tk.Button(self.sidebar, image=icon_unsharp, command=self.unsharp_masking, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_unsharp.photo = icon_unsharp
        btn_unsharp.grid(row=3, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_unsharp, "Unsharp Masking")

        img_highboost = Image.open("assets\highboost.png")
        img_highboost = img_highboost.resize((30,30))
        icon_highboost = ImageTk.PhotoImage(img_highboost)

        btn_highboost = tk.Button(self.sidebar, image=icon_highboost, command=self.highboost_filter, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_highboost.photo = icon_highboost
        btn_highboost.grid(row=4, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_highboost, "Highboost Filtering")

        img_gradient = Image.open("assets\gradient.png")
        img_gradient = img_gradient.resize((30,30))
        icon_gradient = ImageTk.PhotoImage(img_gradient)
        
        btn_gradient = tk.Button(self.sidebar, image=icon_gradient, command=self.gradient_filter, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_gradient.photo = icon_gradient
        btn_gradient.grid(row=5, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_gradient, "Gradient: Sobel Magnitude Operator")
    
    # This is the function that opens the image file
    def open_img_file(self):
        filepath = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])
        if not filepath:
            return
        
        self.orig_img = None
        self.curr_img = None
        self.red_channel = []
        self.green_channel = []
        self.blue_channel = []
        
        image = Image.open(filepath)
        self.show_image(image)
        
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()

        self.rightsidebar.destroy()
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=2, sticky="nsew")

        # Extract the filename from the full filepath
        filename = os.path.basename(filepath)
        self.add_text_to_statusbar(f"Status: {filename} loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    
    # Function that displays an image to the UI    
    def show_image(self, image):
        if(image == None):
            print("WALAAAAAA")
            #Show status of image here when there's no image loaded
            #self.canvas.delete(self.add_text_to_statusbar)
            self.add_text_to_statusbar("Status: No image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
        else:
            
            # Opens the image using PIL
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()
            
            # Define the padding size
            padding_x = 20  # Horizontal padding
            padding_y = 20  # Vertical padding

            # Calculate the available space for the image within the label
            available_width = label_width - (2 * padding_x)
            available_height = label_height - (2 * padding_y)

            # Calculate the aspect ratio of the image
            aspect_ratio = image.width / image.height

            # Checks if the aspect ratio of the image is greater than the aspect ratio of the space available for the image to display
            if aspect_ratio > available_width/available_height:
                wpercent = available_width/float(image.width)
                hsize = int((image.height)*float(wpercent))
                image = image.resize((available_width, hsize))
            else:
                hpercent = available_height/float(image.height)
                wsize = int((image.width)*float(hpercent))
                image = image.resize((wsize, available_height))


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
        
        with open(filepath, "rb") as file:
            self.orig_img = None
            self.curr_img = None
            self.red_channel = []
            self.green_channel = []
            self.blue_channel = []
        
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
            self.palette=[]
            
            while(i < len(color_data)):
                self.palette.append((color_data[i], color_data[i+1], color_data[i+2]))
                i += 3
            
            if self.header[0] != 10:
                raise ValueError("Not a valid PCX file.")
                
            else:
                # Extracts header information of the PCX file
                content = file.read()
                
                manufacturer = self.header[0]
                version = self.header[1]
                encoding = self.header[2]
                bits_per_pixel = self.header[3]
                x_min = self.header[4] + self.header[5] * 256
                y_min = self.header[6] + self.header[7] * 256
                x_max = self.header[8] + self.header[9] * 256
                y_max = self.header[10] + self.header[11] * 256
                
                self.width = x_max - x_min + 1
                self.height = y_max - y_min + 1
                print(f"{self.width}x{self.height}")
                
                hdpi = self.header[12]
                vdpi = self.header[14]
                nplanes = self.header[65]
                bytesperline = self.header[66] + self.header[67] * 256
                paletteinfo = self.header[68]
                
                self.pcx_image_data = self.decode(image_data)
                print(f"addada: {len(self.pcx_image_data)}")
                
                # Create a blank image with a white background for the opened image
                img_pcx = Image.new('RGB', (self.width, self.height), (255, 255, 255))
                
                draw_orig = ImageDraw.Draw(img_pcx)

                # Define the size of each color block
                block_size = 1

                # Draw the colored blocks on the image
                for i, color in enumerate(self.pcx_image_data):
                    if i % self.width == 0:
                        x1 = 0
                        y1 = i // self.width
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                    else:
                        x1 = (i % self.width) * block_size
                        y1 = (i // self.width) * block_size
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                        
                    draw_orig.rectangle([x1, y1, x2, y2], fill=self.palette[color])
                
                self.get_img_channels() # Extracts color channels
                
                self.orig_img = img_pcx 
                self.show_image(img_pcx)     # Displays the opened PCX image to the GUI
                
                # Create a blank image with a white background for the color palette
                img_palette = Image.new('RGB', (256, 256), (255, 255, 255))
                draw = ImageDraw.Draw(img_palette)

                # Define the size of each color block
                block_size = 16

                # Draw the colored blocks on the image
                for i, color in enumerate(self.palette):
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
                img_pcx_small = Image.new('RGB', (256, 256), (255, 255, 255))
                draw_orig_small = ImageDraw.Draw(img_pcx_small)
                
                # Define the size of each color block
                block_size = 1

                # Draw the colored blocks on the image
                for i, color in enumerate(self.pcx_image_data):
                    if i % self.width == 0:
                        x1 = 0
                        y1 = i // self.width
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                    else:
                        x1 = (i % self.width) * block_size
                        y1 = (i // self.width) * block_size
                        x2 = x1 + block_size
                        y2 = y1 + block_size
                        
                    draw_orig_small.rectangle([x1, y1, x2, y2], fill=self.palette[color])
                
                # Resize the image to 128x128
                img_pcx_small = img_pcx_small.resize((128, 128), Image.LANCZOS)

                # Convert the PIL image to a PhotoImage object
                image_tk_orig = ImageTk.PhotoImage(img_pcx_small)

                # Create the canvas in the right sidebar
                self.create_right_sidebar_canvas(1,50)

                self.add_text_to_right_sidebar("Original Image ", x=65, y=30, fill="white", font=("Arial", 11, "bold"))
                self.display_image_on_right_sidebar(image_tk_orig, 2)

                # Create the canvas in the right sidebar
                self.create_right_sidebar_canvas(3,300)

                # Add text to the canvas in the right sidebar
                self.add_text_to_right_sidebar("Header Information", x=76, y=30, fill="white", font=("Arial", 11, "bold"))
                self.add_text_to_right_sidebar(f"Manufacturer: {manufacturer}", x=68, y=70, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Version: {version}", x=47, y=90, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Resolution: {self.width} x {self.height}", x=85, y=110, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Encoding: {encoding}", x=53, y=130, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Bits Per Pixel: {bits_per_pixel}", x=65, y=150, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"HDPI: {hdpi}", x=43, y=170, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"VDPI: {vdpi}", x=43, y=190, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Number of Color Planes: {nplanes}", x=100, y=210, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Bytes Per Line: {bytesperline}", x=78, y=230, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar(f"Palette Info: {paletteinfo}", x=60, y=250, fill="white", font=("Arial", 11))
                self.add_text_to_right_sidebar("Color Palette", x=58, y=290, fill="white", font=("Arial", 11, "bold"))

                # Display the image on the canvas

                self.display_image_on_right_sidebar(image_tk_palette, 4)
                
    # Function that allows the user to save an image in the program
    def save_file_as(self, event=None):
        file = asksaveasfilename(defaultextension=".pcx", filetypes=[("PCX Files", "*.pcx")])
        self.curr_img = self.curr_img.save(file)
    
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

    # Function to create a canvas for the status bar
    def create_statusbar_canvas(self):
        # Create the canvas in the right sidebar
        self.canvas = tk.Canvas(self.statusbar, width=2040, height=40, bg="#2B2B2B", highlightthickness=0)
        self.canvas.grid(row=1, columnspan=3, sticky="nsew")

    # Function to add text onto the canvas of the status bar
    def add_text_to_statusbar(self, text, x, y, fill, font):
        # Clear the previous text on the canvas
        self.canvas.delete("status_text")

        # Use the previously created canvas
        self.canvas.create_text(x, y, text=text, fill=fill, font=font, justify="right",tags="status_text")
    
    # Function that separates the image into the red, green, and blue channels
    def get_img_channels(self):
        # Draw the colored blocks on the image
        for i, color in enumerate(self.pcx_image_data):
            rgb = list(self.palette[color])
            self.red_channel.append(rgb[0])
            self.green_channel.append(rgb[1])
            self.blue_channel.append(rgb[2])
    
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
    
    # Function that displays the color channel in the UI    
    def show_channel(self, channel, string):
        if not channel:
            print("WALAAAAA")
        else:
            # Creates output image
            channel_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
            draw_channel_img = ImageDraw.Draw(channel_img)
            
            # Define the size of each color block
            block_size = 1

            # Draw the colored blocks on the image
            for i, color in enumerate(self.pcx_image_data):
                if i % self.width == 0:
                    x1 = 0
                    y1 = i // self.width
                    x2 = x1 + block_size
                    y2 = y1 + block_size
                else:
                    x1 = (i % self.width) * block_size
                    y1 = (i // self.width) * block_size
                    x2 = x1 + block_size
                    y2 = y1 + block_size
                
                rgb = list(self.palette[color])
            
                # Extracts the color channels
                if(string == "red"):
                    draw_channel_img.rectangle([x1, y1, x2, y2], fill=(rgb[0], 0, 0))    
                elif(string == "green"):
                    draw_channel_img.rectangle([x1, y1, x2, y2], fill=(0, rgb[1], 0))
                elif(string == "blue"):
                    draw_channel_img.rectangle([x1, y1, x2, y2], fill=(0, 0, rgb[2]))

            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            
            if(string == "red"):
                self.add_text_to_statusbar("Status: Extracted Red Channel Filter to Image", x=180, y=20, fill="white", font=("Arial", 9,))
            elif(string == "green"):
                self.add_text_to_statusbar("Status: Extracted Green Channel Filter to Image", x=180, y=20, fill="white", font=("Arial", 9,))
            elif(string == "blue"):
                self.add_text_to_statusbar("Status: Extracted Blue Channel Filter to Image", x=180, y=20, fill="white", font=("Arial", 9,))
                
            self.show_image(channel_img)
            self.show_hist(channel, string)
    
    # Function for transforming the colored (RGB) image to grayscale
    def get_grayscale_img(self):
        # Transforms image to grayscale
        row = []
        gray = []
        for i, color in enumerate(self.pcx_image_data):
            rgb = list(self.palette[color])
            grayscale_value = (int)((rgb[0] + rgb[1] + rgb[2]) / 3)
            row.append(grayscale_value)

            if len(row) == self.width:
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
    def drawImage1DArray(self, array, draw):
        block_size = 1
            
        # Draw the colored blocks on the image
        for i, color in enumerate(array):
            if i % self.width == 0:
                x1 = 0
                y1 = i // self.width
                x2 = x1 + block_size
                y2 = y1 + block_size
            else:
                x1 = (i % self.width) * block_size
                y1 = (i // self.width) * block_size
                x2 = x1 + block_size
                y2 = y1 + block_size
            
            draw.rectangle([x1, y1, x2, y2], fill=color)
    
    # Function that transforms the RGB PCX file to Grayscale
    def grayscale_transform(self):
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Creates the output image
            grayscale_img = Image.new('L', (self.width, self.height), 255)
            draw_grayscale = ImageDraw.Draw(grayscale_img)
            
            gray = self.get_grayscale_img() # transforms image to grayscale
            
            self.drawImage(draw_grayscale, gray) # draws resulting pixel values to image
                
            self.show_image(grayscale_img) # shows image to GUI
            self.curr_img = grayscale_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar("Status: Image transformed to grayscale through transformation function (R+G+B)/3", x=250, y=20, fill="white", font=("Arial", 9,))
    
    # Function that transforms the RGB PCX file to Negative image
    def negative_transform(self):
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Creates the output image
            negative_img = Image.new('L', (self.width, self.height), 255)
            draw_negative = ImageDraw.Draw(negative_img)
            
            gray = self.get_grayscale_img()
            
            # Define the size of each color block
            block_size = 1

            # Draws resulting pixel values to an image
            for i, row in enumerate(gray):
                for j, color in enumerate(row):
                    x1 = j
                    y1 = i
                    x2 = x1 + 1
                    y2 = y1 + 1

                    draw_negative.rectangle([x1, y1, x2, y2], fill=(255-color))
                
            self.show_image(negative_img)
            self.curr_img = negative_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar("Status: Image transformed to negative image through transformation function s = L - 1 - r", x=300, y=20, fill="white", font=("Arial", 9,))
    
    # Function that transforms the PCX image to Black/White via Manual Thresholding      
    def BW_manual_thresholding(self):
        # Function that pops up a window that show a slider for the manual threshold value
        def open_popup():
            window = tk.Toplevel()
            window.geometry("400x130+500+300")
            window.title("Black/White via Manual Thresholding")
            window.resizable(False, False)
            # tk.Label(window, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)
            
            window.columnconfigure(0, weight=2)
            window.columnconfigure(1, weight=5)
            
            current_value = tk.IntVar(value=0)
            threshold = tk.IntVar()
            
            # Monitors any change in text box
            def entry_changed(event):
                value = text_box.get()  # Get the value from the entry box
                if value.isdigit() and int(value) >= 0 and int(value) <= 255:  # Check if the value is a valid integer and is between 0 and 255
                    current_value.set(int(value))  # Set the slider value to the entry value
                else:
                    err_window = tk.Toplevel()
                    err_window.geometry("400x130+500+300")
                    err_window.title("Black/White via Manual Thresholding")
                    err_window.resizable(False, False)
                    ttk.Label(err_window, text='Threshold value must be between 0 to 255', font=('Arial 10 bold')).place(x=50, y=35)
                    btn_ok = tk.Button(err_window, command=err_window.destroy, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
                    btn_ok.place(x=80, y=85)

            # Monitors any change in the slider
            def slider_changed(*args):
                value = current_value.get()
                text_box.delete(0, tk.END)  # Clear the entry box
                text_box.insert(0, value)

            # Function that executes when OK button is clicked
            def on_click():
                value = current_value.get()
                threshold.set(value)
                window.destroy()

            # label for the slider
            ttk.Label(window, text='Slider:', font=('Arial 10 bold')).place(x=15, y=10)

            #  slider
            ttk.Scale(window, from_= 0, to = 255, orient='horizontal', command=slider_changed, variable=current_value, length=310).place(x=65, y=10)

            # current value label
            ttk.Label(window, text='Threshold Value:', font=('Arial 10 bold')).place(x=150, y=35)
            
            text_box = tk.Entry(window, bg="white", textvariable=current_value, width=5, font=('Arial 13'))
            text_box.place(x=160, y=55)
            text_box.bind("<KeyRelease>", entry_changed)

            current_value.trace("w", slider_changed)
            
            btn = tk.Button(window, command=on_click, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
            btn.place(x=165, y=85)
            
            window.wait_window(window)  # Wait for the window to be destroyed
            return threshold.get()
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            threshold = open_popup()
            # Creates the output image
            BW_img = Image.new('L', (self.width, self.height), 255)
            draw_BW = ImageDraw.Draw(BW_img)
            
            gray = self.get_grayscale_img() # transforms image to grayscale
            
            # Define the size of each color block
            block_size = 1

            # Draws the resulting pixel values to an image
            for i, row in enumerate(gray):
                for j, color in enumerate(row):
                    x1 = j
                    y1 = i
                    x2 = x1 + 1
                    y2 = y1 + 1

                    if(color <= threshold):
                        color = 0
                    else:
                        color = 255

                    draw_BW.rectangle([x1, y1, x2, y2], fill=color)
                
            self.show_image(BW_img)
            self.curr_img = BW_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Image transformed to Black&White at threshold = {threshold}", x=200, y=20, fill="white", font=("Arial", 9,))
    
    # Function that executes the Power-Law (Gamma) Transformation to the PCX file
    def Power_law_transform(self):
        # Function that pops up a window that lets the user input the gamma value    
        def open_popup():
            window = tk.Toplevel()
            window.geometry("400x130+500+300")
            window.title("Power-Law Transformation")
            window.resizable(False, False)
            # tk.Label(window, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)
            
            window.columnconfigure(0, weight=2)
            window.columnconfigure(1, weight=5)
            
            current_value = tk.DoubleVar(value=0.0)

            # Detects the value inside the text box
            def entry_changed(event):
                value = text_box.get()  # Get the value from the entry box
                if int(value) >= 0:  # Check if the value is a positive constant
                    current_value.set(int(value))  # Set the slider value to the entry value
                else:
                    err_window = tk.Toplevel()
                    err_window.geometry("400x130+500+300")
                    err_window.title("Black/White via Manual Thresholding")
                    err_window.resizable(False, False)
                    ttk.Label(err_window, text='Gamma value must be a positive constant', font=('Arial 10 bold')).place(x=50, y=35)
                    btn_ok = tk.Button(err_window, command=err_window.destroy, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
                    btn_ok.place(x=80, y=85)

            # Function that executes when OK button is clicked
            def on_click():
                window.destroy()

            # current value label
            ttk.Label(window, text='Input Gamma Value:', font=('Arial 10 bold')).place(x=150, y=35)
            
            text_box = tk.Entry(window, bg="white", textvariable=current_value, width=5, font=('Arial 13'))
            text_box.place(x=160, y=55)
            text_box.bind("<KeyRelease>", entry_changed)
            
            btn = tk.Button(window, command=on_click, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
            btn.place(x=165, y=85)
            
            window.wait_window(window)  # Wait for the window to be destroyed
            
            return current_value.get()
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            gamma = open_popup()
            # Creates the output image
            PL_img = Image.new('L', (self.width, self.height), 255)
            draw_PL = ImageDraw.Draw(PL_img)
            
            gray = self.get_grayscale_img() # transforms image to grayscale
            
            # Define the size of each color block
            block_size = 1

            # Draws the resulting pixels to an image
            for i, row in enumerate(gray):
                for j, color in enumerate(row):
                    x1 = j
                    y1 = i
                    x2 = x1 + 1
                    y2 = y1 + 1

                    c = 1
                    color = (int)(c*(color**gamma))
                    
                    # Clips pixel values between 0 and 255
                    if color < 0:
                        color = 0
                    elif color > 255:
                        color = 255

                    draw_PL.rectangle([x1, y1, x2, y2], fill=color)
                
            self.show_image(PL_img)
            self.curr_img = PL_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Image transformed through transformation function s=c*r^(gamma) where c = 1 and gamma = {gamma}", x=330, y=20, fill="white", font=("Arial", 9,))
    
    # Function that implements the averaging filter which blurs the image
    def average_filter(self):
        # Function that gets the average pixel value encompassed by an n x n mask
        def get_pixel_value(mask, neighbors):
            avg = 0
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    avg += neighbors[i][j]*mask[i][j]
            
            return int(avg)
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Initializes the n x n mask
            radius = self.n//2
            mask = [[1/(self.n*self.n) for i in range(self.n)] for j in range(self.n)]
            
            gray = self.get_grayscale_img() # transforms image to grayscale
                           
            blur_pixels = [row[:] for row in gray]
            
            padded_img = self.clamp_padding(radius, gray) # executes clamp padding
            
            # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
            neighbors = []
            for i in range(self.height):
                for j in range(self.width):
                    neighbors = self.get_neighbors(i+radius, j+radius, radius, padded_img)
                    blur_pixels[i][j] = get_pixel_value(mask, neighbors)
            
            # Creates the output image
            avg_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_avg_filtered = ImageDraw.Draw(avg_filtered_img)        
            self.drawImage(draw_avg_filtered, blur_pixels)        
                
            self.show_image(avg_filtered_img)
            self.curr_img = avg_filtered_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Averaging filter is applied to the image on a {self.n}x{self.n} mask", x=180, y=20, fill="white", font=("Arial", 9,))
    
    # Function that implements the unsharp masking       
    def unsharp_masking(self):
        # Function that gets the average pixel value encompassed by an n x n mask
        def get_pixel_value(mask, neighbors):
            avg = 0
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    avg += neighbors[i][j]*mask[i][j]
            
            return int(avg)
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Initializes the n x n mask
            radius = self.n//2
            mask = [[1/(self.n*self.n) for i in range(self.n)] for j in range(self.n)]
            
            gray_orig = self.get_grayscale_img() # transforms image to grayscale
            
            flat_gray_orig = [element for row in gray_orig for element in row]
            blur_pixels = [row[:] for row in gray_orig]
            
            padded_img = self.clamp_padding(radius, gray_orig) # executes clamp padding
            
            # Blurs the image using averaging filter
            neighbors = []
            for i in range(self.height):
                for j in range(self.width):
                    neighbors = self.get_neighbors(i+radius, j+radius, radius, padded_img)
                    blur_pixels[i][j] = get_pixel_value(mask, neighbors)
            
            flat_blur_pixels = [element for row in blur_pixels for element in row]
            
            # Obtains the mask
            unsharp_mask = []
            
            for orig_pixel, blur_pixel in zip(flat_gray_orig, flat_blur_pixels):
                unsharp_mask.append(orig_pixel - blur_pixel)
            
            img_result = []
            k=1
            
            # Adds the mask to the original image  
            for orig_pixel, value in zip(flat_gray_orig, unsharp_mask):
                img_result.append(orig_pixel + (k * value))
            
            
            # Creates the output image
            unsharp_masked_img = Image.new('L', (self.width, self.height), 255)
            draw_unsharp_masked = ImageDraw.Draw(unsharp_masked_img)
            self.drawImage1DArray(img_result, draw_unsharp_masked)
            self.show_image(unsharp_masked_img)
            self.curr_img = unsharp_masked_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Unsharp masking is applied to the image", x=180, y=20, fill="white", font=("Arial", 9,))
    
    # Function that implements the Highboost filtering        
    def highboost_filter(self):
        # Function that gets the average pixel value encompassed by an n x n mask
        def get_pixel_value(mask, neighbors):
            avg = 0
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    avg += neighbors[i][j]*mask[i][j]
                    
            return int(avg)       
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Initializes the n x n mask
            radius = self.n//2
            mask = [[1/(self.n*self.n) for i in range(self.n)] for j in range(self.n)]
            
            gray_orig = self.get_grayscale_img() # transforms image to grayscale
            
            flat_gray_orig = [element for row in gray_orig for element in row]
            blur_pixels = [row[:] for row in gray_orig]
            
            padded_img = self.clamp_padding(radius, gray_orig) # executes clamp padding
            
            # Blurs the image
            neighbors = []
            for i in range(self.height):
                for j in range(self.width):
                    neighbors = self.get_neighbors(i+radius, j+radius, radius, padded_img)
                    blur_pixels[i][j] = get_pixel_value(mask, neighbors)

            # Creates output image
            highpass_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_highboost = ImageDraw.Draw(highpass_filtered_img)
            
            flat_blur_pixels = [element for row in blur_pixels for element in row]
            
            highpass = []
            
            # Gets the highpass filtered image
            for orig_pixel, blur_pixel in zip(flat_gray_orig, flat_blur_pixels):
                highpass.append(orig_pixel - blur_pixel)
            
            img_result = []
            A = 3.5
            
            # Adds the highpass image to the original image multiplied by an amplification value A-1    
            for orig_pixel, value in zip(flat_gray_orig, highpass):
                img_result.append(int(((A-1)*orig_pixel) + value))
                    
            self.drawImage1DArray(img_result, draw_highboost)
                
            self.show_image(highpass_filtered_img)
            self.curr_img = highpass_filtered_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Highboost filter is applied to the image where the amplification parameter is 3.5", x=300, y=20, fill="white", font=("Arial", 9,))
    
    # Function that gets the neighboring pixels of a particular pixel in an image
    # It also saves the passed pixel
    def get_neighbors(self, row_index, column_index, radius, grid):
        neighbors = []
        for i in range(row_index-radius, row_index+radius+1):
            row = []
            for j in range(column_index-radius, column_index+radius+1):
                row.append(grid[i][j])  
                
            neighbors.append(row)
                
        return neighbors        
    
    # Function that implements the Median filter which reduces salt-and-pepper (impulse) noise in an image
    def median_filter(self):
        # Function that gets the median pixel value encompassed by an nxn mask
        def get_pixel_value(mask, neighbors):
            mdn = 0
            pxls_array = []
            
            # Gets the pixel values encompassed by a mask
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    pxls_array.append(neighbors[i][j])
                    
            n = len(pxls_array)      # get the length of the array
            pxls_array.sort() # sorts the pixel values from least to greatest

            # Finds the median of the pixel values encompassed by the mask
            if n % 2 == 0:
                mdn1 = pxls_array[n//2]
                mdn2 = pxls_array[n//2 - 1]
                mdn = (mdn1 + mdn2)/2
            else:
                mdn = pxls_array[n//2]

            return int(mdn)
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Initializes the n x n mask
            radius = self.n//2
            mask = [[1/(self.n*self.n) for i in range(self.n)] for j in range(self.n)]
            
            gray = self.get_grayscale_img() # transforms image to grayscale
            
            blur_pixels = [row[:] for row in gray] # copies gray pixel values to another array
            
            padded_img = self.clamp_padding(radius, gray) # executes clamp padding
            
            # Blurs the image
            neighbors = []
            for i in range(self.height):
                for j in range(self.width):
                    neighbors = self.get_neighbors(i+radius, j+radius, radius, padded_img)
                    blur_pixels[i][j] = get_pixel_value(mask, neighbors)
            
            # Creates output image
            mdn_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_mdn_filtered = ImageDraw.Draw(mdn_filtered_img)
            
            self.drawImage(draw_mdn_filtered, blur_pixels)  
                
            self.show_image(mdn_filtered_img)
            self.curr_img = mdn_filtered_img
            
            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Median filter is applied to the image on a {self.n}x{self.n} mask", x=180, y=20, fill="white", font=("Arial", 9,))

    # Function for Laplacian
    def laplacian_filter(self):
        # Function that gets the median pixel value encompassed by an nxn mask
        def get_pixel_value(mask, neighbors):
            lap_val = 0
          
            for i in range(len(mask)):
                for j in range(len(mask[i])):
                    lap_val += mask[i][j]*neighbors[i][j]
            
            # Clips the pixel values to be between 0 and 255
            if lap_val < 0:
                lap_val = 0
            elif lap_val > 255:
                lap_val = 255
            
            return int(lap_val)
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            # Initializes the n x n mask
            n = 3
            radius = n//2
            mask = [ [0,1,0] , [1,-4,1] , [0,1,0] ] # Sobel Magnitude Operator
            
            gray = self.get_grayscale_img() # transforms image to grayscale
            
            copy = [row[:] for row in gray] # copies gray pixel values to another array
            
            padded_img = self.clamp_padding(radius, gray) # executes clamp padding
            
            # Blurs the image
            neighbors = []
            for i in range(self.height):
                for j in range(self.width):
                    neighbors = self.get_neighbors(i+radius, j+radius, radius, padded_img)
                    copy[i][j] = get_pixel_value(mask, neighbors)
           
            # Creates output image
            lapla_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_lapla_filtered = ImageDraw.Draw(lapla_filtered_img)
            
            self.drawImage(draw_lapla_filtered, copy) # Draws each pixel value to an image
                
            self.show_image(lapla_filtered_img) # Shows image applied with laplacian filter
            self.curr_img = lapla_filtered_img 
            
            # Updates status bar
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Laplacian filter is applied to a {mask} kernel", x=180, y=20, fill="white", font=("Arial", 9,))
    
    # Function for Gradient filter using Sobel Operator
    def gradient_filter(self):
        if not self.pcx_image_data:
            print("No image data available.")
        else:
            # Initializes the n x n mask
            n = 3
            radius = n // 2

            # Function that implements gradient filtering by using the sobel operator
            def sobelOperator(image):
                Gx = [[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]]

                Gy = [[-1, -2, -1],
                      [0, 0, 0],
                      [1, 2, 1]]

                rows = len(image)
                cols = len(image[0])
                mag = [[0] * (cols-2) for _ in range(rows-2)]  # Initialize output differential/gradient

                r = 0
                for i in range(1, rows-1):
                    c = 0
                    for j in range(1, cols-1):
                        S1 = sum(image[(i-1) + m][(j-1) + n] * Gx[m][n] for m in range(3) for n in range(3))
                        S2 = sum(image[(i-1) + m][(j-1) + n] * Gy[m][n] for m in range(3) for n in range(3))
                        mag[r][c] = int(((S1 ** 2) + (S2 ** 2)) ** 0.5)
                        c+=1
                    r+=1

                # Clips the pixel values to be between 0 and 255
                for i in range(rows-2):
                    for j in range(cols-2):
                        if mag[i][j] < 0:
                            mag[i][j] = 0
                        elif mag[i][j] > 255:
                            mag[i][j] = 255

                return mag

            gray = self.get_grayscale_img() # transforms image to grayscale

            padded_img = self.clamp_padding(radius, gray) # implements clamp padding

            # Apply Sobel operator to the grayscale image with clamp padding
            sobel_result = sobelOperator(padded_img)

            # Creates output image
            grdn_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_grdn_filtered = ImageDraw.Draw(grdn_filtered_img)

            self.drawImage(draw_grdn_filtered, sobel_result) 

            self.show_image(grdn_filtered_img)
            self.curr_img = grdn_filtered_img

            # Updates status
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Gradient filter using the Sobel edge detection is applied to the image", x=180, y=20, fill="white", font=("Arial", 9,))

    # Function that implements clamp padding
    # This is to allow the border side of the image to be accounted with the operation being done
    # For instance, if an image is 
    # [1, 2, 3]
    # [1, 4, 5]
    # [1, 6, 7]
    # Then clamp padding will turn it into
    # [1, 1, 2, 3, 3]
    # [1, 1, 2, 3, 3]
    # [1, 1, 4, 5, 5]
    # [1, 1, 6, 7, 7]
    # [1, 1, 6, 7, 7]
    def clamp_padding(self, radius, gray):
        # Initializes rows and columns after padding
        padded_rows = self.height + 2*radius
        padded_cols = self.width + 2*radius
        
        # Create the padded array and implement clamp padding
        clamp_padded_img = [[0 for _ in range(padded_cols)] for _ in range(padded_rows)]

        # Copy the contents of the original array to the center of the padded array
        for i in range(self.height):
            for j in range(self.width):
                # Use clamp padding to set border values
                padded_i = i + radius
                padded_j = j + radius
                clamp_padded_img[padded_i][padded_j] = gray[i][j]

        # Fill in the border values using clamp padding
        for i in range(padded_rows):
            for j in range(padded_cols):
                if i < radius:
                    # Clamp padding for the top border
                    padded_i = radius
                elif i >= self.height + radius:
                    # Clamp padding for the bottom border
                    padded_i = self.height + radius - 1
                else:
                    padded_i = i

                if j < radius:
                    # Clamp padding for the left border
                    padded_j = radius
                elif j >= self.width + radius:
                    # Clamp padding for the right border
                    padded_j = self.width + radius - 1
                else:
                    padded_j = j

                clamp_padded_img[i][j] = gray[padded_i - radius][padded_j - radius]
                
        return clamp_padded_img

    # Function that closes the image file being displayed
    # It removes all references of the image, information, and applied operations to its respective variables and widgets
    # It also reverts the program back to its state when it was first opened    
    def close_img(self):
        
        self.orig_img = None
        self.curr_img = None
        self.red_channel = []
        self.green_channel = []
        self.blue_channel = []
        self.pcx_image_data = []
        
        # Reverts right sidebar to its original form
        self.rightsidebar.destroy()
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=2, sticky="nsew")
        
        # Removes image in the image panel
        self.image_label.destroy()
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=1, sticky="nsew")

        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar("Status: Image closed", x=120, y=20, fill="white", font=("Arial", 9,))
                    
if __name__ == "__main__":
    app = App()
    app.mainloop()