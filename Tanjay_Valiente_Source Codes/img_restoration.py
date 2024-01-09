# This is where the image restoration process is implemented.
# When an image is degraded by the functions in img_degradation, the functions in this file restores it.
# Otherwise, it applies the same techniques as an enhancement filter.
import numpy as np
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import tkinter as tk
from tkinter import ttk
import math

import variables
from img_ops import *
from img_enhancement import *

# Function that implements the maximum filter by getting the highest pixel value within a mask.    
def maximum_filter(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(neighbors):        
        return max([element for row in neighbors for element in row])
    
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
            
            # Initializes the n x n mask
            radius = variables.n//2
            
            data = get_grayscale_img(self) # transforms image to grayscale
                            
            data_2D = [row[:] for row in data]
            
            padded_img = clamp_padding(radius, data) # executes clamp padding
            
            # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
            neighbors = []
            for i in range(variables.img_height):
                for j in range(variables.img_width):
                    neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                    data_2D[i][j] = get_pixel_value(neighbors)
            
            # Creates the output image
            max_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_max_filtered = ImageDraw.Draw(max_filtered_img)        
            drawImage(self, draw_max_filtered, data_2D)
                    
            variables.img_seq.append(max_filtered_img)
            
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
        
        output_video = cv2.VideoWriter(output_video_filepath, fourcc, 80, (variables.img_width, variables.img_height))
        
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
        
                # Initializes the n x n mask
                radius = variables.n//2
                
                data = get_grayscale_img(self) # transforms image to grayscale
                                
                data_2D = [row[:] for row in data]
                
                padded_img = clamp_padding(radius, data) # executes clamp padding
                
                # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
                neighbors = []
                for i in range(variables.img_height):
                    for j in range(variables.img_width):
                        neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                        data_2D[i][j] = get_pixel_value(neighbors)
                
                # Creates the output image
                max_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_max_filtered = ImageDraw.Draw(max_filtered_img)        
                drawImage(self, draw_max_filtered, data_2D)
                
                new_frame = cv2.cvtColor(np.array(max_filtered_img), cv2.COLOR_RGB2BGR)
                
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
        # Initializes the n x n mask
        radius = variables.n//2
        
        if variables.isDegraded:
            data = variables.degraded_image_data
        else:
            data = get_grayscale_img(self) # transforms image to grayscale
                        
        data_2D = [row[:] for row in data]
        
        padded_img = clamp_padding(radius, data) # executes clamp padding
        
        # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                data_2D[i][j] = get_pixel_value(neighbors)
        
        # Creates the output image
        max_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_max_filtered = ImageDraw.Draw(max_filtered_img)        
        drawImage(self, draw_max_filtered, data_2D)        
        show_image(self, max_filtered_img, " ")
        variables.curr_image_data = data_2D
        variables.curr_img = max_filtered_img
                
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Averaging filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in data_2D for element in row]

        # Call show histogram function after applying salt and pepper noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Maximum Filtered Histogram'))

# Function that implements the minimum filter by getting the lowest pixel value within a mask.    
def minimum_filter(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(neighbors):        
        return min([element for row in neighbors for element in row])
    
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
            
            # Initializes the n x n mask
            radius = variables.n//2
                            
            data = get_grayscale_img(self)
                            
            data_2D = [row[:] for row in data]
            
            padded_img = clamp_padding(radius, data) # executes clamp padding
            
            # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
            neighbors = []
            for i in range(variables.img_height):
                for j in range(variables.img_width):
                    neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                    data_2D[i][j] = get_pixel_value(neighbors)
            
            # Creates the output image
            min_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_min_filtered = ImageDraw.Draw(min_filtered_img)        
            drawImage(self, draw_min_filtered, data_2D)
                    
            variables.img_seq.append(min_filtered_img)
            
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
        
                # Initializes the n x n mask
                radius = variables.n//2
                                
                data = get_grayscale_img(self)
                                
                data_2D = [row[:] for row in data]
                
                padded_img = clamp_padding(radius, data) # executes clamp padding
                
                # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
                neighbors = []
                for i in range(variables.img_height):
                    for j in range(variables.img_width):
                        neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                        data_2D[i][j] = get_pixel_value(neighbors)
                
                # Creates the output image
                min_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_min_filtered = ImageDraw.Draw(min_filtered_img)        
                drawImage(self, draw_min_filtered, data_2D)
                
                new_frame = cv2.cvtColor(np.array(min_filtered_img), cv2.COLOR_RGB2BGR)
                
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
        # Initializes the n x n mask
        radius = variables.n//2
        
        if variables.isDegraded:
            data = variables.degraded_image_data
        else:
            data = get_grayscale_img(self) # transforms image to grayscale
                        
        data_2D = [row[:] for row in data]
        
        padded_img = clamp_padding(radius, data) # executes clamp padding
        
        # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                data_2D[i][j] = get_pixel_value(neighbors)
        
        # Creates the output image
        min_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_min_filtered = ImageDraw.Draw(min_filtered_img)        
        drawImage(self, draw_min_filtered, data_2D)        
            
        show_image(self, min_filtered_img, " ")
        variables.curr_image_data = data_2D
        variables.curr_img = min_filtered_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Averaging filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in data_2D for element in row]

        # Call show histogram function after applying salt and pepper noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Minimum Filtered Histogram'))

