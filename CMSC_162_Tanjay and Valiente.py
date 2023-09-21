from PIL import Image, ImageTk #pip install pillow
import tkinter as tk #pip install tk
from tkinter.filedialog import askopenfilename

# This is the class constructor for the Image Processing App
class App(tk.Tk):
    def __init__(self):
        super().__init__()

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
        self.statusbar = tk.Frame(self, height=30, bg="#2F333A", borderwidth=1, relief="solid")
        self.statusbar.grid(row=2, columnspan=3, sticky="ew")
        
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
        file_menu.add_command(label='Open...', command=self.open_file)
        file_menu.add_command(label='Close')
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
        
        # Configures open file button
        btn_open = tk.Button(self.sidebar, text="Open", command=self.open_file)
        btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
    # This is the function that opens the image file
    def open_file(self):
        filepath = askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.gif *.bmp *.jpeg *.tiff")])
        if not filepath:
            return

        # Opens the image using PIL
        image = Image.open(filepath)
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

        self.title(f"Image Viewer - {filepath}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
