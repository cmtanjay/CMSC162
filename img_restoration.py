import variables
from img_ops import *
from img_enhancement import *
    
def maximum_filter(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(neighbors):        
        return max([element for row in neighbors for element in row])
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        radius = variables.n//2
        # mask = [[1/(variables.n*variables.n) for i in range(variables.n)] for j in range(variables.n)]
        
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

def minimum_filter(self):
    # Function that gets the average pixel value encompassed by an n x n mask
    def get_pixel_value(neighbors):        
        return min([element for row in neighbors for element in row])
    
    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        # Initializes the n x n mask
        radius = variables.n//2
        # mask = [[1/(variables.n*variables.n) for i in range(variables.n)] for j in range(variables.n)]
        
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

    if not variables.pcx_image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
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

        geo_filtered_img = Image.new('L', (variables.img_width, variables.img_height), 255)
        draw_geo_filtered = ImageDraw.Draw(geo_filtered_img)
        drawImage(self, draw_geo_filtered, data_2D)
        # print(data_2D)
        show_image(self, geo_filtered_img, " ")
        variables.curr_image_data = data_2D
        variables.curr_img = geo_filtered_img

        self.statusbar.destroy()
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=0.5, relief="groove")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        self.create_statusbar_canvas()
        self.add_text_to_statusbar(f"Status: Geometric mean filter is applied to the image on a {variables.n}x{variables.n} mask", x=220, y=20, fill="white", font=("Arial", 9,))

def contraharmonic_filter():
    print("Contraharmonic filter ni hihi")

def midpoint_filter():
    print("Midpoint filter eme")