# Function that implements the geometric filter by getting the product of all pixels inside a mask then exponentiating
# it to 1/n.  
def geometric_filter(self):
    def get_pixel_value(neighbors):
        
        final_product = 1.00
        count = 0
        for row in neighbors:
            row_prod = np.prod(row)
            count += len(row)
            final_product = final_product * row_prod
        
        
        # Check if the product is non-positive
        if final_product <= 0:
            # Handle non-positive values, for example, return 0 or a default value
            return 0
        
        # epsilon = 1e-10  # Small positive constant to avoid numerical instability
        return int((final_product)**(1.0 / count))

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
            
            # Initializes the n x n mask
            radius = variables.n//2
                            
            data = get_grayscale_img(self)

            data_2D = [row[:] for row in data]
            padded_img = clamp_padding(radius, data)

            for i in range(variables.img_height):
                for j in range(variables.img_width):
                    neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                    data_2D[i][j] = get_pixel_value(neighbors)

            geo_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_geo_filtered = ImageDraw.Draw(geo_filtered_img)
            drawImage(self, draw_geo_filtered, data_2D)
                    
            variables.img_seq.append(geo_filtered_img)
            
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
        
                # Initializes the n x n mask
                radius = variables.n//2
                                
                data = get_grayscale_img(self)

                data_2D = [row[:] for row in data]
                padded_img = clamp_padding(radius, data)

                for i in range(variables.img_height):
                    for j in range(variables.img_width):
                        neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                        data_2D[i][j] = get_pixel_value(neighbors)

                geo_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_geo_filtered = ImageDraw.Draw(geo_filtered_img)
                drawImage(self, draw_geo_filtered, data_2D)
                
                new_frame = cv2.cvtColor(np.array(geo_filtered_img), cv2.COLOR_RGB2BGR)
                
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
        radius = variables.n // 2

        if variables.isDegraded: # If image is degraded
            data = variables.degraded_image_data
        else: # if image is not degraded (no noises are applied by the user)
            data = get_grayscale_img(self)

        data_2D = [row[:] for row in data]
        padded_img = clamp_padding(radius, data)

        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                data_2D[i][j] = get_pixel_value(neighbors)

        geo_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_geo_filtered = ImageDraw.Draw(geo_filtered_img)
        drawImage(self, draw_geo_filtered, data_2D)
        show_image(self, geo_filtered_img, " ")
        
        variables.curr_image_data = data_2D
        variables.curr_img = geo_filtered_img

        # Updates the status bar
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Geometric mean filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in data_2D for element in row]

        # Call show histogram function after applying salt and pepper noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Geometric Filtered Histogram'))

