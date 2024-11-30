#Reference: https://www.codingforentrepreneurs.com/blog/how-to-record-video-in-opencv-python
#Refrence: https://www.youtube.com/embed/1eHQIu4r0Bc
import numpy as np
import os
import cv2
from scipy.io.wavfile import write
from audio_record_module import audio_record
from silence_detection_module import slience_remove
import threading

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

def video_record(video_filename, audio_filename, video_length, combine_filename):

    ###TODO: we might want to adjust these in the future###
    camera_index = 0 #Here we assume index 0 is the webcam
    ###TODO: we might want to adjust these in the future###
    cap = cv2.VideoCapture(camera_index)

    fps=30 #webcam defaults to 30 fps (even though cv2.VideoWriter uses 24 fps)
    out = cv2.VideoWriter(video_filename, get_video_type(video_filename), fps, get_dims(cap))
    total_frames = int(video_length * fps)
    frames_recorded = 0

    #we start audio recording thread here
    audio_thread = threading.Thread(target=audio_record, args=(video_filename, audio_filename, video_length, combine_filename))
    audio_thread.start()

    while frames_recorded < total_frames:
        ret, frame = cap.read()
        out.write(frame)
        #cv2.imshow('frame',frame)
        frames_recorded += 1
    
    cap.release()
    out.release()
    #cv2.destroyAllWindows()

    #wait for audio thread is done
    audio_thread.join()

    print("done video taping!")

    #call silence remove
    ###TODO: we might want to adjust these in the future###
    silence_threshold = "-30dB"
    silence_duration = "0.1"
    ###TODO: we might want to adjust these in the future###
    slience_remove(combine_filename, silence_threshold, silence_duration, video_length)
    
