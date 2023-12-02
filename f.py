import tkinter as tk
from tkinter import ttk
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Progress Bar Example")

        # Create a progress bar variable
        self.progress_var = tk.DoubleVar()

        # Create a Start button
        start_button = tk.Button(root, text="Start", command=self.start_function)
        start_button.pack(pady=10)

    def start_function(self):
        # Create a progress window
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Progress")

        # Create a progress bar in the progress window
        self.progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10)

        # Call the function with an after delay to start updating the progress bar
        self.root.after(100, self.update_progress, 0)
        # Simulate some work being done in your actual function
        self.root.after(1000, self.simulated_work)

    def update_progress(self, value):
        # Update the progress bar value
        self.progress_var.set(value)

        if value < 100:
            # Continue updating the progress bar until it reaches 100
            self.root.after(100, self.update_progress, value + 5)
            # print("j")
        else:
            # Function is done, initiate the closing process
            # self.root.after(100, self.update_progress, 100)
            self.root.after(3000, self.close_progress)

    def simulated_work(self):
        # Simulate your actual function logic here
        # ...
        time.sleep(5)
        # Once the work is done, set the progress bar to its maximum value
        self.root.after(100, self.update_progress, 100)

    def close_progress(self):
        # Function is done, destroy the progress window
        self.progress_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
