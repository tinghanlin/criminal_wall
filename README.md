# criminal_wall

![criminal_wall_teaser](https://github.com/user-attachments/assets/dd6a55a3-e985-44b6-bdb9-f932c78fd4c0)

## Introduction

The formal project name of this experience is **Between the Words**, created by Ting-Han (Timmy) Lin, Hanes Hsu, Charlotte Gilmore, Lade Tinubu, and Arlie Jackson.

With the popularity of digital games, social media, and other data-sharing platforms, more and more individuals’ information is tracked and used without users being aware. Often, people give companies information about themselves without knowing how that data may be shared or sold to other parties. Our exhibit aims to draw attention to this privacy issue - that too often, individuals are convinced to provide data about themselves, in seemingly legitimate ways, which companies may take advantage of and misuse the data. 

We captured this idea in our exhibit by creating a seemingly fun and lighthearted game, in a style inspired by the New York Times Dialect Quiz, to trick people into saying specific words. However, at the end of the experience, instead of using users’ data to guess their accent as we originally proposed, we reorganized and manipulated the recordings to make users appear to say silly things - in this case, the lyrics of Mary Had a Little Lamb. To conclude the experience, we presented users with this recording, as well as their likeness in a grid format with others’, to create a group announcement about data privacy. Our exhibit is particularly effective in that the “breach” of trust between users and data holders is revealed when it happens - we confront people at our exhibit right after their experience with the manipulated video. In the real world, people and their data are taken advantage of and may never know. 

We essentially built our own camera app from scratch to record people’s video and audio, to accompany a graphical user interface we designed to lead users through our “game”. After individuals’ recordings are taken, our code removes the silence from both ends of the recordings to create smooth transitions between words, for when the recordings are concatenated to make sentences.

## Physical Setup Instructions

This experience will be conducted using a MacOS laptop. Simply set the laptop on a desk and have the user sit in a chair positioned directly in front of it. To prevent the user from noticing they are being recorded during the experience, cover the green indicator light next to the webcam with black tape.

## How To Run The Code?

Our code is designed to be run with a **MacOS** (e.g., 14-inch MacBook Pro Apple M3 Chip) that has pre-installed **FFMpeg** (a free multimedia framework for video/audio processing, conversion, and streaming) and **VLC** (a free, open-source media player supporting diverse formats and streaming). Typically, FFMpeg already exists in MacOS but VLC does not. To download VLC, click [here](https://www.videolan.org/vlc/). Also, please ensure that your VLC is downloaded in your Applications. Once FFMpeg and VLC both exist in your MacOS, go through the following steps.

Git clone this repo and navigate to `criminal_wall` folder on the terminal, and delete and recreate a virtual environment (venv) by running the following code:
```python
rm -rf venv
python3 -m venv venv

source venv/bin/activate
```

If this is your first time running code in this repo, install these python packages and libraries by running the following code in your terminal:
```python
pip3 install numpy opencv-python scipy sounddevice pyqt6
```

Then, to launch the program, run the following code (e.g., `python3 main.py timmy`):
```python
python3 main.py [user_name] [--debug] 
```
Note: We did design a short debug mode using an optional command line flag. If you want to run that, use this command `python3 main.py timmy --debug`.

Also, if this is your first time running code in this repo, your terminal might prompt you to give permission to use your camera and microphone. Please give permission access to both. If this does happen, please restart by re-running the program again.

Once you are done, you can deactivate the venv by running the following command
```python
deactivate
```

If you can run the above code, but find that the webcam on the MacOS laptop constantly jumps to your IPhone's camera to record videos. You may want to disable continuity camera on your IPhone. If you don't know how to disable continuity camera on your IPhone, click [here](https://www.youtube.com/watch?v=Kopw8kTyc9c).

Often time this repo will be updated with new code, please git pull the latest code if you haven't tested with this repo for a while. If you are new to git pull, just navigate to `criminal_wall` folder on the terminal and run the following code:
```python
git pull
```

## System Overview

![system](https://github.com/user-attachments/assets/e1e323b6-91db-4426-a73f-7bba81c490f2)

## Description of Important File and Folder Names

### final.mp4
This file is the final concatenated video shown to the user at the end of the experience.

### debug folder
This folder stores all users' singing videos from the debug mode. 

### debug_psa1 folder
This folder stores all users' first PSA videos from the debug mode.

### debug_psa2 folder
This folder stores all users' second PSA videos from the debug mode.

### debug_psa1_adjust folder
This folder stores all users' first PSA videos that are adjusted to match the length of the current user's first PSA video from the debug mode. These videos are then used to generate the first group video.

### debug_psa2_adjust folder
This folder stores all users' second PSA videos that are adjusted to match the length of the current user's second PSA video from the debug mode. These videos are then used to generate the second group video.

### full_experience folder
This folder stores all users' singing videos from the full experience mode. 

### full_experience_psa1 folder
This folder stores all users' first PSA videos from the full experience mode.

### full_experience_psa2 folder
This folder stores all users' second PSA videos from the full experience mode.

### full_experience_psa1_adjust folder
This folder stores all users' first PSA videos that are adjusted to match the length of the current user's first PSA video from the full experience mode. These videos are then used to generate the first group video.

### full_experience_psa2_adjust folder
This folder stores all users' second PSA videos that are adjusted to match the length of the current user's second PSA video from the full experience mode. These videos are then used to generate the second group video.

### [user_name] folder
This folder stores all videos of the user saying each word. 

### assets folder
This folder stores the necessary figures and gifs to create the GUI. It also contains a video of the warning text, which is included in the final video.

## Finetune and Troubleshoot

### gui_module.py
- **self.video_length**: how many seconds we are recording for each clip
- **self.wait_time_for_video_generation**: how many seconds we will wait for generating the final video

### video_record_module.py
- **camera_index**: determine which camera to record. For example, 0 usually mean webcam for a MacBook.
- **silence_threshold**: determine what counts as silence. For example, -30dB means we consider anything below -30dB as silence. In a noisy environment, we can potentially increase this threshold to a higher level like -50dB.
- **silence_duration**: determine the minimal length of silence. For example, 0.1 means we only consider segments that are longer than 0.1 seconds as a silent segment.

### audio_record_module.py
- `sd.default.device = #`: during audio recording, sounddevice in Python will just choose a default microphone (usually MacBook's microphone is the default). If you want to change the source of the microphone, you can first `print(sd.query_devices())` and set `sd.default.device = #` to the index of that source of microphone.
  
### silence_detection_module.py
- If a user did not speak in the video recording, our current implementation is to just keep the first 0.1 second for the video so the program won't crash.

### video_edit_group_module.py
- How did we select users to fill up the surrounding videos in the group video? If the current user is the first user for this experience, the surrounding videos will all be that user. If there are less than 12 past users, we first fill up all past users to the surrounding videos and randomly select past users to fill up the remaining spots. If there are more than 12 past users, we select the latest 12 users excluding the current user. 
- If you want to include new media into the final video (e.g., updating the warning_text.mp4), you will need to call reencode_video() to re-encode it so that your new media will be able to be successfully concatenated by ffmpeg.

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

### video_edit_personal_module.py
- [How to draw text on video using ffmpeg?](https://stackoverflow.com/questions/17623676/text-on-video-ffmpeg)

### video_edit_group_module.py
- [How to Resize and Crop Videos using FFmpeg?](https://www.fastpix.io/blog/how-to-resize-and-crop-videos-using-ffmpeg#:~:text=If%20you%20want%20to%20crop,to%20calculate%20the%20center%20coordinates.&text=This%20command%20crops%20a%20640x360,\)%2F2%20as%20thestarting%20coordinates.)
- [How to get video duration in seconds?](https://superuser.com/questions/650291/how-to-get-video-duration-in-seconds)

