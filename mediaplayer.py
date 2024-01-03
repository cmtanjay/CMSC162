import cv2
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")

        self.cap = None
        self.total_frames = 0
        self.fps = 0
        self.elapsed_time = 0
        self.start_time = 0
        self.paused = False

        self.create_widgets()

    def create_widgets(self):
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.play_button = tk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_video)
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.close_button = tk.Button(self.root, text="Close", command=self.close_video)
        self.close_button.pack(side=tk.LEFT, padx=10)

    def play_video(self):
        filepath = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
        if filepath:
            self.cap = cv2.VideoCapture(filepath)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.elapsed_time = 0
            self.start_time = time.time()
            self.paused = False

            self.update_video()

    def update_video(self):
        success, frame = self.cap.read()

        if success:
            if not self.paused:
                # Convert frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert frame to PhotoImage
                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(img)
                # Update label with the new frame
                self.video_label.img = img_tk
                self.video_label.config(image=img_tk)

                current_time = time.time() - self.start_time
                self.elapsed_time = int(current_time)
                total_time = self.total_frames // self.fps

                print(f"Elapsed Time: {self.elapsed_time} seconds / Total Time: {total_time} seconds", end='\r')

            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.total_frames - 1:
                # Video has reached the end, restart it
                self.restart_video()
            else:
                self.root.after(25, self.update_video)  # Update every 25 milliseconds
        else:
            self.cap.release()

    def pause_video(self):
        self.paused = not self.paused

    def restart_video(self):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.start_time = time.time()
            self.update_video()

    def close_video(self):
        if self.cap:
            self.cap.release()
            self.video_label.config(image=None)

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
