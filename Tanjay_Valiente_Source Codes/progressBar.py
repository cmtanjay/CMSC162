# This is where the implementation of the progress bar is stored.
import tkinter as tk
from tkinter import ttk
import time

def update_progress(self, value):
    # Update the progress bar value
    time.sleep(0.1)
    self.progress_var.set(value)
    self.progress_window.update()

    if value < 100:
        # Continue updating the progress bar until it reaches 100
        update_progress(self, value+5)
    else:
        time.sleep(1)
        close_progress(self)

def close_progress(self):
    # Function is done, destroy the progress window
    self.progress_window.destroy()
