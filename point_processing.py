# This is where the point processing techniques are implemented.
from PIL import Image, ImageTk, ImageDraw #pip install pillow
import tkinter as tk #pip install tk
from tkinter import ttk

import variables
from img_ops import *

# Function that transforms the RGB PCX file to Grayscale
def grayscale_transform(self):
    if not variables.pcx_image_data and variables.file_type == 1:
        print("No PCX Image Loaded")
        # self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
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
            # Creates the output image
            grayscale_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_grayscale = ImageDraw.Draw(grayscale_img)
            
            gray = get_grayscale_img(self) # transforms image to grayscale
            
            drawImage(self, draw_grayscale, gray) # draws resulting pixel values to image
            variables.img_seq.append(grayscale_img)
            
            value += (1/len(variables.image_paths))*100
            self.progress_var.set(value)
            self.progress_window.update()
            
            num += 1
            print(num)
        
        self.progress_window.destroy()
        show_image(self, variables.img_seq[0], " ")
             
    else:
        # Creates the output image
        grayscale_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_grayscale = ImageDraw.Draw(grayscale_img)
        
        gray = get_grayscale_img(self) # transforms image to grayscale
        
        drawImage(self, draw_grayscale, gray) # draws resulting pixel values to image
        
        show_image(self, grayscale_img, " ") # shows image to GUI
        variables.curr_img = grayscale_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar("Status: Image transformed to grayscale through transformation function (R+G+B)/3", x=250, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in gray for element in row]

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Grayscale Image Histogram'))

# Function that transforms the RGB PCX file to Negative image
def negative_transform(self):
    if not variables.pcx_image_data and variables.file_type == 1:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
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
            
            # Creates the output image
            negative_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_negative = ImageDraw.Draw(negative_img)
            
            gray = get_grayscale_img(self)
            negative_pixels = [[255 - pixel for pixel in row] for row in gray]
            drawImage(self, draw_negative, negative_pixels) # draws resulting pixel values to image
            variables.img_seq.append(negative_img)
            
            value += (1/len(variables.image_paths))*100
            self.progress_var.set(value)
            self.progress_window.update()
            
            num += 1
            print(num)
        
        self.progress_window.destroy()
        show_image(self, variables.img_seq[0], " ")
            
    else:
        # Creates the output image
        negative_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_negative = ImageDraw.Draw(negative_img)
        
        gray = get_grayscale_img(self)
        
        negative_pixels = [[255 - pixel for pixel in row] for row in gray]
        negative = [element for row in negative_pixels for element in row]
        drawImage(self, draw_negative, negative_pixels)
            
        show_image(self, negative_img, " ")
        variables.curr_img = negative_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar("Status: Image transformed to negative image through transformation function s = L - 1 - r", x=300, y=20, fill="white", font=("Arial", 9,))

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(negative, 'Negative Image Histogram'))

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
            value = int(current_value.get())
            text_box.delete(0, tk.END)  # Clear the entry box
            text_box.insert(0, value)

        # Function that executes when OK button is clicked
        def on_click():
            value = int(current_value.get())
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
    
    if not variables.pcx_image_data and variables.file_type == 1:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    
    elif variables.file_type == 2:
        variables.is_filtered = True
        variables.img_seq = []
        
        threshold = open_popup()
        
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
            # Creates the output image
            BW_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_BW = ImageDraw.Draw(BW_img)
            
            gray = get_grayscale_img(self)
            BW_pixels = [[0 if color <= threshold else 255 for color in row] for row in gray]
            drawImage(self, draw_BW, BW_pixels) # draws resulting pixel values to image
            variables.img_seq.append(BW_img)
            
            value += (1/len(variables.image_paths))*100
            self.progress_var.set(value)
            self.progress_window.update()
            
            num += 1
            print(num)
        
        self.progress_window.destroy()
        show_image(self, variables.img_seq[0], " ")
            
    else:
        threshold = open_popup()
        # Creates the output image
        BW_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_BW = ImageDraw.Draw(BW_img)
        
        gray = get_grayscale_img(self) # transforms image to grayscale
        BW_pixels = [[0 if color <= threshold else 255 for color in row] for row in gray]
        BW_color = [element for row in BW_pixels for element in row]

        drawImage(self, draw_BW, BW_pixels)
            
        show_image(self, BW_img, " ")
        variables.curr_img = BW_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Image transformed to Black&White at threshold = {threshold}", x=200, y=20, fill="white", font=("Arial", 9,))

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(BW_color, 'B&W Thresholded Image Histogram'))

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
            if float(value) >= 0:  # Check if the value is a positive constant
                current_value.set(float(value))  # Set the slider value to the entry value
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
    
    if not variables.pcx_image_data and variables.file_type == 1:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    
    elif variables.file_type == 2:
        variables.is_filtered = True
        variables.img_seq = []
        
        gamma = open_popup()
        
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
            
            # Creates the output image
            PL_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_PL = ImageDraw.Draw(PL_img)
            
            gray = get_grayscale_img(self)
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
                    
            variables.img_seq.append(PL_img)
            
            value += (1/len(variables.image_paths))*100
            self.progress_var.set(value)
            self.progress_window.update()
            
            num += 1
            print(num)
        
        self.progress_window.destroy()
        show_image(self, variables.img_seq[0], " ")
        
    else:
        gamma = open_popup()
        # Creates the output image
        PL_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_PL = ImageDraw.Draw(PL_img)
        
        gray = get_grayscale_img(self) # transforms image to grayscale
        
        # Define the size of each color block
        PL_color=[]

        # Draws the resulting pixels to an image
        for i, row in enumerate(gray):
            for j, color in enumerate(row):
                x1 = j
                y1 = i
                x2 = x1 + 1
                y2 = y1 + 1

                c = 1
                color = (int)(c*(color**gamma))
                PL_color.append(color)
                
                # Clips pixel values between 0 and 255
                if color < 0:
                    color = 0
                elif color > 255:
                    color = 255

                draw_PL.rectangle([x1, y1, x2, y2], fill=color)
            
        show_image(self, PL_img, " ")
        variables.curr_img = PL_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Image transformed through transformation function s=c*r^(gamma) where c = 1 and gamma = {gamma}", x=330, y=20, fill="white", font=("Arial", 9,))

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(PL_color, 'Power-Law Transformed Image Histogram'))