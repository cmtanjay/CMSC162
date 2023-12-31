# Importing all necessary libraries 
import cv2 
import os 
from tkinter import filedialog as ff

# Read the video from specified path 
filepath = ff.askopenfilename()

cam = cv2.VideoCapture(filepath) 

try: 
	
	# creating a folder named data 
	if not os.path.exists('data'): 
		os.makedirs('data') 

# if not created then raise error 
except OSError: 
	print ('Error: Creating directory of data') 

# frame 
currentframe = 0

f = []

while(True): 
	
	# reading from frame 
	ret,frame = cam.read() 

	if ret: 
		# if video is still left continue creating images 
		name = './data/frame' + str(currentframe) + '.bmp'
		print ('Creating...' + name) 
  
		f.append(frame)

		# writing the extracted images 
		# cv2.imwrite(name, frame) 

		# increasing counter so that it will 
		# show how many frames are created 
		currentframe += 1
	else: 
		break

print(f)

# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 