# Function that implements the contraharmonic filter
def contraharmonic_filter(self):
    def open_popup():
        window = tk.Toplevel()
        window.geometry("400x200+500+300")
        window.title("Contraharmonic Filter")
        window.resizable(False, False)

        window.columnconfigure(0, weight=2)
        window.columnconfigure(1, weight=5)

        Q_var = tk.DoubleVar()

        def entry_changed(event):
            Q_value = Q_text_box.get()
            try:
                Q_value = float(Q_value)
                Q_var.set(Q_value)
            except ValueError:
                pass

        def on_click():
            window.destroy()

        ttk.Label(window, text='Input Q for Contraharmonic Filter:', font=('Arial 10 bold')).place(x=120, y=35)

        Q_text_box = tk.Entry(window, bg="white", textvariable=Q_var, width=5, font=('Arial 13'))
        Q_text_box.place(x=160, y=55)
        Q_text_box.bind("<KeyRelease>", entry_changed)

        btn = tk.Button(window, command=on_click, text="OK", font=("Arial", 10), background="#313E4E", foreground="white",
                        relief="ridge", borderwidth=2)
        btn.place(x=165, y=155)

        window.wait_window(window)
        return Q_var.get()

    # Function that gets the pixel value of a resulting image by using the contraharmonic filter equation
    def get_pixel_value(neighbors, Q):
        flat_neighbors = np.array(neighbors).flatten()
        
        numerator = 0.0
        denominator = 0.0
        for pixel in flat_neighbors:
            if pixel == 0 and (Q+1) < 0:
                numerator += 0
            else:
                numerator += pixel**(Q+1)
                
            if pixel == 0 and Q < 0:
                denominator += 0
            else:
                denominator += pixel**Q
                
        return int(numerator // denominator) if denominator != 0 else 0

    if not variables.pcx_image_data and variables.file_type == 1:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    
    elif variables.file_type == 2:
        variables.is_filtered = True
        variables.img_seq = []
        
        Q = open_popup()
        
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
            
            radius = variables.n // 2

            data = get_grayscale_img(self)

            data_2D = [row[:] for row in data]
            padded_img = clamp_padding(radius, data)

            for i in range(variables.img_height):
                for j in range(variables.img_width):
                    neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                    data_2D[i][j] = get_pixel_value(neighbors, Q)

            contraharmonic_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_contraharmonic = ImageDraw.Draw(contraharmonic_img)
            drawImage(self, draw_contraharmonic, data_2D)
                    
            variables.img_seq.append(contraharmonic_img)
            
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
        
        Q = open_popup()
        
        while True:
            status, frame = video.read() 
            
            if status:
                
                # Convert the frame to BMP format
                bmp_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Access pixel data
                variables.pcx_image_data = list(bmp_image.getdata())
        
                radius = variables.n // 2


                data = get_grayscale_img(self)

                data_2D = [row[:] for row in data]
                padded_img = clamp_padding(radius, data)

                for i in range(variables.img_height):
                    for j in range(variables.img_width):
                        neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                        data_2D[i][j] = get_pixel_value(neighbors, Q)

                contraharmonic_img = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_contraharmonic = ImageDraw.Draw(contraharmonic_img)
                drawImage(self, draw_contraharmonic, data_2D)
                
                new_frame = cv2.cvtColor(np.array(contraharmonic_img), cv2.COLOR_RGB2BGR)
                
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
        Q = open_popup()

        radius = variables.n // 2

        if variables.isDegraded:
            data = variables.degraded_image_data
        else:
            data = get_grayscale_img(self)

        data_2D = [row[:] for row in data]
        padded_img = clamp_padding(radius, data)

        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                data_2D[i][j] = get_pixel_value(neighbors, Q)

        contraharmonic_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_contraharmonic = ImageDraw.Draw(contraharmonic_img)
        drawImage(self, draw_contraharmonic, data_2D)

        show_image(self, contraharmonic_img, " ")
        variables.curr_image_data = data_2D
        variables.curr_img = contraharmonic_img

        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Contraharmonic filter (Q={Q}) is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))
        
        image_data = [element for row in data_2D for element in row]

        # Call show histogram function after applying salt and pepper noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Contraharmonic Filtered Histogram'))
        
# Function that applies the midpoint filter by getting the average of the maximum and minimum pixel value of an nxn mask
def midpoint_filter(self):
    # Function that gets the pixel value of a resulting image
    def get_pixel_value(neighbors):
        min_val = np.min(neighbors)
        max_val = np.max(neighbors)
        return int((min_val + max_val) / 2)

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
            
            radius = variables.n // 2

            data = get_grayscale_img(self)

            data_2D = [row[:] for row in data]
            padded_img = clamp_padding(radius, data)

            for i in range(variables.img_height):
                for j in range(variables.img_width):
                    neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                    data_2D[i][j] = get_pixel_value(neighbors)

            midpoint_img = Image.new('L', (variables.img_width, variables.img_height), 255)
            draw_midpoint = ImageDraw.Draw(midpoint_img)
            drawImage(self, draw_midpoint, data_2D)
                    
            variables.img_seq.append(midpoint_img)
            
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
        
                radius = variables.n // 2

                data = get_grayscale_img(self)

                data_2D = [row[:] for row in data]
                padded_img = clamp_padding(radius, data)

                for i in range(variables.img_height):
                    for j in range(variables.img_width):
                        neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                        data_2D[i][j] = get_pixel_value(neighbors)

                midpoint_img = Image.new('L', (variables.img_width, variables.img_height), 255)
                draw_midpoint = ImageDraw.Draw(midpoint_img)
                drawImage(self, draw_midpoint, data_2D)
                
                new_frame = cv2.cvtColor(np.array(midpoint_filter), cv2.COLOR_RGB2BGR)
                
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
        radius = variables.n // 2

        if variables.isDegraded:
            data = variables.degraded_image_data
        else:
            data = get_grayscale_img(self)

        data_2D = [row[:] for row in data]
        padded_img = clamp_padding(radius, data)

        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i + radius, j + radius, radius, padded_img)
                data_2D[i][j] = get_pixel_value(neighbors)

        midpoint_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_midpoint = ImageDraw.Draw(midpoint_img)
        drawImage(self, draw_midpoint, data_2D)

        show_image(self, midpoint_img, " ")
        variables.curr_image_data = data_2D
        variables.curr_img = midpoint_img

        # Updates status bar
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Midpoint filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))
        
        image_data = [element for row in data_2D for element in row]

        # Call show histogram function after applying salt and pepper noise
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Midpoint Filtered Histogram'))