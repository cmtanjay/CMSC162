import cv2
import numpy as np
from tkinter import filedialog as ff

# Use glob to get a list of image files in a directory
import glob
import re

path = ff.askdirectory()

# Load all images in the sequence
image_sequence = sorted(glob.glob(f"{path}/*"), key=lambda x: int(re.search(r'\d+', x).group()))

# Create a VideoWriter object for output video
height, width, _ = cv2.imread(image_sequence[0]).shape
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_video = cv2.VideoWriter("output.avi", fourcc, 10, (width, height))

# Read the first frame
frame1 = cv2.imread(image_sequence[0])
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

exit_flag = False

while not exit_flag:
    for image_path in image_sequence[1:]:
        frame2 = cv2.imread(image_path)
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Compute magnitude and angle of 2D vectors
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Set image hue according to the optical flow direction
        hsv[..., 0] = ang * 180 / np.pi / 2

        # Set image value according to the optical flow magnitude (normalized)
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

        # Convert HSV to BGR color representation
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Overlay the RGB image onto the optical flow visualization
        result = cv2.addWeighted(rgb, 0.5, frame2, 0.5, 0)

        # Display the result
        cv2.imshow('Optical Flow with Overlay', rgb)
        output_video.write(result)

        # Check for 'q' key to set exit_flag
        key = cv2.waitKeyEx(1)
        if key == ord('q') or key == 27:  # 'q' key or Esc key
            exit_flag = True
            break

        prvs = next

output_video.release()
cv2.destroyAllWindows()
