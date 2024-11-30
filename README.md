# criminal_wall

## System Overview

![Frame 3](https://github.com/user-attachments/assets/4132f19f-08e4-4cc5-9674-b0a9dd712781)

## Finetune and Troubleshoot

### main.py
- **video_length**: how many seconds we are recording for each clip
- **number_of_clips**: how many clips we are recording per time in a sequence

### video_record_module.py
- **camera_index**: determine which camera to record. For example, 0 usually mean webcam for a MacBook.
- **silence_threshold**: determine what counts as silence. For example, -30dB means we consider anything below -30dB as silence. In a noisy environment, we can potentially increase this threshold to a higher level like -25dB.
- **silence_duration**: determine the minimal length of silence. For example, 0.1 means we only consider segments that are longer than 0.1 seconds as a silent segment.

## What to Install?

To run this project, you might need to install the following tools.

- FFMpeg (this is a command line tool, follow this [video](https://www.youtube.com/watch?v=JSrIABa0IwY) if you haven't installed)
- Third-party Python libraries (``pip install numpy opencv-python scipy sounddevice``)

## References

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
