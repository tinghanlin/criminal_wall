from video_record_module import video_record
import os
import sounddevice as sd
import time

#global variables to define
counter = 1
video_filename = "video_"+str(counter)+".mp4" #typically people use .avi or .mp4 file
audio_filename = "audio_"+str(counter)+".wav"
video_length = 2
combine_filename = "combined_"+str(counter)+".mp4"
recorded_audio = []

if __name__ == "__main__":
    # It looks like we always need to delete the wav file first or else there will be some problems with over-writing the sound file
    if os.path.exists(video_filename):
        os.remove(video_filename)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
    if os.path.exists(combine_filename):
        os.remove(combine_filename)

    for i in range(74): #record 5 clips
        video_record(video_filename, audio_filename, video_length, combine_filename)
        counter +=1
    
        video_filename = "video_"+str(counter)+".mp4"
        audio_filename = "audio_"+str(counter)+".wav"
        combine_filename = "combined_"+str(counter)+".mp4"

    
