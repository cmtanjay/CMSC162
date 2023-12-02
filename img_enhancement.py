import variables
from img_ops import *

# Function that implements the averaging filter which blurs the image
def average_filter(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(mask, neighbors):
        avg = 0
        for i in range(len(mask)):
            for j in range(len(mask[0])):
                avg += neighbors[i][j]*mask[i][j]
        
        return int(avg)
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        radius = variables.n//2
        mask = [[1/(variables.n*variables.n) for i in range(variables.n)] for j in range(variables.n)]
        
        gray = get_grayscale_img(self) # transforms image to grayscale
                        
        blur_pixels = [row[:] for row in gray]
        
        padded_img = clamp_padding(radius, gray) # executes clamp padding
        
        # Updates current pixel value with the average of the sum of it and its neighbors in an nxn mask
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                blur_pixels[i][j] = get_pixel_value(mask, neighbors)
        
        # Creates the output image
        avg_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_avg_filtered = ImageDraw.Draw(avg_filtered_img)        
        drawImage(self, draw_avg_filtered, blur_pixels)        
            
        show_image(self, avg_filtered_img, " ")
        variables.curr_img = avg_filtered_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Averaging filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in blur_pixels for element in row]

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Averaging Filtered Image Histogram'))

# Function that implements the unsharp masking       
def unsharp_masking(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(mask, neighbors):
        avg = 0
        for i in range(len(mask)):
            for j in range(len(mask[0])):
                avg += neighbors[i][j]*mask[i][j]
        
        return int(avg)
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        radius = variables.n//2
        mask = [[1/(variables.n*variables.n) for i in range(variables.n)] for j in range(variables.n)]
        
        gray_orig = get_grayscale_img(self) # transforms image to grayscale
        
        flat_gray_orig = [element for row in gray_orig for element in row]
        blur_pixels = [row[:] for row in gray_orig]
        
        padded_img = clamp_padding(radius, gray_orig) # executes clamp padding
        
        # Blurs the image using averaging filter
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
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
        unsharp_masked_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_unsharp_masked = ImageDraw.Draw(unsharp_masked_img)
        drawImage1DArray(self, img_result, draw_unsharp_masked, [])
        show_image(self, unsharp_masked_img, " ")
        variables.curr_img = unsharp_masked_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Unsharp masking is applied to the image", x=200, y=20, fill="white", font=("Arial", 9,))

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(img_result, 'Unsharp Masked Image Histogram'))

# Function that implements the Highboost filtering        
def highboost_filter(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(mask, neighbors):
        avg = 0
        for i in range(len(mask)):
            for j in range(len(mask[0])):
                avg += neighbors[i][j]*mask[i][j]
                
        return int(avg)       
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        radius = variables.n//2
        mask = [[1/(variables.n*variables.n) for i in range(variables.n)] for j in range(variables.n)]
        
        gray_orig = get_grayscale_img(self) # transforms image to grayscale
        
        flat_gray_orig = [element for row in gray_orig for element in row]
        blur_pixels = [row[:] for row in gray_orig]
        
        padded_img = clamp_padding(radius, gray_orig) # executes clamp padding
        
        # Blurs the image
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                blur_pixels[i][j] = get_pixel_value(mask, neighbors)

        # Creates output image
        highpass_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
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
                
        drawImage1DArray(self, img_result, draw_highboost,[])
            
        show_image(self, highpass_filtered_img, " ")
        variables.curr_img = highpass_filtered_img
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Highboost filter is applied to the image where the amplification parameter is 3.5", x=300, y=20, fill="white", font=("Arial", 9,))

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(img_result, 'Highboost Filtered Image Histogram'))

