import tkinter as tk
from tkinter import ttk
import time

def start_function(self):
    # Create a progress window
    self.progress_window = tk.Toplevel(self)
    self.progress_window.title("Progress")

    # Create a progress bar in the progress window
    self.progress_bar = ttk.Progressbar(self.progress_window, variable=self.progress_var, maximum=100)
    self.progress_bar.pack(pady=10)

    # Call the function with an after delay to start updating the progress bar
    self.after(100, update_progress(self, 0))
    # Simulate some work being done in your actual function

def update_progress(self, value):
    # Update the progress bar value
    self.progress_var.set(value)

    if value < 100:
        # Continue updating the progress bar until it reaches 100
        self.after(100, update_progress(self, value+5))
        # print("j")
    else:
        # Function is done, initiate the closing process
        # self.root.after(100, self.update_progress, 100)
        self.after(3000, close_progress(self))

def simulated_work(self):
    # Simulate your actual function logic here
    # ...
    time.sleep(5)
    # Once the work is done, set the progress bar to its maximum value
    self.after(100, self.update_progress, 100)

def close_progress(self):
    # Function is done, destroy the progress window
    self.progress_window.destroy()
