import cv2
import tkinter as tk
from tkinter import filedialog


#tk.Tk().withdraw() ## remove window
filename = filedialog.askopenfilename(title='Load video file', defaultextension='avi')

cap = cv2.VideoCapture(filename)
while not cap.isOpened():
    cap = cv2.VideoCapture(filename)
    cv2.waitKey(1000)
    print("Wait for the header")

num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
num_dropped = 0 # number of dropped frames
frame_ix = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
frame_t = cap.get(cv2.CAP_PROP_POS_MSEC)
print(num_frames, "frames found in file.")
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("(width, height):", (w,h))
while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        #cv2.imshow('video', frame)
        diff = (cap.get(cv2.CAP_PROP_POS_MSEC) - frame_t) * 0.001 ### ms = 10^-3 s
        ifps = 1/diff
        if cap.get(cv2.CAP_PROP_POS_FRAMES) != frame_ix + 1:
            num_dropped += 1
        frame_ix = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        frame_t = cap.get(cv2.CAP_PROP_POS_MSEC)

        if diff > 0.02:
            print("drop!")

        if int(frame_ix%36000) == 0:
            print("{}%: {} frames dropped".format(100*frame_ix/num_frames, int(num_dropped)))
        #print(str(pos_frame),"frames")
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        print("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if frame_ix == num_frames:
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        print("# dropped frames:", num_dropped)
        break
