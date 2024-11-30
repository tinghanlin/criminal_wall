from video_record_module import video_record
import os
import sounddevice as sd
import time

###TODO: we might want to adjust these in the future###
video_length = 2 # in seconds
number_of_clips = 50
###TODO: we might want to adjust these in the future###

counter = 1
video_filename = "new_video_"+str(counter)+".mp4" #typically people use .avi or .mp4 file
audio_filename = "new_audio_"+str(counter)+".wav"
combine_filename = "new_combined_"+str(counter)+".mp4"
recorded_audio = []

if __name__ == "__main__":
    # It looks like we always need to delete the wav file first or else there will be some problems with over-writing the sound file
    if os.path.exists(video_filename):
        os.remove(video_filename)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
    if os.path.exists(combine_filename):
        os.remove(combine_filename)

    for i in range(number_of_clips):
        video_record(video_filename, audio_filename, video_length, combine_filename)
        counter +=1
    
        video_filename = "new_video_"+str(counter)+".mp4"
        audio_filename = "new_audio_"+str(counter)+".wav"
        combine_filename = "new_combined_"+str(counter)+".mp4"

    
