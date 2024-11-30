#Reference: https://www.geeksforgeeks.org/retrieving-the-output-of-subprocesscall-in-python/
#Reference: https://www.w3schools.com/python/python_regex.asp#findall
#Reference: https://stackoverflow.com/questions/18444194/cutting-multimedia-files-based-on-start-and-end-time-using-ffmpeg
#Reference: https://www.youtube.com/watch?v=ak52RXKfDw8
#Reference: https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg

import subprocess
import re

#Example running this function: slience_remove("combined_1.mp4", "-25dB", "0.2", 2.0)
def slience_remove(video_filename, silence_threshold, silence_duration, video_length):

    command = [
        "ffmpeg",
        "-hide_banner",
        "-i", video_filename,
        "-af", f"silencedetect=n={silence_threshold}:d={silence_duration}",
        "-f", "null", "-"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    # print("Return code:", result.returncode)
    # print("Output:", result.stdout)
    # print("Error:", result.stderr)
    ffmpeg_output = result.stderr

    silence_start_time_array_str = re.findall(r"silence_start: ([.\d]+)", ffmpeg_output)
    silence_end_time_array_str = re.findall(r"silence_end: ([.\d]+)", ffmpeg_output)
    print("silence_start_time_array_str:", silence_start_time_array_str)
    print("silence_end_time_array_str:", silence_end_time_array_str)

    #convert all time array from str to float
    silence_start_time_array_float = []
    silence_end_time_array_float = []

    for t in silence_start_time_array_str:
        silence_start_time_array_float.append(float(t))

    for t in silence_end_time_array_str:
        silence_end_time_array_float.append(float(t))
    
    number_of_silence_segments = len(silence_start_time_array_float) #silence_start_time_array_float and silence_end_time_array_float have the same length

    voice_start_time_array_float = [] #stores start time for voice
    voice_end_time_array_float = [] #stores end time for voice

    if number_of_silence_segments == 0:
        print("Case 0 (no silence), we output the original video")
        voice_start_time_array_float.append(0.0)
        voice_end_time_array_float.append(video_length)
    else:

        if silence_start_time_array_float[0] == 0.0 and silence_end_time_array_float[number_of_silence_segments-1] >= video_length:
            print("Case 1 (there is silence at the beginning and at the end of the video): we can just keep the voice intervals")
            for i in range(number_of_silence_segments-1):
                voice_start_time_array_float.append(silence_end_time_array_float[i])
                voice_end_time_array_float.append(silence_start_time_array_float[i+1])
            
        elif silence_start_time_array_float[0] == 0.0:
            print("Case 2 (one silent segment is at the beginning of the video): we can keep the voice intervals and add the ending voice")
            for i in range(number_of_silence_segments-1):
                voice_start_time_array_float.append(silence_end_time_array_float[i])
                voice_end_time_array_float.append(silence_start_time_array_float[i+1])
            
            voice_start_time_array_float.append(silence_end_time_array_float[number_of_silence_segments-1])
            voice_end_time_array_float.append(video_length)

        elif silence_end_time_array_float[number_of_silence_segments-1] >= video_length:
            print("Case 3 (one silent segment is at the end of the video): we can keep the voice intervals and add the beginning voice")
            voice_start_time_array_float.append(0.0)
            voice_end_time_array_float.append(silence_start_time_array_float[0])

            for i in range(number_of_silence_segments-1):
                voice_start_time_array_float.append(silence_end_time_array_float[i])
                voice_end_time_array_float.append(silence_start_time_array_float[i+1])
            
        else:
            print("Case 4 (typical case - silent segment is in the middle of the video): we can keep the voice intervals and add the beginning and ending voice")

            voice_start_time_array_float.append(0.0)
            voice_end_time_array_float.append(silence_start_time_array_float[0])

            for i in range(number_of_silence_segments-1):
                voice_start_time_array_float.append(silence_end_time_array_float[i])
                voice_end_time_array_float.append(silence_start_time_array_float[i+1])
            
            voice_start_time_array_float.append(silence_end_time_array_float[number_of_silence_segments-1])
            voice_end_time_array_float.append(video_length)

    print("voice_start_time_array_float: ", voice_start_time_array_float)
    print("voice_end_time_array_float: ", voice_end_time_array_float)

    ###TEST CASES###
    # #test case for Case 1
    # silence_start_time_array_float = [0.0, 0.7, 1.8]
    # silence_end_time_array_float = [0.3, 0.9, 2.0]
    # # expected output is: voice_start_time_array_float: [0.3, 0.9], voice_end_time_array_float: [0.7, 1.8]

    # #test case for Case 2
    # silence_start_time_array_float = [0.0, 0.4, 0.7, 1.1]
    # silence_end_time_array_float = [0.2, 0.5, 0.8, 1.2]
    # # expected output is: voice_start_time_array_float: [0.2, 0.5, 0.8, 1.2], voice_end_time_array_float: [0.4, 0.7, 1.1, 2.0]

    # #test case for Case 3
    # silence_start_time_array_float = [0.7]
    # silence_end_time_array_float = [2.0]
    # # expected output is: voice_start_time_array_float: [0.0], voice_end_time_array_float: [0.7]

    #test case for Case 4
    # silence_start_time_array_float = [0.2, 0.4, 0.6, 0.8]
    # silence_end_time_array_float = [0.3, 0.5, 0.7, 0.9]
    # expected output is: voice_start_time_array_float: [0.0, 0.3, 0.5, 0.7, 0.9], voice_end_time_array_float: [0.2, 0.4, 0.6, 0.8, 2.0]
    ###TEST CASES###

    #now we cut out the voice part from the video
    number_of_voice_segments = len(voice_start_time_array_float)

    voice_file_names = [] #this is used when there exists multiple voice segments

    for i in range(number_of_voice_segments):
        temp_file_name = f"{video_filename[:-4]}_no_silence_{str(i)}.mp4" # -4 is there to remove .mp4 (4 characters)
        command2 = [
            "ffmpeg",
            "-y",
            "-i", video_filename,
            "-ss", str(voice_start_time_array_float[i]),
            "-to", str(voice_end_time_array_float[i]),
            "-c:v", "libx264",
            "-c:a", "aac",
            temp_file_name
        ]

        voice_file_names.append(temp_file_name)

        subprocess.run(command2, check=True)

    #if there are multiple voice segments, we concatenate them together
    #if there is only one, we just concatenate the same file (ie basically just rename the file)

    FILENAME = "voice_file_names.txt"
    CONCAT_FILENAME = f"{video_filename[:-4]}_no_silence_concat.mp4" # -4 is there to remove .mp4 (4 characters)
    print(CONCAT_FILENAME)
    with open(FILENAME, "w") as f:
        for file_name in voice_file_names:
            f.write(f"file '{file_name}'\n")

    command3 = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-i", FILENAME,
        "-c", "copy",
        CONCAT_FILENAME
    ]

    subprocess.run(command3, check=True)
