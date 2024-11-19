#Reference: https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html
#Reference: https://www.mux.com/articles/merge-audio-and-video-files-with-ffmpeg
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import threading
import time
import csv
import subprocess

recorded_audio = []

def callback(indata, frames, time, status):
    if status:
        print ("recording error: ", status)
    recorded_audio.append(indata.copy())

def audio_record(video_filename, audio_filename, audio_length, combine_filename):
    global recorded_audio
    #Uncomment below if you want to see the list of all available audio devices
    #print(sd.query_devices())
    audio_sample_rate = 48000
    stream = sd.InputStream(callback=callback, dtype = "float32", samplerate=audio_sample_rate, channels=1)
    stream.start()

    start_time = time.time()
    while time.time() - start_time < audio_length:
        time.sleep(0.1)

    stream.stop()
    stream.close()

    recorded_audio = np.concatenate(recorded_audio)

    #Since the audio file might not be precisely # seconds, we will handle it by the following 
    total_samples = audio_length * audio_sample_rate

    if recorded_audio.shape[0] > total_samples:
        # we will truncate the audio file if it exceeds # seconds
        print("audio is longer than video!")
        recorded_audio = recorded_audio[:total_samples] 

    elif recorded_audio.shape[0] < total_samples:
        #pad by adding silence the audio file if it is under # seconds
        print("audio is shorter than video!")

        sample_difference = total_samples - recorded_audio.shape[0]
        silence = np.zeros((sample_difference, 1), dtype=recorded_audio.dtype)
        recorded_audio = np.concatenate((recorded_audio, silence))
    else:
        print("audio has the exactly same length as video!")

    audio_data = recorded_audio.flatten()

    #save audio to file
    write(audio_filename, audio_sample_rate, audio_data)

    #wait for video mp4 file to be generated
    time.sleep(1)

    #join the video file and the audio file
    command = [
        "ffmpeg",
        "-y",
        "-i", video_filename,
        "-i", audio_filename,
        "-c:v", "copy",        
        "-c:a", "aac",
        combine_filename
    ]

    # Run the command
    subprocess.run(command, check=True)
    recorded_audio = []




    
    


