# This is where the variables necessary for the functioning of all image processing techniques are stored.
orig_img = None
curr_img = None
red_channel = []
green_channel = []
blue_channel = []
pcx_image_data = [] #orig image data
image_data = []
curr_image_data = []
palette = []
isDegraded = False
degraded_image_data = []
n = 3

manufacturer = None
version = None
encoding = None
bits_per_pixel = 0
img_width = 0
img_height = 0
hdpi = 0
vdpi = 0
nplanes = 0
bytesperline = 0
paletteinfo = 0

video_filepath = None
orig_video_filepath = None

file_type = None #1 for image, 2 for image sequence, 3 for video
image_paths = None

is_filtered = None

# Image sequences
prev_btn = None
next_btn = None
play_imgs_button = None
reset_button = None
img_seq = []