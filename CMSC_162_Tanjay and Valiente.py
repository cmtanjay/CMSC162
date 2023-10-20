from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
import os

# This is the class constructor for the Image Processing App
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.orig_img = None
        self.red_channel = []
        self.green_channel = []
        self.blue_channel = []

        # Configures the app window
        self.title("Image Processor")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Gets the screen width and height
        screen_width = self.winfo_screenwidth() - 100
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

        # Configures open PCX file button
        btn_open_pcx = tk.Button(self.topbar, text="Open PCX", command=self.open_pcx_file,font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_open_pcx.grid(row=1, column=1, sticky="ew", padx=5, pady=10)

        # Configures open image file button
        btn_open_img = tk.Button(self.topbar, text="Open Image", command=self.open_img_file, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_open_img.grid(row=1, column=2, sticky="ew", padx=5, pady=10)

        # Configures close file button
        btn_close_file = tk.Button(self.topbar,  text="Close File", command=self.close_img, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_close_file.grid(row=1, column=3, sticky="ew", padx=5, pady=10)
        
        # Configures orig image button
        btn_orig_img = tk.Button(self.topbar,  text="Original Image", command=lambda: self.show_image(self.orig_img), font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_orig_img.grid(row=1, column=4, sticky="ew", padx=5, pady=10)
        
        # Configures red channel button
        btn_red_channel = tk.Button(self.topbar,  text="Red Channel", command=lambda: self.show_channel(self.red_channel, "red"), font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_red_channel.grid(row=1, column=5, sticky="ew", padx=5, pady=10)
        
        # Configures green channel button
        btn_green_channel = tk.Button(self.topbar,  text="Green Channel", command=lambda: self.show_channel(self.green_channel, "green"), font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_green_channel.grid(row=1, column=6, sticky="ew", padx=5, pady=10)
        
        # Configures blue channel button
        btn_blue_channel = tk.Button(self.topbar,  text="Blue Channel", command=lambda: self.show_channel(self.blue_channel, "blue"), font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_blue_channel.grid(row=1, column=7, sticky="ew", padx=5, pady=10)
        
        # Configures grayscale button
        btn_grayscale = tk.Button(self.topbar,  text="Grayscale", command=self.grayscale_transform, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_grayscale.grid(row=1, column=8, sticky="ew", padx=5, pady=10)
        
        # Configures negative button
        btn_grayscale = tk.Button(self.topbar,  text="Negative", command=self.negative_transform, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_grayscale.grid(row=1, column=9, sticky="ew", padx=5, pady=10)
        
        # Configures B/W button
        btn_grayscale = tk.Button(self.topbar,  text="B/W", command=self.BW_manual_thresholding, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_grayscale.grid(row=1, column=10, sticky="ew", padx=5, pady=10)
        
        # Configures Power-Law button
        btn_grayscale = tk.Button(self.topbar,  text="Power-Law", command=self.Power_law_transform, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_grayscale.grid(row=1, column=11, sticky="ew", padx=5, pady=10)
        
        # Configures Power-Law button
        btn_avg_filter = tk.Button(self.sidebar,  text="Ave Filter", command=self.average_filter, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_avg_filter.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        
        btn_unsharp = tk.Button(self.sidebar,  text="Unsharp", command=self.unsharp_masking, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_unsharp.grid(row=1, column=1, sticky="ew", padx=5, pady=10)
        
        btn_highboost = tk.Button(self.sidebar,  text="High-boost", command=self.highboost_filter, font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn_highboost.grid(row=2, column=1, sticky="ew", padx=5, pady=10)
    
    # This is the function that opens the image file
    def open_img_file(self):
        filepath = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])
        if not filepath:
            return
        
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

            self.title(f"Image Viewer - {image}")
            
    # Function that opens a PCX file
    def open_pcx_file(self):
        
        filepath = askopenfilename(filetypes=[("PCX Files", "*.pcx")])
        if not filepath:
            print("Not a PCX file")
                     
            return
        
        with open(filepath, "rb") as file:
        
            self.add_text_to_statusbar("Status: PCX Image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
            
            self.header = file.read(128)
            
            file.seek(0)
            size = len(file.read())
            
            # pixel_data_size = file.seek(128,2) - 769
            # print(pixel_data_size)
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
                content = file.read()
                #print(content)
                
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
                
                # Create a blank image with a white background
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
                
                self.get_img_channels()
                
                self.orig_img = img_pcx 
                self.show_image(img_pcx)    
                
                # Create a blank image with a white background
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

                # Create the canvas in the right sidebar
                self.create_right_sidebar_canvas()

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

                self.display_image_on_right_sidebar(image_tk_palette)
    
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
    def create_right_sidebar_canvas(self):
        # Create the canvas in the right sidebar
        self.canvas = tk.Canvas(self.rightsidebar, width=250, height=300, bg="#2B2B2B", highlightthickness=0)
        self.canvas.grid(row=1, column=2, sticky="nsew")

    # Function to add text onto the canvas of the right side bar
    def add_text_to_right_sidebar(self, text, x, y, fill, font):
        # Use the previously created canvas
        self.canvas.create_text(x, y, text=text, fill=fill, font=font)
    
    # Function to display the generated color palette to the right side bar
    def display_image_on_right_sidebar(self, image_tk):
        canvas = tk.Canvas(self.rightsidebar, width=256, height=200, bg="#2B2B2B", highlightthickness=0)
        canvas.grid(row=2, column=2, sticky="nsew")

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
                
                if(string == "red"):
                    draw_channel_img.rectangle([x1, y1, x2, y2], fill=(rgb[0], 0, 0))
                elif(string == "green"):
                    draw_channel_img.rectangle([x1, y1, x2, y2], fill=(0, rgb[1], 0))
                elif(string == "blue"):
                    draw_channel_img.rectangle([x1, y1, x2, y2], fill=(0, 0, rgb[2]))
                
            self.show_image(channel_img)
            self.show_hist(channel, string)
    
    # Function that transforms the RGB PCX file to Grayscale
    def grayscale_transform(self):
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            grayscale_img = Image.new('L', (self.width, self.height), 255)
            draw_grayscale = ImageDraw.Draw(grayscale_img)
            
            gray = []
            
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
                gray.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                    
                draw_grayscale.rectangle([x1, y1, x2, y2], fill=(gray[i]))
                
            self.show_image(grayscale_img)
            
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
            negative_img = Image.new('L', (self.width, self.height), 255)
            draw_negative = ImageDraw.Draw(negative_img)
            
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
                s = (int)((rgb[0]+rgb[1]+rgb[2])/3)
                    
                draw_negative.rectangle([x1, y1, x2, y2], fill=(255 - s))
                
            self.show_image(negative_img)
            
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
            
            current_value = tk.IntVar()
            threshold = tk.IntVar()
            
            def entry_changed(event):
                value = text_box.get()  # Get the value from the entry box
                if value.isdigit():  # Check if the value is a valid integer
                    current_value.set(int(value))  # Set the slider value to the entry value
                else:
                    # Handle invalid input (e.g., non-integer values)
                    pass

            def slider_changed(*args):
                value = current_value.get()
                text_box.delete(0, tk.END)  # Clear the entry box
                text_box.insert(0, value)

            def on_click():
                value = current_value.get()
                threshold.set(value)
                window.destroy()

            # label for the slider
            ttk.Label(window, text='Slider:', font=('Arial 10 bold')).place(x=15, y=10)

            #  slider
            ttk.Scale(window, from_= 0, to = 255, orient='horizontal', command=slider_changed, variable=current_value, length=310).place(x=65, y=10)

            # current value label
            ttk.Label(window, text='Current Value:', font=('Arial 10 bold')).place(x=150, y=35)
            
            text_box = tk.Entry(window, bg="white", width=5, font=('Arial 13'))
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
            BW_img = Image.new('L', (self.width, self.height), 255)
            draw_BW = ImageDraw.Draw(BW_img)
            
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
                s = (int)((rgb[0]+rgb[1]+rgb[2])/3)
                
                if(s <= threshold):
                    s = 0
                else:
                    s = 255
                    
                draw_BW.rectangle([x1, y1, x2, y2], fill=s)
                
            self.show_image(BW_img)
            
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

            def on_click():
                window.destroy()

            # current value label
            ttk.Label(window, text='Current Gamma Value:', font=('Arial 10 bold')).place(x=150, y=35)
            
            text_box = tk.Entry(window, bg="white", textvariable=current_value, width=5, font=('Arial 13'))
            text_box.place(x=160, y=55)
            
            btn = tk.Button(window, command=on_click, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
            btn.place(x=165, y=85)
            
            window.wait_window(window)  # Wait for the window to be destroyed
            
            return current_value.get()
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            gamma = open_popup()
            PL_img = Image.new('L', (self.width, self.height), 255)
            draw_PL = ImageDraw.Draw(PL_img)
            
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
                r = (int)((rgb[0]+rgb[1]+rgb[2])/3)
                c = 1
                
                s = (int)(c*(r**gamma))
                #print(f"{r} => {s} => {(r**gamma)}")
                    
                draw_PL.rectangle([x1, y1, x2, y2], fill=s)
                
            self.show_image(PL_img)
            
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Image transformed through transformation function s=c*r^(gamma) where c = 1 and gamma = {gamma}", x=330, y=20, fill="white", font=("Arial", 9,))
    
    # Function that implements the averaging filter which blurs the image
    def average_filter(self):
        # Function that gets the average pixel value encompassed by an nxn mask
        def get_pixel_value(mask, neighbors):
            avg = 0
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    avg += neighbors[i][j]*mask[i][j]
            
            return int(avg)
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            avg_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_avg_filtered = ImageDraw.Draw(avg_filtered_img)
            
            # Initializes the n x n mask
            n = 3
            radius = n//2
            mask = [[1/(n*n) for i in range(n)] for j in range(n)]
            
            gray = []
            row = []

            # Transforms image to grayscale
            for i, color in enumerate(self.pcx_image_data):
                rgb = list(self.palette[color])
                if i % self.width == 0:
                    if i == 0:
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                    else:
                        gray.append(row)
                        row = []
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                else:
                    if i == len(self.pcx_image_data)-1:
                        gray.append(row)
                    else:
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
            
            copy = gray
            
            # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
            neighbors = []
            for i in range(radius, self.height-radius-1):
                for j in range(radius, self.width-radius-1):
                    neighbors = self.get_neighbors(i, j, radius, gray)
                    copy[i][j] = get_pixel_value(mask, neighbors)
            
            copy2 = [element for row in copy for element in row]
                    
            block_size = 1
            
            # Draw the colored blocks on the image
            for i, color in enumerate(copy2):
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
                    
                draw_avg_filtered.rectangle([x1, y1, x2, y2], fill=color)
                
            self.show_image(avg_filtered_img)
            
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Averaging filter is applied to the image on a {n}x{n} mask", x=180, y=20, fill="white", font=("Arial", 9,))
    
    # Function that implements the unsharp masking       
    def unsharp_masking(self):
        # Function that gets the average pixel value encompassed by an nxn mask
        def get_pixel_value(mask, neighbors):
            avg = 0
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    avg += neighbors[i][j]*mask[i][j]
            
            return int(avg)
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            unsharp_masked_img = Image.new('L', (self.width, self.height), 255)
            draw_avg_filtered = ImageDraw.Draw(unsharp_masked_img)
            
            # Initializes the n x n mask
            n = 3
            radius = n//2
            mask = [[1/(n*n) for i in range(n)] for j in range(n)]
            
            gray_orig = []
            row = []

            # Transforms image to grayscale
            for i, color in enumerate(self.pcx_image_data):
                rgb = list(self.palette[color])
                if i % self.width == 0:
                    if i == 0:
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                    else:
                        gray_orig.append(row)
                        row = []
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                else:
                    if i == len(self.pcx_image_data)-1:
                        gray_orig.append(row)
                    else:
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
            
            flat_gray_orig = [element for row in gray_orig for element in row]
            blur_pixels = gray_orig
            
            # Blurs the image
            neighbors = []
            for i in range(radius, self.height-radius-1):
                for j in range(radius, self.width-radius-1):
                    neighbors = self.get_neighbors(i, j, radius, gray_orig)
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
                    
            block_size = 1
            
            # Draw the colored blocks on the image
            for i, color in enumerate(img_result):
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
                    
                draw_avg_filtered.rectangle([x1, y1, x2, y2], fill=color)
                
            self.show_image(unsharp_masked_img)
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Unsharp masking is applied to the image", x=180, y=20, fill="white", font=("Arial", 9,))
    
    # Function that implements the Highboost filtering        
    def highboost_filter(self):
        # Function that gets the average pixel value encompassed by an nxn mask
        def get_pixel_value(mask, neighbors):
            avg = 0
            for i in range(len(mask)):
                for j in range(len(mask[0])):
                    avg += neighbors[i][j]*mask[i][j]
                    
            return int(avg)       
        
        if not self.pcx_image_data:
            print("WALAAAAAA")
        else:
            highpass_filtered_img = Image.new('L', (self.width, self.height), 255)
            draw_avg_filtered = ImageDraw.Draw(highpass_filtered_img)
            
            # Initializes the n x n mask
            n = 3
            radius = n//2
            mask = [[1/(n*n) for i in range(n)] for j in range(n)]
            
            gray_orig = []
            row = []

            # Transforms image to grayscale
            for i, color in enumerate(self.pcx_image_data):
                rgb = list(self.palette[color])
                if i % self.width == 0:
                    if i == 0:
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                    else:
                        gray_orig.append(row)
                        row = []
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
                else:
                    if i == len(self.pcx_image_data)-1:
                        gray_orig.append(row)
                    else:
                        row.append((int)((rgb[0]+rgb[1]+rgb[2])/3))
            
            flat_gray_orig = [element for row in gray_orig for element in row]
            blur_pixels = gray_orig
            
            # Gets lowpass filtered version of image
            neighbors = []
            for i in range(radius, self.height-radius-1):
                for j in range(radius, self.width-radius-1):
                    neighbors = self.get_neighbors(i, j, radius, gray_orig)
                    blur_pixels[i][j] = get_pixel_value(mask, neighbors)
            
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
                    
            block_size = 1
            
            # Draw the colored blocks on the image
            for i, color in enumerate(img_result):
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
                
                draw_avg_filtered.rectangle([x1, y1, x2, y2], fill=color)
                
            self.show_image(highpass_filtered_img)
            
            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()
            self.add_text_to_statusbar(f"Status: Highboost filter is applied to the image where the amplification parameter is 3.5", x=300, y=20, fill="white", font=("Arial", 9,))
    
    # Function that gets the neighboring pixels of a particular pixel in an image
    def get_neighbors(self, row_index, column_index, radius, grid):
        neighbors = []
        for i in range(row_index-radius, row_index+radius+1):
            row = []
            for j in range(column_index-radius, column_index+radius+1):
                row.append(grid[i][j])   
            neighbors.append(row)
                
        return neighbors        
    
    # Function that closes the image file being displayed    
    def close_img(self):
        
        self.orig_img = None
        self.red_channel = []
        self.green_channel = []
        self.blue_channel = []
        self.pcx_image_data = []

        print("close")
        
        
        self.rightsidebar.destroy()
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=2, sticky="nsew")
        
        self.image_label.destroy()
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=1, sticky="nsew")

        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar("Status: Image closed", x=120, y=20, fill="white", font=("Arial", 9,))
                    
if __name__ == "__main__":
    app = App()
    app.mainloop()
