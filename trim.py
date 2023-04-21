import os
import sys
from datetime import datetime

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

    start_time = input("Enter start time: ")
    if not start_time:
        print("You didn't enter start time!\nExiting..")
        sys.exit()

    end_time = input("Enter end time: ")
    if not end_time:
        print("You didn't enter end time!\nExiting..")
        sys.exit()

    duration = str(
        datetime.strptime(end_time, "%H:%M:%S")
        - datetime.strptime(start_time, "%H:%M:%S")
    )

    command_list = [
        "ffmpeg",
        "-i",
        input_file,
        "-ss",
        start_time,
        "-t",
        duration,
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-c:s",
        "copy",
        f"{filename}-trimmed{extension}",
    ]
    FfmpegProcess(command_list).run()


if __name__ == "__main__":
    run_script()
