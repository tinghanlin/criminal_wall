#Reference: https://www.fastpix.io/blog/how-to-resize-and-crop-videos-using-ffmpeg#:~:text=If%20you%20want%20to%20crop,to%20calculate%20the%20center%20coordinates.&text=This%20command%20crops%20a%20640x360,)%2F2%20as%20thestarting%20coordinates.
#Reference: https://superuser.com/questions/650291/how-to-get-video-duration-in-seconds
import subprocess
import os
import time
import glob
import random

def top_left_video(input_filename, output_filename):

    ffmpeg_command = [
    "ffmpeg",
    "-i", input_filename,
    "-y",
    "-filter:v", 
    "crop=iw/2:ih/2:0:0",
    "-s", "1280x720",
    output_filename
    ]

    subprocess.run(ffmpeg_command, check=True)

def top_right_video(input_filename, output_filename):

    ffmpeg_command = [
    "ffmpeg",
    "-i", input_filename,
    "-y",
    "-filter:v", 
    "crop=iw/2:ih/2:iw/2:0",
    "-s", "1280x720",
    output_filename
    ]

    subprocess.run(ffmpeg_command, check=True)

def bottom_left_video(input_filename, output_filename):

    ffmpeg_command = [
    "ffmpeg",
    "-i", input_filename,
    "-y",
    "-filter:v", 
    "crop=iw/2:ih/2:0:ih/2",
    "-s", "1280x720",
    output_filename
    ]

    subprocess.run(ffmpeg_command, check=True)

def bottom_right_video(input_filename, output_filename):

    ffmpeg_command = [
    "ffmpeg",
    "-i", input_filename,
    "-y",
    "-filter:v", 
    "crop=iw/2:ih/2:iw/2:ih/2",
    "-s", "1280x720",
    output_filename
    ]

    subprocess.run(ffmpeg_command, check=True)

#path_to_folder: stores all of the candidate videos
def select_surrounding_videos(path_to_folder):
    #assume we are going with 4x4 psa grid and the middle 4 is the current user
    #we will need to select 12 surrounding videos
    clips = []
    files = glob.glob(f'{path_to_folder}/*') #path_to_folder can be full_experience_psa1/*
    files.sort(key=os.path.getctime,reverse=True) # we are getting the latest videos
    number_of_videos = len(files)
    print("number_of_videos: ", number_of_videos)

    if number_of_videos <= 12:
        print("We have <= 12 videos!")
        #fill up all the existing videos into the grid, and random fill up the remaining grids with the existing videos
        for i in range(number_of_videos):
            clips.append(files[i])

        for i in range(12-number_of_videos):
            clips.append(files[random.randint(0, number_of_videos-1)])
    
    else: #number of videos > 12
        print("We have more than 12 videos!")
        #pick 12 videos (excluding the current user)
        for i in range(12):
            #since we already order the files by time, we can use +1 to skip the current user
            clips.append(files[i+1]) 
        
    return clips
    
def get_video_length_in_seconds(center_video_filename):
    ffprobe_command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        center_video_filename
    ]

    result = subprocess.run(ffprobe_command, capture_output=True, text=True)
    #print("Return code:", result.returncode)
    print("Output:", result.stdout)
    #print("Error:", result.stderr)
    video_length_in_seconds =  result.stdout
    
    return float(video_length_in_seconds)

"""
TODO: The current implementation will try to adjust all files in the folder to match the 
length of the current user's video. This means it will take more and more time to run this 
program as we have more users experiencing our project. Future work will need to solve this problem.
Perhaps, by only adjust the latest 12 videos (excluding the current user).
"""
def adjust_videos_to_center_video_length(path_to_folder, center_video_filename):

    files = glob.glob(f"{path_to_folder}/*") #path_to_folder can be full_experience_psa1/*
    files.sort(key=os.path.getctime, reverse=True)
    number_of_videos = len(files)

    center_video_length = get_video_length_in_seconds(center_video_filename)

    for side_video_filename in files:
        side_video_length = get_video_length_in_seconds(side_video_filename)
        parts = side_video_filename.split("/")
        output_filename = parts[1]
    
        if side_video_length >= center_video_length:
            #this surrounding video is too long, so we need to truncate it
            print("surrounding video is too long!")
            ffmpeg_command = [
                "ffmpeg",
                "-i", side_video_filename,
                "-y",
                "-t", str(center_video_length),
                "-c:v", "libx264", "-c:a", "aac", 
                f"{path_to_folder}_adjusted/{output_filename}"
            ]
            subprocess.run(ffmpeg_command, check=True)
        else:
            #this surrounding video is too short, so we need to pad it such that it loops on itself a little bit more
            print("surrounding video is too short!")
            pad_time = str(center_video_length - side_video_length)

            ffmpeg_command = [
                "ffmpeg",
                "-i", side_video_filename,
                "-y",
                "-vf", f"tpad=stop_mode=clone:stop_duration={pad_time}",
                "-t", str(center_video_length),
                "-copyts",
                "-c:v", "libx264", "-c:a", "aac",
                f"{path_to_folder}_adjusted/{output_filename}"
            ]
            subprocess.run(ffmpeg_command, check=True)