# Function that gets the neighboring pixels of a particular pixel in an image
# It also saves the passed pixel
def get_neighbors(row_index, column_index, radius, grid):
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
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        radius = variables.n//2
        mask = [[1/(variables.n*variables.n) for i in range(variables.n)] for j in range(variables.n)]
        
        if variables.isDegraded:
            gray = variables.degraded_image_data
        else:
            gray = get_grayscale_img(self) # transforms image to grayscale
        
        blur_pixels = [row[:] for row in gray] # copies gray pixel values to another array
        
        padded_img = clamp_padding(radius, gray) # executes clamp padding
        
        # Blurs the image
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                blur_pixels[i][j] = get_pixel_value(mask, neighbors)
        
        # Creates output image
        mdn_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_mdn_filtered = ImageDraw.Draw(mdn_filtered_img)
        
        drawImage(self, draw_mdn_filtered, blur_pixels)  
            
        show_image(self, mdn_filtered_img, " ")
        variables.curr_img = mdn_filtered_img
        variables.curr_image_data = blur_pixels
        
        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Median filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in blur_pixels for element in row]

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Median Filtered Image Histogram'))

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
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        n = 3
        radius = n//2
        mask = [ [0,1,0] , [1,-4,1] , [0,1,0] ] # Sobel Magnitude Operator
        
        gray = get_grayscale_img(self) # transforms image to grayscale
        
        copy = [row[:] for row in gray] # copies gray pixel values to another array
        
        padded_img = clamp_padding(radius, gray) # executes clamp padding
        
        # Blurs the image
        neighbors = []
        for i in range(variables.img_height):
            for j in range(variables.img_width):
                neighbors = get_neighbors(i+radius, j+radius, radius, padded_img)
                copy[i][j] = get_pixel_value(mask, neighbors)
        
        # Creates output image
        lapla_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_lapla_filtered = ImageDraw.Draw(lapla_filtered_img)
        
        drawImage(self, draw_lapla_filtered, copy) # Draws each pixel value to an image
            
        show_image(self, lapla_filtered_img, " ") # Shows image applied with laplacian filter
        variables.curr_img = lapla_filtered_img
        
        # Updates status bar
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Laplacian filter is applied to a {mask} kernel", x=250, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in copy for element in row]

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Laplacian Filtered Image Histogram'))

# Function for Gradient filter using Sobel Operator
def gradient_filter(self):
    if not variables.pcx_image_data:
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

        gray = get_grayscale_img(self) # transforms image to grayscale

        padded_img = clamp_padding(radius, gray) # implements clamp padding

        # Apply Sobel operator to the grayscale image with clamp padding
        sobel_result = sobelOperator(padded_img)

        # Creates output image
        grdn_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_grdn_filtered = ImageDraw.Draw(grdn_filtered_img)

        drawImage(self, draw_grdn_filtered, sobel_result) 

        show_image(self, grdn_filtered_img, " ")
        variables.curr_img = grdn_filtered_img

        # Updates status
        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Gradient filter using the Sobel edge detection is applied to the image", x=280, y=20, fill="white", font=("Arial", 9,))

        image_data = [element for row in sobel_result for element in row]

        # Call histogram function
        self.btn_hist.config(state="normal", command=lambda: show_histogram(image_data, 'Gradient Filtered Image Histogram'))

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
def clamp_padding(radius, gray):
    # Initializes rows and columns after padding
    padded_rows = variables.img_height + 2*radius
    padded_cols = variables.img_width + 2*radius
    
    # Create the padded array and implement clamp padding
    clamp_padded_img = [[0 for _ in range(padded_cols)] for _ in range(padded_rows)]

    # Copy the contents of the original array to the center of the padded array
    for i in range(variables.img_height):
        for j in range(variables.img_width):
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
            elif i >= variables.img_height + radius:
                # Clamp padding for the bottom border
                padded_i = variables.img_height + radius - 1
            else:
                padded_i = i

            if j < radius:
                # Clamp padding for the left border
                padded_j = radius
            elif j >= variables.img_width + radius:
                # Clamp padding for the right border
                padded_j = variables.img_width + radius - 1
            else:
                padded_j = j

            clamp_padded_img[i][j] = gray[padded_i - radius][padded_j - radius]
            
    return clamp_padded_img
