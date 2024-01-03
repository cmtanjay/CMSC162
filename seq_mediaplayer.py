import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from glob import glob
import re

class ImageSequencePlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sequence Player")

        self.image_paths = []
        self.current_index = 0

        self.create_widgets()

    def create_widgets(self):
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.next_button = tk.Button(self.root, text="Next Image", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.prev_button = tk.Button(self.root, text="Previous Image", command=self.show_prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.close_button = tk.Button(self.root, text="Close", command=self.close_window)
        self.close_button.pack(side=tk.LEFT, padx=10)

    def load_image_sequence(self, directory):
        self.image_paths = sorted(glob(f"{directory}/*"), key=lambda x: int(re.search(r'\d+', x).group()))  # Change the extension based on your image format
        if not self.image_paths:
            print("No image files found in the directory.")
            return False
        return True

    def show_next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.show_image_with_transition()

    def show_prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.show_image_with_transition()

    def show_image_with_transition(self):
        self.show_image()
        self.root.after(50, self.show_next_image)

    def show_image(self):
        image_path = self.image_paths[self.current_index]
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
        self.video_label.img = img_tk
        self.video_label.config(image=img_tk)

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    player = ImageSequencePlayer(root)

    # Specify the directory containing the image sequence
    image_sequence_directory = filedialog.askdirectory()
    if player.load_image_sequence(image_sequence_directory):
        # player.show_image_with_transition()
        root.mainloop()
