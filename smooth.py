import os
import sys

from better_ffmpeg_progress import FfmpegProcess


def run_script():
    # Setup input file
    input_file = input("Enter input file path: ")
    if not input_file:
        print("You did not input file path!\nExiting...")
        sys.exit()

    # Validate input file path
    if not os.path.exists(input_file):
        print("Input file doesn't exist!\nExiting...")
        sys.exit()

    filename, extension = os.path.splitext(input_file)
    if not extension == ".mp4":
        ans = "yes"
        ans = input("Change extension to .mp4? [yes]: ")
        if ans == "yes":
            extension = ".mp4"

    fps_value = input("Enter FPS value between 10 to 90: ")
    if int(fps_value) not in range(10, 91):
        print("You didn't enter correct FPS value!\nExiting..")
        sys.exit()

    video_filters = (
        "minterpolate=fps="
        + fps_value
        + ":mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
    )

    smooth_command_list = [
        "ffmpeg",
        "-i",
        input_file,
        "-vf",
        video_filters,
        "-c:a",
        "copy",
        "-c:s",
        "copy",
        f"{filename}-{fps_value}FPS{extension}",
    ]

    FfmpegProcess(smooth_command_list).run()


if __name__ == "__main__":
    run_script()
