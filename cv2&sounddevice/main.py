from video_record_module import video_record
import os
import sounddevice as sd

#global variables to define
counter = 1
video_filename = "video_"+str(counter)+".mp4" #typically people use .avi or .mp4 file
video_length = 5
audio_filename = "audio_"+str(counter)+".wav"

# It looks like we always need to delete the wav file first or else there will be some problems with over-writing the sound file
if os.path.exists(audio_filename):
    os.remove(audio_filename)

video_record(video_filename, audio_filename, video_length)
