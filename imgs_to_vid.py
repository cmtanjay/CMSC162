import cv2
import os
from tkinter import filedialog as ff

path = ff.askdirectory()
out_path = 'C:/Users/HAROLD/Documents/IVP/Opticalflow/video_res/'
out_video_name = 'res.mp4'
out_video_full_path = out_path+out_video_name

pre_imgs = os.listdir(path)
#print(pre_imgs)
img = []

for i in pre_imgs:
    i = path+'/'+i
    # print(i)
    img.append(i)

# print(img)

cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
print(img[0])
frame = cv2.imread(img[0])
size = list(frame.shape)
del size[2]
size.reverse()
# print(size)

video = cv2.VideoWriter(out_video_full_path, cv2_fourcc, 24, size) #output video name, fourcc, fps, size

for i in range(len(img)): 
    video.write(cv2.imread(img[i]))
    print('frame ', i+1, ' of ', len(img))

video.release()
print('outputed video to ', out_path)