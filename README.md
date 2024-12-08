# criminal_wall

## How to run the code using the virtual environment?

Navigate to `criminal_wall` folder, and delete and recreate a venv by running the following code:
```python
rm -rf venv
python3 -m venv venv

source venv/bin/activate
python3 main.py [user_name] [--debug] 
```

Note: We designed a short debug mode. If you want to run that, use this command `python3 main.py timmy --debug`.
Otherwise. If you want the full experience, use this command `python3 main.py timmy`.

You might need to install some python packages. If so, you can run the following code:
```python
pip3 install numpy opencv-python scipy sounddevice pyqt6 moviepy==1.0.3
```

Once you are done, you can deactivate the venv by running the following command
```python
deactivate
```

## System Overview

![Frame 3 (2)](https://github.com/user-attachments/assets/b86a6642-10c6-4275-84bd-b5579bec310b)


## Finetune and Troubleshoot

### gui_module.py
- **self.video_length**: how many seconds we are recording for each clip

### audio_record_module.py
- `sd.default.device = #`: during audio recording, sounddevice in Python will just choose a default microphone (usually MacBook's microphone is the default). If you want to change the source of the microphone, you can first `print(sd.query_devices())` and set `sd.default.device = #` to the index of that source of microphone.
  
### video_record_module.py
- **camera_index**: determine which camera to record. For example, 0 usually mean webcam for a MacBook.
- **silence_threshold**: determine what counts as silence. For example, -30dB means we consider anything below -30dB as silence. In a noisy environment, we can potentially increase this threshold to a higher level like -50dB.
- **silence_duration**: determine the minimal length of silence. For example, 0.1 means we only consider segments that are longer than 0.1 seconds as a silent segment.

### PSA VIDEO - status
I know Blaze wanted us experiment with deep fakes So I coded the PSA to include the "user's voice" Using an AI cloning package but on my computer in order to get the cloning package to work I had to downgrade to python 3.9 ( it says on the website it works with python 3.11 but I'm unsure if it's only 3.11 0  it wouldn't work with my Python and I'm on 3.11.0) Which required me to downgrade movie.py.
(PSA.py  (Verson with deep fake)- runs on python 3.9)
(PSA_no_words.py(Verson with no deep fake) - runs on python 3.11.5)
in terms of storage (All things saved in the main directory (where the raw videos went) Can be deleted after each user )
Everything stored in the psa/ folder should be kept, that's where we store the multiple users in order to create the grid effect.
in the end I used movie.py has it was easier to do the grid and provided two different scale versions let me know if I should switch to ffmpeg 
The speed even with all the additions on my computer was about the same because it was before all the changes I made to Tommy's code so I assume it should still run at the same speed.

## What to Install?

To run this project, you might need to install the following tools in the 

- FFMpeg
- Third-party Python libraries (e.g., ``pip3 install numpy opencv-python scipy sounddevice pyqt6 moviepy==1.0.3``)
- VLC video player

## References

### main.py
- [How to use argparse?](https://docs.python.org/3/library/argparse.html)

### gui_module.py
- [How to use PyQt's QThread to Prevent Freezing GUIs?](https://realpython.com/python-pyqt-qthread/)
- [How to create your first app with PyQt6](https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/)

### audio_record_module.py

- [How to use sounddevice to record audio?](https://python-sounddevice.readthedocs.io/en/0.3.15/api/streams.html)
- [How to merrge audio and video files with FFmpeg?](https://www.mux.com/articles/merge-audio-and-video-files-with-ffmpeg)

### video_record_module.py

- [How to Record Video in OpenCV & Python?](https://www.codingforentrepreneurs.com/blog/how-to-record-video-in-opencv-python)
- [How to Record Video in OpenCV & Python on Youtube?](https://www.youtube.com/embed/1eHQIu4r0Bc)

### silence_detection_module.py

- [How to retrieve the output of subprocess in Python?](https://www.geeksforgeeks.org/retrieving-the-output-of-subprocesscall-in-python/)
- [How to use Python RegEx?](https://www.w3schools.com/python/python_regex.asp#findall)
- [How to truncate video using ffmpeg?](https://stackoverflow.com/questions/18444194/cutting-multimedia-files-based-on-start-and-end-time-using-ffmpeg)
- [How to remove the silent parts of a video using ffmpeg and Python?](https://www.youtube.com/watch?v=ak52RXKfDw8)
- [How to concatenate video using ffmpeg?](https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg)
