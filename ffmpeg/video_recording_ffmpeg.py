#Reference for python subprocess: https://www.geeksforgeeks.org/python-subprocess-module/
"""
Python Subprocess Call

subprocess.call() is a Python function within the subprocess module. 
It is employed to execute a command in a separate process and wait for its completion. 
The function returns a return code, which is typically zero for success and non-zero for failure. 
This function shares its arguments with subprocess.run(), such as 'args' for specifying the command to be executed, 
along with optional parameters like 'stdin', 'stdout', 'stderr', 'shell', 'cwd', and 'env'.

"""

#Reference for ffmpeg: https://trac.ffmpeg.org/wiki/Capture/Desktop
#More reference for ffmpeg: https://ffmpeg.org/ffmpeg-devices.html#avfoundation
#Some post about how to solve the crackling sound: https://stackoverflow.com/questions/65817212/crackling-sound-when-recording-audio-with-ffmpeg
#Another post with similar issues: https://superuser.com/questions/1601224/ffmpeg-with-blackhole-audio-crackling-noises-why
"""
macOS

ffmpeg -f avfoundation -list_devices true -i ""

The above command will enumerate all the available input devices including screens ready to be captured.
For example, 
in AVFoundation video devices, I have [0] FaceTime HD Camera, [1] Capture screen 0
in AVFoundation audio devices, I have [0] ZoomAudioDevice, [1] MacBook Pro Microphone

ffmpeg -f avfoundation -y -framerate 30 -video_size 1280x720 -i "0:1" -async 1 -t 5 video_recording_test.mp4



When you run these commands, you might need to go to Privacy $ Security, Screen & System Audio Recording, and allow terminal to audio record. 
"""

import subprocess

ffmpeg_command  = [
    "ffmpeg",
    "-f", "avfoundation",
    "-y",
    "-framerate", "30",
    "-video_size", "1280x720",
    "-i", "0:1",
    "-async", "1",
    "-t", "5",
    "video_recording_test.mp4"
]

return_code = subprocess.call(ffmpeg_command)

if return_code == 0:
    print("Command executed.")
else:
    print("Command failed.", return_code)

"""
Experiment note:
Video is good, but the audio is cracking right now.

"""