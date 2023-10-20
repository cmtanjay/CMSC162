from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
from tkinter import ttk
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import filedialog
from image_processor import *
from tkinter import filedialog

class App(tk.Tk):
    # Create an instance of the ImageProcessor class
    processor = ImageProcessor()    

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
        screen_width = self.winfo_screenwidth() - 20
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

    # def configure_button(self, text, command, row, column):
    #     btn = tk.Button(self.topbar, text=text, command=command, font=("Arial", 10), background="#313E4E", foreground="white", relief="ridge", borderwidth=2)
    #     btn.grid(row=row, column=column, sticky="ew", padx=5, pady=10)

    #     # To use the function for each button:
    #     self.configure_button("Open PCX", self.open_pcx_file, 1, 1)
    #     self.configure_button("Open Image", self.open_img_file, 1, 2)
    #     self.configure_button("Close File", self.close_img, 1, 3)
    #     self.configure_button("Original Image", lambda: self.show_image(self.orig_img), 1, 4)
    #     self.configure_button("Red Channel", lambda: self.show_channel(self.red_channel, "red"), 1, 5)
    #     self.configure_button("Green Channel", lambda: self.show_channel(self.green_channel, "green"), 1, 6)
    #     self.configure_button("Blue Channel", lambda: self.show_channel(self.blue_channel, "blue"), 1, 7)
    #     self.configure_button("Grayscale", self.grayscale_transform, 1, 8)
    #     self.configure_button("Negative", self.negative_transform, 1, 9)
    #     self.configure_button("B/W", self.BW_manual_thresholding, 1, 10)
    #     self.configure_button("Power-Law", self.Power_law_transform, 1, 11)
        
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
    
    # Functions for opening, closing, and processing images
    def show_image(self, image):
        self.processor.show_image(self,image)

    # Functions for opening, closing, and processing images
    def open_pcx_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PCX files", "*.pcx")])
        if file_path:
            self.orig_img = self.processor.open_pcx_file(file_path)
            
            self.add_text_to_statusbar(f"Status: Image opened from {file_path}")

            

    def open_img_file(self):
        
        file_path = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])
        if file_path:
            self.orig_img = self.processor.open_img_file()  # Call the method from ImageProcessor
            self.show_image(self.orig_img)

            self.statusbar.destroy()
            self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
            self.statusbar.grid(row=2, columnspan=3, sticky="ew")
            self.create_statusbar_canvas()

            self.rightsidebar.destroy()
            self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
            self.rightsidebar.grid(row=1, column=2, sticky="nsew")

            # Extract the filename from the full filepath
            filename = os.path.basename(file_path)
            self.add_text_to_statusbar(f"Status: {filename} loaded", x=120, y=20, fill="white", font=("Arial", 9,))

    def close_img(self):
        self.orig_img = None
        self.show_image(self.orig_img)
        self.add_text_to_statusbar("Status: No image loaded")

    def grayscale_transform(self):
        if self.orig_img is not None:
            self.orig_img = self.processor.grayscale(self.orig_img)
            self.show_image(self.orig_img)
            self.add_text_to_statusbar("Status: Grayscale transformation applied")

    def negative_transform(self):
        if self.orig_img is not None:
            self.orig_img = self.processor.negative(self.orig_img)
            self.show_image(self.orig_img)
            self.add_text_to_statusbar("Status: Negative transformation applied")

    def BW_manual_thresholding(self):
        if self.orig_img is not None:
            self.orig_img = self.processor.BW_manual_thresholding(self.orig_img, threshold=128)
            self.show_image(self.orig_img)
            self.add_text_to_statusbar("Status: B/W manual thresholding applied")

    def Power_law_transform(self):
        if self.orig_img is not None:
            self.orig_img = self.processor.Power_law(self.orig_img, gamma=1.5)
            self.show_image(self.orig_img)
            self.add_text_to_statusbar("Status: Power-Law transformation applied")

if __name__ == "__main__":
    app = App()
    
    app.mainloop()