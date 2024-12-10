import subprocess
import os
import time

def generate_video_list_to_concatenate(user_name, sequence, dictionary):
    sequence_numbers = [int(num) for num in sequence.split()]

    words = [dictionary[num] for num in sequence_numbers]

    with open('video_list_to_concatenate.txt', 'w') as f:
        for num in sequence_numbers:
            filename = f"{user_name}/new_combined_{num}_no_silence_concat.mp4"

            #raise errors if a file does not exist
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} ({dictionary[num]}) not found")

            f.write(f"file '{filename}'\n")

#type_of_message: sing, psa1, psa2
#output_filename: re-ordered video without subtitles
#subtitled_output_filename: re-ordered video with subtitles
def video_edit(user_name, type_of_message, output_filename, subtitled_output_filename, debug_flag):
    
    #start a time to see how long it takes to run video_edit
    start_time = time.time()

    if debug_flag == True:
        
        debug_dictionary = {
            1: "Bath", #practice
            2: "Car", #practice
            3: "Think", #practice
            4: "A",
            5: "E",
            6: "I",
        }

        """
        6 5 4
        I E A
        """
        sequence = "6 5 4"
        video_subtitle = "~~ I E A ~~"

        if type_of_message == "psa1":
            """
            4 4 4
            A A A
            """
            sequence = "4 4 4"
            video_subtitle = "~~ A A A ~~"
        elif type_of_message == "psa2":
            """
            6 6 6
            I I I
            """
            sequence = "6 6 6"
            video_subtitle = "~~ I I I ~~"

        generate_video_list_to_concatenate(user_name, sequence, debug_dictionary)

    else:

        dictionary = {
            1: "Bath", #practice
            2: "Car", #practice
            3: "Think", #practice
            4: "A",
            5: "E",
            6: "I",
            7: "O",
            8: "U",
            9: "His",
            10: "Hers",
            11: "Its",
            12: "Is",
            13: "Was",
            14: "As",
            15: "Have",
            16: "Had",
            17: "For",
            18: "And",
            19: "If",
            20: "Not",
            21: "This",
            22: "That",
            23: "Join",
            24: "Unite",
            25: "Marry",
            26: "Your",
            27: "Fleece",
            28: "Feather",
            29: "Wind",
            30: "Rain",
            31: "Sun",
            32: "Snow",
            33: "What",
            34: "Why",
            35: "When",
            36: "Where",
            37: "Just",
            38: "Justice",
            39: "Silly",
            40: "Fun",
            41: "Little",
            42: "Tiny",
            43: "Beef",
            44: "Lamb",
            45: "Chicken",
            46: "White",
            47: "Black",
            48: "Letter",
            49: "Words",
            50: "File",
            51: "Data",
            52: "Accountability",
            53: "Responsibility"
        }

        """
        25 16 4 41 44 41 44 41 44
        Mary had a little lamb, little lamb, little lamb
        25 16 4 41 44 11 27 14 46 14 32
        Mary had a little lamb, it's fleece as white as snow
        """
        
        sequence = "25 16 4 41 44 41 44 41 44 25 16 4 41 44 11 27 14 46 14 32"
        video_subtitle = "~~     Mary had a little lamb, little lamb, little lamb.     ~~\n~~ Mary had a little lamb, it's fleece as white as snow. ~~"
        
        if type_of_message == "psa1":
            """
            33 19 21 13 20 37 17 40
            What if this was not just for fun?
            """
            sequence = "33 19 21 13 20 37 17 40"
            video_subtitle = "~~ What if this was not just for fun? ~~"
        elif type_of_message == "psa2":
            """
            26 49 26 51 26 53
            Your words, your data, your responsibility
            """
            sequence = "26 49 26 51 26 53"
            video_subtitle = "~~ Your words, your data, your responsibility ~~"
        
        generate_video_list_to_concatenate(user_name, sequence, dictionary)

    #concatenate the vidoes together into one video
    command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "video_list_to_concatenate.txt",
        "-c", "copy",
        output_filename
    ]

    # run the command
    subprocess.run(command, check=True)

    #by the time you get here, ffmpeg is done, so we can directly draw subtitles to video

    fontfile = "SoleilRegular.otf"
    font_color="white"
    font_size=40
    bottom_margin=10

    command = [
        "ffmpeg",
        "-y",
        "-i", output_filename,
        "-vf", f"drawtext=text='{video_subtitle}':fontfile={fontfile}:fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=h-th-{bottom_margin}",
        "-codec:a", "copy",
        subtitled_output_filename
    ]

    # run the command
    subprocess.run(command, check=True)

    end_time2 = time.time()
    elapsed_time = end_time2 - start_time
    print(f"Time taken for concatenating the {type_of_message} videos and including the subtitles: {elapsed_time} seconds!") 
    #Empirically, on MacOS M3, "sing" took 1.72, "psa1" took 0.81, "psa2" took 0.55.

#generate sing, psa1, and psa2 for a user
def triple_video_edit(user_name, debug_flag):
    #start a time to see how long it takes to run triple_video_edit
    start_time = time.time()
    if debug_flag == True:
        video_edit(user_name, "sing", f'debug/sing_{user_name}.mp4', f'debug/sing_subtitled_{user_name}.mp4', debug_flag)
        video_edit(user_name, "psa1", f'debug/psa1_{user_name}.mp4', f'debug/psa1_subtitled_{user_name}.mp4', debug_flag)
        video_edit(user_name, "psa2", f'debug/psa2_{user_name}.mp4', f'debug/psa2_subtitled_{user_name}.mp4', debug_flag)
    else:
        video_edit(user_name, "sing", f'full_experience/sing_{user_name}.mp4', f'full_experience/sing_subtitled_{user_name}.mp4', debug_flag)
        video_edit(user_name, "psa1", f'full_experience/psa1_{user_name}.mp4', f'full_experience/psa1_subtitled_{user_name}.mp4', debug_flag)
        video_edit(user_name, "psa2", f'full_experience/psa2_{user_name}.mp4', f'full_experience/psa2_subtitled_{user_name}.mp4', debug_flag)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to run triple_video_edit is: {end_time} seconds!") 