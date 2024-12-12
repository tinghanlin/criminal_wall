#Reference: https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html
# The code will record sound and separate them into chunks

#python3 dynamic_audio_record.py

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import threading
import time
import csv

recorded_audio = []
counter = 0
FILENAME = "output"+str(counter)+".wav"
audio_length = 5 #5 seconds
threads = []
t = None
stop_flag = "FALSE"

def startRecord():
    global counter, FILENAME, recorded_audio, audio_length, t, stop_flag

    # with open('shared_data.csv', newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in spamreader: 
    #             stop_flag = row[0]
    counter+=1
    FILENAME = "output"+str(counter)+".wav"
    recorded_audio = []
    t = threading.Timer(audio_length, startRecord)
    t.start()

    print("Recording")
    userDefinedAudioRecord(FILENAME, recorded_audio)

    # if stop_flag == "TRUE":
    #     t.cancel()
    
    
def callback(indata, frames, time, status):
    if status:
        print ("recording error: ", status)
    recorded_audio.append(indata.copy())

def userDefinedAudioRecord(fileName, recorded_audio):
    global audio_length
    stream = sd.InputStream(callback=callback, dtype = "float32", samplerate=48000, channels=1)
    stream.start()

    # input() #when I want to stop
    # print ("record is done")
    #time.sleep(audio_length)
    time.sleep(audio_length)

    stream.stop()
    stream.close()

    recorded_audio = np.concatenate(recorded_audio)

    audio_data = recorded_audio.flatten()

    # save audio to file
    write(fileName, 48000, audio_data)


if __name__ == "__main__":

    # It looks like we always need to delete the wav file first or else there will be some problems with over-writing the sound file
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

    startRecord()
    


