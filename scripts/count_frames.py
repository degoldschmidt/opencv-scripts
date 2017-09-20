# import the necessary packages
from imutils.video import count_frames
import argparse
import os
import tkinter as tk
from tkinter import filedialog


tk.Tk().withdraw() ## remove window
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to input video file")
ap.add_argument("-o", "--override", type=int, default=-1, help="whether to force manual frame count")
args = vars(ap.parse_args())
if "video" not in args.keys() or args["video"] is None:
	video = filedialog.askopenfilename(title='Load video file', defaultextension='avi')
else:
	video = args["video"]
# count the total number of frames in the video file
override = False if args["override"] < 0 else True
total = count_frames(video, override=override)

# display the frame count to the terminal
print("[INFO] {:,} total frames read from {}".format(total,
	video[video.rfind(os.path.sep) + 1:]))
