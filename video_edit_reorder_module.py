import subprocess
import os

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
33 19 21 13 20 37 17 40
What if this was not just for fun?
26 49 26 51 26 53
Your words, your data, your responsibility
"""

sequence = "25 16 4 41 44 41 44 41 44 25 16 4 41 44 11 27 14 46 14 32 33 19 21 13 20 37 17 40 26 49 26 51 26 53"

sequence_numbers = [int(num) for num in sequence.split()]

words = [dictionary[num] for num in sequence_numbers]

with open('video_list_to_concatenate.txt', 'w') as f:
    for num in sequence_numbers:
        filename = f"new_recordings/new_combined_{num}_no_silence_concat.mp4" #TODO: could potentially change

        #raise errors if a file does not exist
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} ({dictionary[num]}) not found")

        f.write(f"file '{filename}'\n")

#concatenate the vidoes together into one video
command = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'video_list_to_concatenate.txt',
    '-c', 'copy',
    'singing.mp4'
]

# run the command
subprocess.run(command, check=True)
