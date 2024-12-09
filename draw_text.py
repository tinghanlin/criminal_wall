import subprocess

def draw_labels_on_video(input_video_filename, output_video_filename):

    text = "~~     Mary had a little lamb, little lamb, little lamb.     ~~\n~~ Mary had a little lamb, it's fleece as white as snow. ~~"
    fontfile = "SoleilRegular.otf"
    font_color="white"
    font_size=40
    bottom_margin=10
    
    #draw text to video
    command = [
        "ffmpeg",
        "-y",
        "-i", input_video_filename,
        "-vf", f"drawtext=text='{text}':fontfile={fontfile}:fontcolor={font_color}:fontsize={font_size}:x=(w-text_w)/2:y=h-th-{bottom_margin}",
        "-codec:a", "copy",
        output_video_filename
    ]

    # run the command
    subprocess.run(command, check=True)

draw_labels_on_video("full_singing/singing_timmy.mp4", "full_singing/singing_timmy_with_labels.mp4")