# #Reference: https://www.codingforentrepreneurs.com/blog/how-to-record-video-in-opencv-python
# #Refrence: https://www.youtube.com/embed/1eHQIu4r0Bc

# import numpy as np
# import os
# import cv2
# import time

# # Set resolution for the video capture
# # Function adapted from https://kirr.co/0l6qmh
# def change_res(cap, width, height):
#     cap.set(3, width)
#     cap.set(4, height)

# # Standard Video Dimensions Sizes
# STD_DIMENSIONS =  {
#     "480p": (640, 480),
#     "720p": (1280, 720), #width and height (pixels)
#     "1080p": (1920, 1080),
#     "4k": (3840, 2160),
# }

# # grab resolution dimensions and set video capture to it.
# def get_dims(cap):
#     width,height = STD_DIMENSIONS["720p"]
#     ## change the current caputre device
#     ## to the resulting resolution
#     change_res(cap, width, height)
#     return width, height

# # Video Encoding, might require additional installs
# # Types of Codes: http://www.fourcc.org/codecs.php
# VIDEO_TYPE = {
#     'avi': cv2.VideoWriter_fourcc(*'XVID'),
#     #'mp4': cv2.VideoWriter_fourcc(*'H264'),
#     'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
# }

# def get_video_type(filename):
#     filename, ext = os.path.splitext(filename)
#     if ext in VIDEO_TYPE:
#       return  VIDEO_TYPE[ext]
#     return VIDEO_TYPE['avi']

# def video_record(filename, video_length):

#     cap = cv2.VideoCapture(0)
#     out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap))

#     start_time = time.time()

#     while True:
#         ret, frame = cap.read()
#         out.write(frame)
#         #cv2.imshow('frame',frame)

#         if time.time() - start_time > video_length:
#             break

#         # if cv2.waitKey(1) & 0xFF == ord('q'):
#         #     break

#     cap.release()
#     out.release()
#     #cv2.destroyAllWindows()
#     print("done video taping!")


#Reference: https://www.codingforentrepreneurs.com/blog/how-to-record-video-in-opencv-python
#Refrence: https://www.youtube.com/embed/1eHQIu4r0Bc

import numpy as np
import os
import cv2
import time
import sounddevice as sd
from scipy.io.wavfile import write
from audio_record_module import audio_record
import threading

audio_filename = "output1.wav"
audio_length = 5

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720), #width and height (pixels)
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# grab resolution dimensions and set video capture to it.
def get_dims(cap):
    width,height = STD_DIMENSIONS["720p"]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

def video_record(filename, video_length):

    cap = cv2.VideoCapture(0)
    fps=30
    out = cv2.VideoWriter(filename, get_video_type(filename), fps, get_dims(cap))
    total_frames = int(video_length * fps)
    frames_recorded = 0

    #Note: so audio recording has no problem
    #Video recording needs to match audio. I did that by adjust the frame per second.
    audio_thread = threading.Thread(target=audio_record, args=(audio_filename,audio_length))
    audio_thread.start()

    while frames_recorded < total_frames:
        ret, frame = cap.read()
        out.write(frame)
        #cv2.imshow('frame',frame)
        frames_recorded += 1
    
    cap.release()
    out.release()
    #cv2.destroyAllWindows()
    print("done video taping!")
