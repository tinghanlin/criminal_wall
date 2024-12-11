import numpy as np
from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips,ImageClip
import subprocess
import os
import time
from pathlib import Path
import sys
from os.path import exists, join, basename, splitext
import numpy as np
import glob
import datetime


#start the timer
#add

def concat_with_ffmpeg(video_paths, output_path):
    try:
        with open('temp_inputs.txt', 'w') as f:
            for path in video_paths:
                escaped_path = path.replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
        
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', 'temp_inputs.txt',
            '-c', 'copy',  
            output_path,
            '-y'  
        ]
        
        print("Starting FFmpeg concatenation...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            raise Exception("FFmpeg concatenation failed")
        
        print("Concatenation successful!")
        
    finally:
        if os.path.exists('temp_inputs.txt'):
            os.remove('temp_inputs.txt')
def concat_with_moviepy(video_paths, output_path):
    """
    Alternative MoviePy method that handles audio differently.
    """
    clips = []
    try:
        for path in video_paths:
            video = VideoFileClip(path, audio=True)
            if video.audio is None:
                print(f"Warning: No audio found in {path}")
            clips.append(video)
        
        final_clip = concatenate_videoclips(
            clips,
            method="chain"
        )
        
        print("Exporting video...")
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio=True,
            audio_codec='aac',
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            audio_fps=44100
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    
    finally:
        for clip in clips:
            clip.close()
        if 'final_clip' in locals():
            final_clip.close()


def group_psa(my_video):
    my_video = VideoFileClip("timmy_output.mp4") #40 seconds
    width, height = my_video.size
    v1 = my_video[0].resize(height=180)   
    v2 = my_video[1].resize(height=180)  
    v3 = my_video[2].resize(height=180)  
    v4 = my_video[3].resize(height=180)  
    v5 = my_video[4].resize(height=180)
    cropped_clip_top_left = my_video[5].crop(x1=0, y1=0, x2=(width/2), y2=(height/2))  
    v6 = cropped_clip_top_left.resize(height=180)
    cropped_clip_top_right = my_video[5].crop(x1=(width/2), y1=0, x2=width, y2=(height/2))   
    v7 = cropped_clip_top_right.resize(height=180)  
    v8 = my_video[7].resize(height=180)  
    v9 = my_video[8].resize(height=180)  
    cropped_clip_bottom_left = my_video[5].crop(x1=0, y1=(height/2), x2=(width/2), y2=height)  
    v10 = cropped_clip_bottom_left.resize(height=180)  
    cropped_clip_bottom_right = my_video[5].crop(x1=(width/2), y1=(height/2), x2=width, y2=height) 
    v11 = cropped_clip_bottom_right.resize(height=180)  
    v12 = my_video[9].resize(height=180)  
    v13 = my_video[10].resize(height=180)  
    v14 = my_video[11].resize(height=180)  
    v15 = my_video[12].resize(height=180)  
    v16 = my_video[13].resize(height=180)

    # you might need some code here to make sure all videos are the same length
    my_video_array = clips_array([
        [v1, v2, v3, v4],
        [v5, v6, v7, v8],
        [v9, v10, v11, v12],
        [v13, v14, v15, v16]
    ])
    return my_video_array


def larger_psa(my_video):
    width, height = my_video[0].size
    v1 = my_video[1].resize(height=115)
    v2 = my_video[2].resize(height=115)
    v3 = my_video[3].resize(height=115)
    v4 = my_video[4].resize(height=115)
    v5 = my_video[5].resize(height=115)
    v6 = my_video[6].resize(height=115)
    v7 = my_video[7].resize(height=115)
    v8 = my_video[8].resize(height=115)
    cropped_clip_top_left = my_video[0].crop(x1=0, y1=0, x2=(width/2), y2=(height/2))  
    v9 = cropped_clip_top_left.resize(height=115)
    cropped_clip_top_right = my_video[0].crop(x1=(width/2), y1=0, x2=width, y2=(height/2))   
    v10 = cropped_clip_top_right.resize(height=115) 
    v11 = my_video[9].resize(height=115)
    v12 = my_video[10].resize(height=115)
    v13 = my_video[11].resize(height=115)
    v14 = my_video[12].resize(height=115)
    cropped_clip_bottom_left = my_video[0].crop(x1=0, y1=(height/2), x2=(width/2), y2=height)  
    v15 = cropped_clip_bottom_left.resize(height=115) 
    cropped_clip_bottom_right = my_video[0].crop(x1=(width/2), y1=(height/2), x2=width, y2=height) 
    v16 = cropped_clip_bottom_right .resize(height=115) 
    v17 = my_video[13].resize(height=115)
    v18 = my_video[14].resize(height=115) #.crop(x1 = cell[1][0][0],y1 = cell[0][0][1],x2 = cell[0][1][0],y2 = cell[0][1][1])
    v19 = my_video[15].resize(height=115)
    v20 = my_video[16].resize(height=115)
    v21 = my_video[17].resize(height=115)
    v22 = my_video[18].resize(height=115)
    v23 = my_video[19].resize(height=115)
    v24 = my_video[20].resize(height=115)

    my_video_array = clips_array([
        [v1, v2, v3, v4, v5, v6],
        [v7,v8, v9, v10, v11, v12],
        [v13, v14,v15, v16, v17, v18],
        [v19, v20, v21, v22, v23, v24]
    ])
    return my_video_array

def make_deep_audio(audio_training,output_path):


    # 90 percent this works but it fails becuase im on Unbutu will work on mac i think?

    #concat_with_ffmpeg(audio_training, "temp_audio_training_.mp4")
    #cmd = f"ffmpeg -i temp_audio_training_.mp4 -b:a 192K -vn audio_person_training.wav"
    #subprocess.run(cmd, capture_output=True, text=True)
    audio_psa("audio_person_training.wav",output_path)
    return 0 
    
def make_psa(out_path):

    files = glob.glob('./psa/1_part_psa_vids*')
    files.sort(key=os.path.getctime)
    files_2 = glob.glob('./psa/2_part_psa_vids*')
    files_2.sort(key=os.path.getctime)
    clips_1 = []
    clips_2 = []

    for i in range(22):
        clips_1.append(VideoFileClip(files[i]))
        clips_2.append(VideoFileClip(files_2[i]))

    frist_st_part = larger_psa(clips_1)
    second_nd_part_psa =  larger_psa(clips_2)
    word_pt_1 = ImageClip("assets/psa_word_pt_1.png").set_duration(15)
    word_pt_2 = ImageClip("assets/psa_word_pt_2.png").set_duration(15)
    clips = [frist_st_part,word_pt_1,word_pt_2 , second_nd_part_psa]
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(out_path, fps=24)


start_time = time.time()

# for the 1st part of psa
video_paths = [ "./new_combined_30_no_silence_concat.mp4", "./new_combined_16_no_silence_concat.mp4",
"./new_combined_18_no_silence_concat.mp4", "./new_combined_10_no_silence_concat.mp4", "./new_combined_17_no_silence_concat.mp4", "./new_combined_34_no_silence_concat.mp4", "./new_combined_14_no_silence_concat.mp4", "./new_combined_37_no_silence_concat.mp4" ]
output_path = f"psa/1_part_psa_vids{datetime.datetime.now()}.mp4"
concat_with_moviepy(video_paths,output_path)

# IF ffmpeg is better
#output_path = f"psa/1_part_psa_vids{datetime.datetime.now()}_2.mp4"
#concat_with_ffmpeg(video_paths, output_path)

# for the last part of psa
video_paths = [ "new_combined_23_no_silence_concat.mp4","new_combined_46_no_silence_concat.mp4",
"new_combined_23_no_silence_concat.mp4",
"new_combined_48_no_silence_concat.mp4",
"new_combined_23_no_silence_concat.mp4","new_combined_50_no_silence_concat.mp4"]
output_path = f"psa/2_part_psa_vids{datetime.datetime.now()}.mp4"
concat_with_moviepy(video_paths,output_path)

output_path = f"psa_final_no_words.mp4"
make_psa(output_path)

end_time = time.time()
elapsed_time = end_time - start_time
print("Time taken is: ", round(elapsed_time), " seconds!") # it takes 19 seconds to run this