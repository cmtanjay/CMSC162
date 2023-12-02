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
    time.sleep(0.1)
    self.progress_var.set(value)
    self.progress_window.update()

    if value < 100:
        # Continue updating the progress bar until it reaches 100
        update_progress(self, value+5)
    else:
        time.sleep(3)
        close_progress(self)

def close_progress(self):
    # Function is done, destroy the progress window
    self.progress_window.destroy()