def video_4x4(path_to_folder, top_left_filename, top_right_filename, bottom_left_filename, bottom_right_filename, output_filename):
    #start the timer
    start_time = time.time()
    
    clips = select_surrounding_videos(path_to_folder)

    ffmpeg_command = [
        "ffmpeg",
        "-i", clips[0], #0
        "-i", clips[1], #1
        "-i", clips[2], #2
        "-i", clips[3], #3
        "-i", clips[4], #4
        "-i", top_left_filename, #5 (top left)
        "-i", top_right_filename, #6 (top right)
        "-i", clips[5], #7 
        "-i", clips[6], #8
        "-i", bottom_left_filename, #9 (bottom left)
        "-i", bottom_right_filename, #10 (bottom right)
        "-i", clips[7], #11 
        "-i", clips[8], #12
        "-i", clips[9], #13
        "-i", clips[10], #14
        "-i", clips[11], #15
        "-filter_complex", 
        "[0:v][1:v][2:v][3:v]hstack=inputs=4[r1];"
        "[4:v][5:v][6:v][7:v]hstack=inputs=4[r2];"
        "[8:v][9:v][10:v][11:v]hstack=inputs=4[r3];"
        "[12:v][13:v][14:v][15:v]hstack=inputs=4[r4];"
        "[r1][r2][r3][r4]vstack=inputs=4[vout];"
        "[0:a][1:a][2:a][3:a][4:a][5:a][6:a][7:a][8:a][9:a][10:a][11:a][12:a][13:a][14:a][15:a]amix=inputs=16:duration=longest[aout]",
        "-map", "[vout]",
        "-map", "[aout]",
        "-y",
        "-s", "1280x720",
        output_filename
    ]
    subprocess.run(ffmpeg_command, check=True)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Time taken is: ", elapsed_time, " seconds!")

#example usage: reencode_video("assets/warning_text.mp4", "assets/warning_text_reencoded.mp4")
def reencode_video(input_filename, output_filename):
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i", input_filename,
        "-c:v", "libx264",  
        "-preset", "fast",
        "-crf", "23",
        "-r", "30",
        "-c:a", "aac",
        "-strict", "2",
        output_filename
    ]
    subprocess.run(ffmpeg_command, check=True)

def final_concatenation(user_name, debug_flag):
    #let's re-encode all videos
    #You can also reencode warning_text.mp4 here if you haven't done it yet!
    if debug_flag == True:
        reencode_video(f"debug/sing_subtitled_{user_name}.mp4", f"debug/sing_subtitled_{user_name}_reencoded.mp4")
        reencode_video("debug_psa1_subtitled_group.mp4", "debug_psa1_subtitled_group_reencoded.mp4")
        reencode_video("debug_psa2_subtitled_group.mp4", "debug_psa2_subtitled_group_reencoded.mp4")
    else:
        reencode_video(f"full_experience/sing_subtitled_{user_name}.mp4", f"full_experience/sing_subtitled_{user_name}_reencoded.mp4")
        reencode_video("full_experience_psa1_subtitled_group.mp4", "full_experience_psa1_subtitled_group_reencoded.mp4")
        reencode_video("full_experience_psa2_subtitled_group.mp4", "full_experience_psa2_subtitled_group_reencoded.mp4")

    #sing + group_psa1 + warning_message + group_psa2
    with open('video_list_to_concatenate.txt', 'w') as f:

        if debug_flag == True:
            f.write(f"file 'debug/sing_subtitled_{user_name}_reencoded.mp4'\n")
            f.write(f"file 'debug_psa1_subtitled_group_reencoded.mp4'\n")
            f.write(f"file 'assets/warning_text_reencoded.mp4'\n")
            f.write(f"file 'debug_psa2_subtitled_group_reencoded.mp4'\n")

        else:
            f.write(f"file 'full_experience/sing_subtitled_{user_name}_reencoded.mp4'\n")
            f.write(f"file 'full_experience_psa1_subtitled_group_reencoded.mp4'\n")
            f.write(f"file 'assets/warning_text_reencoded.mp4'\n")
            f.write(f"file 'full_experience_psa2_subtitled_group_reencoded.mp4'\n")
    
    #concatenate the vidoes together into one video
    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "video_list_to_concatenate.txt",
        "-c:v", "libx264",
        "-c:a", "aac",
        "final.mp4"
    ]
    print("final ffmpeg commands: ", command)
    # run the command
    subprocess.run(command, check=True)

