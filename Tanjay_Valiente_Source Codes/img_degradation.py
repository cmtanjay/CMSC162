# This is where the noise models are added to images.
import numpy as np
import math
from statistics import *
import tkinter as tk #pip install tk
from tkinter import ttk

from PIL import Image
import random

import variables
from img_ops import *

import matplotlib.pyplot as plt

# Function that adds salt and pepper noise to an image
def salt_and_pepper_noise(self):
    # Function that pops up a window that lets the user input the probability for both salt and pepper noises 
    def open_popup():
        window = tk.Toplevel()
        window.geometry("400x200+500+300")
        window.title("Salt and Pepper Noise")
        window.resizable(False, False)
        
        window.columnconfigure(0, weight=2)
        window.columnconfigure(1, weight=5)
        
        salt_prob = tk.DoubleVar()
        pepper_prob = tk.DoubleVar()

        # Detects the value inside the text box
        def entry_changed(event):
            # Get the value from the entry box
            salt_value = salt_text_box.get()  
            pepper_value = pepper_text_box.get()
            
            # Makes sure that the values of the probabilities for salt and pepper noises are:
            # 1) Within 0 to 1
            # 2) The sum of the probabilities do not exceed 1
            if (float(salt_value) >= 0 and float(salt_value) <= 1) and (float(pepper_value) >= 0 and float(pepper_value) <= 1) and (float(salt_value) + float(pepper_value) >= 0 and float(salt_value) + float(pepper_value) <= 1): 
                salt_prob.set(float(salt_value))  # Set the slider value to the entry value
            else:
                err_window = tk.Toplevel()
                err_window.geometry("400x130+500+300")
                err_window.title("Salt and Pepper Noise")
                err_window.resizable(False, False)
                ttk.Label(err_window, text='Both probabilities must be within and equate in range 0-1', font=('Arial 8 bold')).place(x=50, y=35)
                btn_ok = tk.Button(err_window, command=err_window.destroy, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
                btn_ok.place(x=80, y=85)

        # Function that executes when OK button is clicked
        def on_click():
            window.destroy()

        # current value label
        ttk.Label(window, text='Input Salt Noise Probability:', font=('Arial 10 bold')).place(x=150, y=35)
        
        salt_text_box = tk.Entry(window, bg="white", textvariable=salt_prob, width=5, font=('Arial 13'))
        salt_text_box.place(x=160, y=55)
        salt_text_box.bind("<KeyRelease>", entry_changed)
        
        # current value label
        ttk.Label(window, text='Input Pepper Noise Probability:', font=('Arial 10 bold')).place(x=150, y=105)
        
        pepper_text_box = tk.Entry(window, bg="white", textvariable=pepper_prob, width=5, font=('Arial 13'))
        pepper_text_box.place(x=160, y=125)
        pepper_text_box.bind("<KeyRelease>", entry_changed)
        
        btn = tk.Button(window, command=on_click, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",relief="ridge", borderwidth=2)
        btn.place(x=165, y=155)
        
        window.wait_window(window)  # Wait for the window to be destroyed
        
        return salt_prob.get(), pepper_prob.get()
    
    if not variables.pcx_image_data and variables.file_type == 1:
        print("No PCX Image Loaded Damn")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    
    elif variables.file_type == 2:
        variables.is_filtered = True
        variables.img_seq = []
        
        Ps, Pp = open_popup()
        
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
            if os.path.basename(path).split('.')[-1] == "bmp": # if a bmp file is opened
                extract_bmp(self, path)
            else: # if other image types (jpg, png, tiff, etc) are opened
                other_image = Image.open(path)

                # Convert the image to BMP format
                bmp_image = other_image.convert('RGB')
                variables.pcx_image_data = list(bmp_image.getdata())
                variables.img_height = bmp_image.height
                variables.img_width = bmp_image.width
            
            
            gray = get_grayscale_img(self) # transforms image to grayscale
            flat_gray_orig = [element for row in gray for element in row]
            
            # Create a blank image with a white background
            img_SP = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_SP = ImageDraw.Draw(img_SP)
            
            deg_img = []
            row = []
            
            # Salt and pepper process
            for i, color in enumerate(flat_gray_orig):
                random = np.random.random()
                
                if random < Pp:
                    row.append(0)
                elif random > (1-Ps):
                    row.append((2**variables.bits_per_pixel)-1)
                else:
                    row.append(color)
                    
                if len(row) == variables.img_width:
                    deg_img.append(row)
                    row = []
            
            drawImage(self, draw_SP, deg_img)
                    
            variables.img_seq.append(img_SP)
            
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
        
        Ps, Pp = open_popup()
        
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
            
            if status:
                
                # Convert the frame to BMP format
                bmp_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Access pixel data
                variables.pcx_image_data = list(bmp_image.getdata())
        
                gray = get_grayscale_img(self) # transforms image to grayscale
                flat_gray_orig = [element for row in gray for element in row]
                
                # Create a blank image with a white background
                img_SP = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_SP = ImageDraw.Draw(img_SP)
                
                deg_img = []
                row = []
                
                # Salt and pepper process
                for i, color in enumerate(flat_gray_orig):
                    random = np.random.random()
                    
                    if random < Pp:
                        row.append(0)
                    elif random > (1-Ps):
                        row.append((2**variables.bits_per_pixel)-1)
                    else:
                        row.append(color)
                        
                    if len(row) == variables.img_width:
                        deg_img.append(row)
                        row = []
                
                drawImage(self, draw_SP, deg_img)
                
                new_frame = cv2.cvtColor(np.array(img_SP), cv2.COLOR_RGB2BGR)
                
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
        Ps, Pp = open_popup()
        
        gray = get_grayscale_img(self) # transforms image to grayscale
        flat_gray_orig = [element for row in gray for element in row]
        
        # Create a blank image with a white background
        img_SP = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_SP = ImageDraw.Draw(img_SP)
        
        deg_img = []
        row = []
        
        # Salt and pepper process
        for i, color in enumerate(flat_gray_orig):
            random = np.random.random()
            
            if random < Pp:
                row.append(0)
            elif random > (1-Ps):
                print(variables.bits_per_pixel)
                row.append((2**variables.bits_per_pixel)-1)
            else:
                row.append(color)
                
            if len(row) == variables.img_width:
                deg_img.append(row)
                row = []
        
        drawImage(self, draw_SP, deg_img)
        show_image(self, img_SP, " ")
        variables.curr_img = img_SP
        variables.curr_image_data = deg_img
        variables.degraded_image_data = deg_img
        variables.isDegraded = True

        image_data = [element for row in variables.degraded_image_data for element in row]

        # Call show histogram function after applying salt and pepper noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Salt and Pepper Noise Histogram'))
    
# Function for applying Gaussian noise to an image
def gaussian_noise(self):
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
            if os.path.basename(path).split('.')[-1] == "bmp": # if a bmp file is opened
                extract_bmp(self, path)
            else: # if other image types (jpg, png, tiff, etc) are opened
                other_image = Image.open(path)

                # Convert the image to BMP format
                bmp_image = other_image.convert('RGB')
                variables.pcx_image_data = list(bmp_image.getdata())
                variables.img_height = bmp_image.height
                variables.img_width = bmp_image.width
            
            gray = get_grayscale_img(self)  # transforms image to grayscale
            flat_gray_orig = [element for row in gray for element in row]

            avg = mean(flat_gray_orig)
            sigma = pstdev(flat_gray_orig)

            # Create a blank image with a white background
            img_Gaussian = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_Gaussian = ImageDraw.Draw(img_Gaussian)

            corrupted_img = []

            # Apply Gaussian noise to each pixel
            for x in range(variables.img_height):
                row = []
                for y in range(variables.img_width):
                    pixel_value = gray[x][y]
                    noise = int(np.random.randn() * sigma)
                    noisy_value = max(0, min(255, pixel_value + noise))
                    row.append(noisy_value)
                corrupted_img.append(row)

            # Draw the corrupted image
            drawImage(self, draw_Gaussian, corrupted_img)
                    
            variables.img_seq.append(img_Gaussian)
            
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
            
            if status:
                
                # Convert the frame to BMP format
                bmp_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Access pixel data
                variables.pcx_image_data = list(bmp_image.getdata())
        
                gray = get_grayscale_img(self)  # transforms image to grayscale
                flat_gray_orig = [element for row in gray for element in row]

                avg = mean(flat_gray_orig)
                sigma = pstdev(flat_gray_orig)

                # Create a blank image with a white background
                img_Gaussian = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_Gaussian = ImageDraw.Draw(img_Gaussian)

                corrupted_img = []

                # Apply Gaussian noise to each pixel
                for x in range(variables.img_height):
                    row = []
                    for y in range(variables.img_width):
                        pixel_value = gray[x][y]
                        noise = int(np.random.randn() * sigma)
                        noisy_value = max(0, min(255, pixel_value + noise))
                        row.append(noisy_value)
                    corrupted_img.append(row)

                # Draw the corrupted image
                drawImage(self, draw_Gaussian, corrupted_img)
                
                new_frame = cv2.cvtColor(np.array(img_Gaussian), cv2.COLOR_RGB2BGR)
                
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
        gray = get_grayscale_img(self)  # transforms image to grayscale
        flat_gray_orig = [element for row in gray for element in row]

        avg = mean(flat_gray_orig)
        sigma = pstdev(flat_gray_orig)

        # Create a blank image with a white background
        img_Gaussian = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_Gaussian = ImageDraw.Draw(img_Gaussian)

        corrupted_img = []

        # Apply Gaussian noise to each pixel
        for x in range(variables.img_height):
            row = []
            for y in range(variables.img_width):
                pixel_value = gray[x][y]
                noise = int(np.random.randn() * sigma)
                noisy_value = max(0, min(255, pixel_value + noise))
                row.append(noisy_value)
            corrupted_img.append(row)

        print(corrupted_img)

        # Draw the corrupted image
        drawImage(self, draw_Gaussian, corrupted_img)
        show_image(self, img_Gaussian, "Corrupted Image")

        variables.curr_img = img_Gaussian
        variables.curr_image_data = corrupted_img
        variables.isDegraded = True
        variables.degraded_image_data = corrupted_img
        
        image_data = [element for row in variables.degraded_image_data for element in row]

        # Call show histogram function after applying Gaussian noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Gaussian Noise Histogram'))

# Function for applying Rayleigh noise to an image
def rayleigh_noise(self):
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
            if os.path.basename(path).split('.')[-1] == "bmp": # if a bmp file is opened
                extract_bmp(self, path)
            else: # if other image types (jpg, png, tiff, etc) are opened
                other_image = Image.open(path)

                # Convert the image to BMP format
                bmp_image = other_image.convert('RGB')
                variables.pcx_image_data = list(bmp_image.getdata())
                variables.img_height = bmp_image.height
                variables.img_width = bmp_image.width
            
            gray = get_grayscale_img(self)  # transforms image to grayscale

            # Set the scale parameter/ sigma for the Rayleigh distribution
            scale_param = 20.0

            # Create a blank image with a white background
            img_Rayleigh = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_Rayleigh = ImageDraw.Draw(img_Rayleigh)

            corrupted_img = []

            # Apply Rayleigh noise to each pixel
            for x in range(variables.img_height):
                row = []
                for y in range(variables.img_width):
                    pixel_value = gray[x][y]
                    
                    # Using the random module to generate Rayleigh-distributed noise
                    noise = int(np.random.rayleigh(scale=scale_param))
                    
                    noisy_value = max(0, min(255, pixel_value + noise))
                    row.append(noisy_value)
                corrupted_img.append(row)

            # Draw the corrupted image
            drawImage(self, draw_Rayleigh, corrupted_img)
                    
            variables.img_seq.append(img_Rayleigh)
            
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
            
            if status:
                
                # Convert the frame to BMP format
                bmp_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Access pixel data
                variables.pcx_image_data = list(bmp_image.getdata())
        
                gray = get_grayscale_img(self)  # transforms image to grayscale

                # Set the scale parameter/ sigma for the Rayleigh distribution
                scale_param = 20.0

                # Create a blank image with a white background
                img_Rayleigh = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_Rayleigh = ImageDraw.Draw(img_Rayleigh)

                corrupted_img = []

                # Apply Rayleigh noise to each pixel
                for x in range(variables.img_height):
                    row = []
                    for y in range(variables.img_width):
                        pixel_value = gray[x][y]
                        
                        # Using the random module to generate Rayleigh-distributed noise
                        noise = int(np.random.rayleigh(scale=scale_param))
                        
                        noisy_value = max(0, min(255, pixel_value + noise))
                        row.append(noisy_value)
                    corrupted_img.append(row)

                # Draw the corrupted image
                drawImage(self, draw_Rayleigh, corrupted_img)
                
                new_frame = cv2.cvtColor(np.array(img_Rayleigh), cv2.COLOR_RGB2BGR)
                
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
        gray = get_grayscale_img(self)  # transforms image to grayscale

        # Set the scale parameter/ sigma for the Rayleigh distribution
        scale_param = 20.0

        # Create a blank image with a white background
        img_Rayleigh = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_Rayleigh = ImageDraw.Draw(img_Rayleigh)

        corrupted_img = []

        # Apply Rayleigh noise to each pixel
        for x in range(variables.img_height):
            row = []
            for y in range(variables.img_width):
                pixel_value = gray[x][y]
                
                # Using the random module to generate Rayleigh-distributed noise
                noise = int(np.random.rayleigh(scale=scale_param))
                
                noisy_value = max(0, min(255, pixel_value + noise))
                row.append(noisy_value)
            corrupted_img.append(row)

        # Draw the corrupted image
        drawImage(self, draw_Rayleigh, corrupted_img)
        show_image(self, img_Rayleigh, "Corrupted Image")

        variables.curr_img = img_Rayleigh
        variables.curr_image_data = corrupted_img
        variables.isDegraded = True
        variables.degraded_image_data = corrupted_img
        
        image_data = [element for row in variables.degraded_image_data for element in row]
        
        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Rayleigh Noise Histogram'))