# This is where the main UI components of the app is implemented.
from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
from tkinter import ttk
from customtkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import matplotlib.pyplot as plt
import numpy as np
import os

import variables
from img_ops import *
from point_processing import *
from img_enhancement import *
from img_degradation import *
from img_restoration import *
from img_compression import *
from optical_flow import *
from video_ops import *
from img_seq_ops import *

from ToolTip import CreateToolTip

import cv2

# This is the class constructor for the Image Processing App
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configures the app window
        self.title("iMage and Video Processor")
        self.configure(bg="#242424")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.progress_var = tk.DoubleVar()

        # Gets the screen width and height
        screen_width = self.winfo_screenwidth() - 10
        screen_height = self.winfo_screenheight() - 100

        # Sets window size with screen dimension
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Configures the top bar of the App GUI
        self.topbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=1, relief="solid")
        self.topbar.grid(row=0, columnspan=4, sticky="ew") 
        
        # Configures the side bar of the App GUI
        self.sidebar = tk.Frame(self, width=100, bg="#2B2B2B")
        self.sidebar.grid(row=1, column=0, rowspan=4, sticky="nsew")
        
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        
        # Configures the right side bar of the App GUI
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=3, sticky="nsew")
        self.rightsidebar.grid_columnconfigure(0, minsize=125)
        self.rightsidebar.grid_columnconfigure(1, minsize=125)
        
        # Configures the status bar of the App GUI
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=5, columnspan=4, sticky="ew")
        
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
        self.image_label.grid(row=1, column=2, sticky="nsew")

        img_pcx = Image.open("assets\pcx.png")
        img_pcx = img_pcx.resize((35,35))
        icon_pcx = ImageTk.PhotoImage(img_pcx)
    
        # Configures open PCX file button
        btn_open_pcx = tk.Button(self.topbar, image=icon_pcx, command=lambda: open_pcx_file(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_open_pcx.photo = icon_pcx
        btn_open_pcx.grid(row=1, column=1, sticky="ew")
        CreateToolTip(btn_open_pcx, "Open PCX")

        img = Image.open("assets\img.png")
        img = img.resize((35,35))
        icon_img = ImageTk.PhotoImage(img)

        # Configures open image file button
        btn_open_img = tk.Button(self.topbar, image=icon_img, command=lambda: open_img_file(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_open_img.photo = icon_img
        btn_open_img.grid(row=1, column=2, sticky="ew")
        CreateToolTip(btn_open_img, "Open Image")
        
        img_vid = Image.open("assets\\video.png")
        img_vid = img_vid.resize((35,35))
        icon_vid = ImageTk.PhotoImage(img_vid)

        # Configures close file button
        btn_vid_file = tk.Button(self.topbar, image=icon_vid, command=lambda: open_vid_file(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_vid_file.photo = icon_vid
        btn_vid_file.grid(row=1, column=3, sticky="ew")
        CreateToolTip(btn_vid_file, "Open Video File")
        
        img_zip = Image.open("assets\directory.png")
        img_zip = img_zip.resize((35,35))
        icon_zip = ImageTk.PhotoImage(img_zip)

        # Configures close file button
        btn_zip_file = tk.Button(self.topbar, image=icon_zip, command=lambda: open_zip_file(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_zip_file.photo = icon_zip
        btn_zip_file.grid(row=1, column=4, sticky="ew")
        CreateToolTip(btn_zip_file, "Open Image Sequence File")

        img_close = Image.open("assets\close.png")
        img_close = img_close.resize((35,35))
        icon_close = ImageTk.PhotoImage(img_close)

        # Configures close file button
        btn_close_file = tk.Button(self.topbar, image=icon_close, command=self.close_img, background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_close_file.photo = icon_close
        btn_close_file.grid(row=1, column=5, sticky="ew")
        CreateToolTip(btn_close_file, "Close File")
        
        img_orig_img = Image.open("assets\\revert.png")
        img_orig_img = img_orig_img.resize((35,35))
        icon_orig_img = ImageTk.PhotoImage(img_orig_img)

        # Configures orig image button
        btn_orig_img = tk.Button(self.topbar, image=icon_orig_img, command=lambda: show_image(self, variables.orig_img, "original"), background="#2F333A", relief="ridge", borderwidth=0)
        btn_orig_img.photo = icon_orig_img
        btn_orig_img.grid(row=1, column=6, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_orig_img, "Revert to Original Image")
        
        img_hist = Image.open("assets\histogram.png")
        img_hist = img_hist.resize((40,40))
        icon_hist = ImageTk.PhotoImage(img_hist)

        # Configures orig image button
        self.btn_hist = tk.Button(self.topbar, image=icon_hist, background="#2F333A", relief="ridge", borderwidth=0, state="disabled")
        self.btn_hist.photo = icon_hist
        self.btn_hist.grid(row=1, column=7, sticky="ew", padx=5, pady=10)
        CreateToolTip(self.btn_hist, "Show Histogram")
        
        img_channel = Image.open("assets\\channel.png")
        img_channel = img_channel.resize((30,30))
        icon_channel = ImageTk.PhotoImage(img_channel)
        
        # Configures averaging filter button
        btn_channel = tk.Button(self.sidebar, image=icon_channel, command=self.channels, background="#2B2B2B", foreground="white", relief="ridge", borderwidth=2)
        btn_channel.photo = icon_channel
        btn_channel.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_channel, "Channels")
        
        img_mdn = Image.open("assets\point.png")
        img_mdn = img_mdn.resize((30,30))
        icon_mdn = ImageTk.PhotoImage(img_mdn)
        
        btn_point_process = tk.Button(self.sidebar, image=icon_mdn, command=self.point_processing, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_point_process.photo = icon_mdn
        btn_point_process.grid(row=1, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_point_process, "Point-Processing Methods")
        
        img_highpass = Image.open("assets\enhance.png")
        img_highpass = img_highpass.resize((30,30))
        icon_highpass = ImageTk.PhotoImage(img_highpass)
        
        btn_enhancement = tk.Button(self.sidebar, image=icon_highpass, command=self.img_enhancement, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_enhancement.photo = icon_highpass
        btn_enhancement.grid(row=2, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_enhancement, "Image Enhancement")

        img_unsharp = Image.open("assets\degrade.png")
        img_unsharp = img_unsharp.resize((30,30))
        icon_unsharp = ImageTk.PhotoImage(img_unsharp)

        btn_degradation = tk.Button(self.sidebar, image=icon_unsharp, command=self.img_degradation, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_degradation.photo = icon_unsharp
        btn_degradation.grid(row=3, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_degradation, "Image Degradation")

        img_restoration = Image.open("assets\\restore.png")
        img_restoration = img_restoration.resize((30,30))
        icon_restoration = ImageTk.PhotoImage(img_restoration)

        btn_restoration = tk.Button(self.sidebar, image=icon_restoration, command=self.img_restoration, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_restoration.photo = icon_restoration
        btn_restoration.grid(row=4, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_restoration, "Image Restoration")

        img_compression = Image.open("assets\compress.png")
        img_compression = img_compression.resize((30,30))
        icon_compression = ImageTk.PhotoImage(img_compression)
        
        btn_compression = tk.Button(self.sidebar, image=icon_compression, command=self.img_compression, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_compression.photo = icon_compression
        btn_compression.grid(row=5, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_compression, "Image Compression")
        
        img_opticalFlow = Image.open("assets\optical-flow.png")
        img_opticalFlow = img_opticalFlow.resize((30,30))
        icon_opticalFlow = ImageTk.PhotoImage(img_opticalFlow)
        
        btn_opticalFlow = tk.Button(self.sidebar, image=icon_opticalFlow, command=self.opticalFlow, background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_opticalFlow.photo = icon_opticalFlow
        btn_opticalFlow.grid(row=6, column=1, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_opticalFlow, "Optical Flow")

    # Function that allows the user to save an image in the program
    def save_file_as(self, event=None):
        file = asksaveasfilename(defaultextension=".pcx", filetypes=[("PCX Files", "*.pcx")])
        print(variables.curr_img)
        variables.curr_img = variables.curr_img.save(file)

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
    
    # Function that contains the buttons for displaying the different color channels of an image.
    def channels(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, sticky="new")
        
        # Configures red channel button
        btn_red_channel = tk.Button(self.opsbar,  text="     ", command=lambda: show_channel(self, variables.red_channel, "red"), font=("Arial", 10), background="#FF0000", foreground="white",relief="ridge", borderwidth=2)
        btn_red_channel.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_red_channel, "Red Channel")
        
        # Configures green channel button
        btn_green_channel = tk.Button(self.opsbar,  text="     ", command=lambda: show_channel(self, variables.green_channel, "green"), font=("Arial", 10), background="#00FF00", foreground="white",relief="ridge", borderwidth=2)
        btn_green_channel.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_green_channel, "Green Channel")
        
        # Configures blue channel button
        btn_blue_channel = tk.Button(self.opsbar,  text="     ", command=lambda: show_channel(self, variables.blue_channel, "blue"), font=("Arial", 10), background="#0000FF", foreground="white",relief="ridge", borderwidth=2)
        btn_blue_channel.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_blue_channel, "Blue Channel")
        
    # Function that contains the buttons for the different point processing techniques of the application
    def point_processing(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, pady=(65, 0), sticky="new")
        
        img_grayscale = Image.open("assets\grayscale.png")
        img_grayscale = img_grayscale.resize((35,35))
        icon_grayscale = ImageTk.PhotoImage(img_grayscale)
        
        # Configures grayscale button
        self.btn_grayscale = tk.Button(self.opsbar, image=icon_grayscale, command=lambda: grayscale_transform(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        self.btn_grayscale.photo = icon_grayscale
        self.btn_grayscale.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(self.btn_grayscale, "Grayscale Transform (R+G+B)/3")
        
        img_negative = Image.open("assets\\negative.png")
        img_negative = img_negative.resize((35,35))
        icon_negative = ImageTk.PhotoImage(img_negative)
        
        # Configures negative button
        btn_negative = tk.Button(self.opsbar, image=icon_negative, command=lambda: negative_transform(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_negative.photo = icon_negative
        btn_negative.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_negative, "Negative")
        
        img_BW = Image.open("assets\BW.png")
        img_BW = img_BW.resize((35,35))
        icon_BW = ImageTk.PhotoImage(img_BW)
        
        # Configures B/W button
        btn_BW = tk.Button(self.opsbar, image=icon_BW, command=lambda: BW_manual_thresholding(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_BW.photo = icon_BW
        btn_BW.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_BW, "Black and White w/ Thresholding")
        
        img_gamma = Image.open("assets\gamma.png")
        img_gamma = img_gamma.resize((35,35))
        icon_gamma = ImageTk.PhotoImage(img_gamma)
        
        # Configures Power-Law button
        btn_gamma = tk.Button(self.opsbar, image=icon_gamma, command=lambda: Power_law_transform(self), background="#2F333A", foreground="white",relief="ridge", borderwidth=0)
        btn_gamma.photo = icon_gamma
        btn_gamma.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_gamma, "Power-Law (Gamma) Transform")
    
    # Function that contains the buttons for the different image enhancement techniques of the application
    def img_enhancement(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, pady=(120, 0), sticky="new")
        
        # Configures averaging filter button
        img_avg = Image.open("assets\\avg.png")
        img_avg = img_avg.resize((30,30))
        icon_avg = ImageTk.PhotoImage(img_avg)
        
        btn_avg_filter = tk.Button(self.opsbar, image=icon_avg, command=lambda: average_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_avg_filter.photo = icon_avg
        btn_avg_filter.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_avg_filter, "Averaging Filter")
        
        # Configures Median filter button
        img_mdn = Image.open("assets\median.png")
        img_mdn = img_mdn.resize((30,30))
        icon_mdn = ImageTk.PhotoImage(img_mdn)
        
        btn_median = tk.Button(self.opsbar, image=icon_mdn, command=lambda: median_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_median.photo = icon_mdn
        btn_median.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_median, "Median Filter")
        
        # Configures Laplacian filter button
        img_highpass = Image.open("assets\highpass.png")
        img_highpass = img_highpass.resize((30,30))
        icon_highpass = ImageTk.PhotoImage(img_highpass)
        
        btn_laplacian = tk.Button(self.opsbar, image=icon_highpass, command=lambda: laplacian_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_laplacian.photo = icon_highpass
        btn_laplacian.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_laplacian, "Highpass Filter (Laplacian Operator)")
        
        # Configures Unsharp Masking button
        img_unsharp = Image.open("assets\mask.png")
        img_unsharp = img_unsharp.resize((30,30))
        icon_unsharp = ImageTk.PhotoImage(img_unsharp)

        btn_unsharp = tk.Button(self.opsbar, image=icon_unsharp, command=lambda: unsharp_masking(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_unsharp.photo = icon_unsharp
        btn_unsharp.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_unsharp, "Unsharp Masking")

        # Configures Highboost Filter button
        img_highboost = Image.open("assets\highboost.png")
        img_highboost = img_highboost.resize((30,30))
        icon_highboost = ImageTk.PhotoImage(img_highboost)

        btn_highboost = tk.Button(self.opsbar, image=icon_highboost, command=lambda: highboost_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_highboost.photo = icon_highboost
        btn_highboost.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_highboost, "Highboost Filtering")

        # Configures Gradient Filter button
        img_gradient = Image.open("assets\gradient.png")
        img_gradient = img_gradient.resize((30,30))
        icon_gradient = ImageTk.PhotoImage(img_gradient)
        
        btn_gradient = tk.Button(self.opsbar, image=icon_gradient, command=lambda: gradient_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_gradient.photo = icon_gradient
        btn_gradient.grid(row=5, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_gradient, "Gradient: Sobel Magnitude Operator")
    
    # Function that contains the buttons for the different image degradation techniques of the application
    def img_degradation(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, pady=(175, 0), sticky="new")
        
        # Configures Salt and Pepper Noise button
        img_sp = Image.open("assets\salt.png")
        img_sp = img_sp.resize((35,35))
        icon_sp = ImageTk.PhotoImage(img_sp)
        
        btn_sp = tk.Button(self.opsbar, image=icon_sp, command=lambda: salt_and_pepper_noise(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_sp.photo = icon_sp
        btn_sp.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_sp, "Salt-and-Pepper Noise")
        
        # Configures Gaussian Noise button
        img_gaussian = Image.open("assets\gaussian.png")
        img_gaussian = img_gaussian.resize((35,35))
        icon_gaussian = ImageTk.PhotoImage(img_gaussian)
      
        btn_gaussian = tk.Button(self.opsbar, image=icon_gaussian, command=lambda: gaussian_noise(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_gaussian.photo = icon_gaussian
        btn_gaussian.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_gaussian, "Gaussian Noise")
        
        # Configures Reyleigh Noise button
        img_rayleigh = Image.open("assets\\rayleigh.png")
        img_rayleigh = img_rayleigh.resize((35,35))
        icon_rayleigh = ImageTk.PhotoImage(img_rayleigh)
        
        btn_rayleigh = tk.Button(self.opsbar, image=icon_rayleigh, command=lambda: rayleigh_noise(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_rayleigh.photo = icon_rayleigh
        btn_rayleigh.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_rayleigh, "Rayleigh Noise")
        
    # Function that contains the buttons for the different image restoration techniques of the application
    def img_restoration(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, pady=(200, 90), sticky="nsew")
        
        # Configures Geometric filter button
        img_geometric = Image.open("assets\geometric.png")
        img_geometric = img_geometric.resize((35,35))
        icon_geometric = ImageTk.PhotoImage(img_geometric)
        
        btn_geometric = tk.Button(self.opsbar, image=icon_geometric, command=lambda: geometric_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_geometric.photo = icon_geometric
        btn_geometric.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_geometric, "Geometric Filter")

        # Configures Contraharmonic filter button
        img_contraharmonic = Image.open("assets\contraharmonic.png")
        img_contraharmonic = img_contraharmonic.resize((35,35))
        icon_contraharmonic = ImageTk.PhotoImage(img_contraharmonic)
        
        btn_contraharmonic = tk.Button(self.opsbar, image=icon_contraharmonic, command=lambda: contraharmonic_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_contraharmonic.photo = icon_contraharmonic
        btn_contraharmonic.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_contraharmonic, "Contraharmonic Filter")
        
        # Configures Median Filter button
        img_mdn = Image.open("assets\median.png")
        img_mdn = img_mdn.resize((30,30))
        icon_mdn = ImageTk.PhotoImage(img_mdn)
        
        btn_median = tk.Button(self.opsbar, image=icon_mdn, command=lambda: median_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_median.photo = icon_mdn
        btn_median.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_median, "Median Filter")
        
        # Configures Maximum filter button
        max_filter = Image.open("assets\maximum.png")
        max_filter = max_filter.resize((35,35))
        icon_max_filter = ImageTk.PhotoImage(max_filter)
        
        btn_max_filter = tk.Button(self.opsbar, image=icon_max_filter, command=lambda: maximum_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_max_filter.photo = icon_max_filter
        btn_max_filter.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_max_filter, "Max Filter")
        
        # Configures Minimum filter button
        min_filter = Image.open("assets\minimum.png")
        min_filter = min_filter.resize((35,35))
        icon_min_filter = ImageTk.PhotoImage(min_filter)
        
        btn_min_filter = tk.Button(self.opsbar, image=icon_min_filter, command=lambda: minimum_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_min_filter.photo = icon_min_filter
        btn_min_filter.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_min_filter, "Min Filter")

        # Configures Midpoint filter button   
        mid_filter = Image.open("assets\midpoint.png")
        mid_filter = mid_filter.resize((35,35))
        icon_mid_filter = ImageTk.PhotoImage(mid_filter)
        
        btn_mid_filter = tk.Button(self.opsbar, image=icon_mid_filter, command=lambda: midpoint_filter(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_mid_filter.photo = icon_mid_filter
        btn_mid_filter.grid(row=5, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_mid_filter, "Midpoint Filter")
        
    # Function that contains the buttons for the different image compression techniques of the application
    def img_compression(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, pady=(250, 260), sticky="nsew")
        
        # Configures Run Length Encoding button
        img_RLE = Image.open("assets\\run_length.png")
        img_RLE = img_RLE.resize((35,35))
        icon_RLE = ImageTk.PhotoImage(img_RLE)
        
        btn_RLE = tk.Button(self.opsbar, image=icon_RLE, command=lambda: run_length_coding(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_RLE.photo = icon_RLE
        btn_RLE.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_RLE, "Run-Length Coding")
        
        # Configures Huffman coding button
        img_huffman = Image.open("assets\huffman.png")
        img_huffman = img_huffman.resize((35,35))
        icon_huffman = ImageTk.PhotoImage(img_huffman)
        
        btn_huffman = tk.Button(self.opsbar, image=icon_huffman, command=lambda: huffman_coding(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_huffman.photo = icon_huffman
        btn_huffman.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_huffman, "Huffman Coding")
    
    def opticalFlow(self):
        self.opsbar.destroy()
        self.opsbar = tk.Frame(self, width=100, bg="#313131")
        self.opsbar.grid(row=1, column=1, pady=(350, 180), sticky="nsew")
        # image_sequence = open_zip_file(self)
        # dense_optical(image_sequence)
        # Configures Run Length Encoding button
        img_dense = Image.open("assets\\dense.png")
        img_dense = img_dense.resize((35,35))
        icon_dense = ImageTk.PhotoImage(img_dense)
        
        # img_sequence = variables.image_paths
        
        btn_dense = tk.Button(self.opsbar, image=icon_dense, command=lambda: dense_optical(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_dense.photo = icon_dense
        btn_dense.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_dense, "Dense Optical Flow")
        
        # Configures Huffman coding button
        img_sparse = Image.open("assets\sparse.png")
        img_sparse = img_sparse.resize((35,35))
        icon_sparse = ImageTk.PhotoImage(img_sparse)
        
        btn_sparse = tk.Button(self.opsbar, image=icon_sparse, command=lambda: sparse_optical(self), background="#2B2B2B", foreground="white",relief="ridge", borderwidth=2)
        btn_sparse.photo = icon_sparse
        btn_sparse.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        CreateToolTip(btn_sparse, "Sparse Optical Flow")
    
    # Function that closes the image file being displayed
    # It removes all references of the image, information, and applied operations to its respective variables and widgets
    # It also reverts the program back to its state when it was first opened    
    def close_img(self):
        
        variables.orig_img = None
        variables.curr_img = None
        variables.red_channel = []
        variables.green_channel = []
        variables.blue_channel = []
        variables.pcx_image_data = []
        
        # Reverts right sidebar to its original form
        self.rightsidebar.destroy()
        self.rightsidebar = tk.Frame(self, width=250,  bg="#2B2B2B")
        self.rightsidebar.grid(row=1, column=3, sticky="nsew")
        
        self.opsbar.grid_forget()
        
        # Removes image in the image panel
        self.image_label.destroy()
        self.image_label = tk.Label(self, bg="#242424")
        self.image_label.grid(row=1, column=2, sticky="nsew")

        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=4, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar("Status: Image closed", x=120, y=20, fill="white", font=("Arial", 9,))

if __name__ == "__main__":
    app = App()
    app.mainloop()