def video_edit_full(user_name, debug_flag):
    start_time = time.time()

    if debug_flag == True:
 
        #generate debug psa1
        top_left_video(f"debug_psa1/psa1_{user_name}.mp4", f"debug/top_left_psa1_{user_name}.mp4")
        top_right_video(f"debug_psa1/psa1_{user_name}.mp4", f"debug/top_right_psa1_{user_name}.mp4")
        bottom_left_video(f"debug_psa1/psa1_{user_name}.mp4", f"debug/bottom_left_psa1_{user_name}.mp4")
        bottom_right_video(f"debug_psa1/psa1_{user_name}.mp4", f"debug/bottom_right_psa1_{user_name}.mp4")
        
        #adjust all other surrounding videos to the video length of f"debug_psa1/psa1_{user_name}.mp4"
        #we need to do this step because not all users have same the length for their psa1 and psa2
        adjust_videos_to_center_video_length("debug_psa1", f"debug_psa1/psa1_{user_name}.mp4")
        #after this step, inside of debug_psa1_adjusted folder, we will have the adjusted surrounding videos

        video_4x4("debug_psa1_adjusted", 
        f"debug/top_left_psa1_{user_name}.mp4", 
        f"debug/top_right_psa1_{user_name}.mp4",
        f"debug/bottom_left_psa1_{user_name}.mp4",
        f"debug/bottom_right_psa1_{user_name}.mp4", 
        "debug_psa1_group.mp4")

        #add subtitles to psa1
        psa1_video_subtitle = "~~ A A A ~~"
        fontfile = "SoleilRegular.otf"
        font_color="white"
        font_size=40
        bottom_margin=10

        command = [
            "ffmpeg",
            "-y",
            "-i", "debug_psa1_group.mp4",
            "-vf", f"drawtext=text='{psa1_video_subtitle}':fontfile={fontfile}:fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=h-th-{bottom_margin}",
            "-codec:a", "copy",
            "debug_psa1_subtitled_group.mp4"
        ]

        # run the command
        subprocess.run(command, check=True)

        #generate debug psa2
        top_left_video(f"debug_psa2/psa2_{user_name}.mp4", f"debug/top_left_psa2_{user_name}.mp4")
        top_right_video(f"debug_psa2/psa2_{user_name}.mp4", f"debug/top_right_psa2_{user_name}.mp4")
        bottom_left_video(f"debug_psa2/psa2_{user_name}.mp4", f"debug/bottom_left_psa2_{user_name}.mp4")
        bottom_right_video(f"debug_psa2/psa2_{user_name}.mp4", f"debug/bottom_right_psa2_{user_name}.mp4")

        #adjust all other surrounding videos to the video length of f"debug_psa1/psa1_{user_name}.mp4"
        #we need to do this step because not all users have same the length for their psa1 and psa2
        adjust_videos_to_center_video_length("debug_psa2", f"debug_psa2/psa2_{user_name}.mp4")
        #after this step, inside of debug_psa2_adjusted folder, we will have the adjusted surrounding videos

        video_4x4("debug_psa2_adjusted", 
        f"debug/top_left_psa2_{user_name}.mp4", 
        f"debug/top_right_psa2_{user_name}.mp4",
        f"debug/bottom_left_psa2_{user_name}.mp4",
        f"debug/bottom_right_psa2_{user_name}.mp4", 
        "debug_psa2_group.mp4")

        #add subtitles to psa2
        psa2_video_subtitle = "~~ I I I ~~"
        fontfile = "SoleilRegular.otf"
        font_color="white"
        font_size=40
        bottom_margin=10

        command = [
            "ffmpeg",
            "-y",
            "-i", "debug_psa2_group.mp4",
            "-vf", f"drawtext=text='{psa2_video_subtitle}':fontfile={fontfile}:fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=h-th-{bottom_margin}",
            "-codec:a", "copy",
            "debug_psa2_subtitled_group.mp4"
        ]

        # run the command
        subprocess.run(command, check=True)

        # this is the final step
        final_concatenation(user_name, debug_flag)

    else:

        #generate full_experience psa1
        top_left_video(f"full_experience_psa1/psa1_{user_name}.mp4", f"full_experience/top_left_psa1_{user_name}.mp4")
        top_right_video(f"full_experience_psa1/psa1_{user_name}.mp4", f"full_experience/top_right_psa1_{user_name}.mp4")
        bottom_left_video(f"full_experience_psa1/psa1_{user_name}.mp4", f"full_experience/bottom_left_psa1_{user_name}.mp4")
        bottom_right_video(f"full_experience_psa1/psa1_{user_name}.mp4", f"full_experience/bottom_right_psa1_{user_name}.mp4")
        
        #adjust all other surrounding videos to the video length of f"full_experience_psa1/psa1_{user_name}.mp4"
        #we need to do this step because not all users have same the length for their psa1 and psa2
        adjust_videos_to_center_video_length("full_experience_psa1", f"full_experience_psa1/psa1_{user_name}.mp4")
        #after this step, inside of full_experience_psa1_adjusted folder, we will have the adjusted surrounding videos

        video_4x4("full_experience_psa1_adjusted",
        f"full_experience/top_left_psa1_{user_name}.mp4", 
        f"full_experience/top_right_psa1_{user_name}.mp4",
        f"full_experience/bottom_left_psa1_{user_name}.mp4",
        f"full_experience/bottom_right_psa1_{user_name}.mp4", 
        "full_experience_psa1_group.mp4")

        #add subtitles to psa1
        psa1_video_subtitle = "~~ What if this was not just for fun? ~~"
        fontfile = "SoleilRegular.otf"
        font_color="white"
        font_size=40
        bottom_margin=10

        command = [
            "ffmpeg",
            "-y",
            "-i", "full_experience_psa1_group.mp4",
            "-vf", f"drawtext=text='{psa1_video_subtitle}':fontfile={fontfile}:fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=h-th-{bottom_margin}",
            "-codec:a", "copy",
            "full_experience_psa1_subtitled_group.mp4"
        ]

        # run the command
        subprocess.run(command, check=True)

        #generate full_experience psa2
        top_left_video(f"full_experience_psa2/psa2_{user_name}.mp4", f"full_experience/top_left_psa2_{user_name}.mp4")
        top_right_video(f"full_experience_psa2/psa2_{user_name}.mp4", f"full_experience/top_right_psa2_{user_name}.mp4")
        bottom_left_video(f"full_experience_psa2/psa2_{user_name}.mp4", f"full_experience/bottom_left_psa2_{user_name}.mp4")
        bottom_right_video(f"full_experience_psa2/psa2_{user_name}.mp4", f"full_experience/bottom_right_psa2_{user_name}.mp4")
        
        #adjust all other surrounding videos to the video length of f"full_experience_psa2/psa2_{user_name}.mp4"
        #we need to do this step because not all users have same the length for their psa1 and psa2
        adjust_videos_to_center_video_length("full_experience_psa2", f"full_experience_psa2/psa2_{user_name}.mp4")
        #after this step, inside of full_experience_psa2_adjusted folder, we will have the adjusted surrounding videos

        video_4x4("full_experience_psa2_adjusted", 
        f"full_experience/top_left_psa2_{user_name}.mp4", 
        f"full_experience/top_right_psa2_{user_name}.mp4",
        f"full_experience/bottom_left_psa2_{user_name}.mp4",
        f"full_experience/bottom_right_psa2_{user_name}.mp4", 
        "full_experience_psa2_group.mp4")

        #add subtitles to psa2
        psa2_video_subtitle = "~~ Your words, your data, your responsibility ~~"
        fontfile = "SoleilRegular.otf"
        font_color="white"
        font_size=40
        bottom_margin=10

        command = [
            "ffmpeg",
            "-y",
            "-i", "full_experience_psa2_group.mp4",
            "-vf", f"drawtext=text='{psa2_video_subtitle}':fontfile={fontfile}:fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=h-th-{bottom_margin}",
            "-codec:a", "copy",
            "full_experience_psa2_subtitled_group.mp4"
        ]

        # run the command
        subprocess.run(command, check=True)

        # this is the final step
        final_concatenation(user_name, debug_flag)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time taken is to run video_edit_full is: ", elapsed_time, " seconds!")