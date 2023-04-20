import os
import sys
from datetime import datetime

from better_ffmpeg_progress import FfmpegProcess


def run_script():
    command_list = ["ffmpeg"]

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
    command_list.extend(["-i", input_file])

    # Trim Video
    trim_video = "yes"
    trim_video = input("Trim Video? [yes]: ")
    if trim_video == "yes":
        start_time = input("Enter start time: ")
        if not start_time:
            print("You didn't enter start time!\nExiting..")
            sys.exit()

        command_list.extend(["-ss", start_time])

        end_time = input("Enter end time: ")
        if not end_time:
            print("You didn't enter end time!\nExiting..")
            sys.exit()

        duration = str(
            datetime.strptime(end_time, "%H:%M:%S")
            - datetime.strptime(start_time, "%H:%M:%S")
        )
        command_list.extend(["-t", duration])

    # Video compression
    compress_video = "yes"
    compress_video = input("Compress video? [yes]: ")
    if compress_video == "yes":
        # Set CRF
        crf_value = input("Enter CRF value between 0 to 51: ")
        if int(crf_value) not in range(52):
            print("You didn't enter correct preset value!Exiting..")
            sys.exit()
        command_list.extend(["-crf", crf_value])

        # Change codec
        change_vcodec = input("Change vcodec?: ")
        if change_vcodec == "yes":
            video_codec = input("Enter video codec value [none]: ")
            if not video_codec:
                print(
                    """You didn't enter codec value we will continue without
                     changing video codec."""
                )
            else:
                command_list.extend(["-vcodec", video_codec])

            audio_codec = input("Enter audio codec value [none]: ")
            if not audio_codec:
                print(
                    """You didn't enter codec value we will continue without
                     changing audio codec."""
                )
            else:
                command_list.extend(["-acodec", audio_codec])

        # Set preset
        possible_preset_values = [
            "ultrafast",
            "superfast",
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower",
            "veryslow",
        ]
        print(
            "Possible preset values are:\n",
            " ".join(possible_preset_values),
        )
        preset = input("Enter preset value: ")
        if preset not in possible_preset_values:
            print("You didn't enter correct preset value!\nExiting..")
            sys.exit()

        command_list.extend(
            ["-preset", preset, f"{filename}-{crf_value}CRF{extension}"]
        )
        FfmpegProcess(command_list).run()

    # Smooth video
    smooth_video = "yes"
    smooth_video = input("Make video smooth? [yes]: ")
    if smooth_video == "yes":
        smooth_command_list = ["ffmpeg"]
        if compress_video == "yes":
            smooth_command_list.extend(
                ["-i", f"{filename}-{crf_value}CRF{extension}"],
            )
        else:
            smooth_command_list.extend(["-i", input_file])
            if trim_video == "yes":
                smooth_command_list.extend(["-ss", start_time, "-t", duration])
        # crf_value = input("Enter CRF value between 0 to 51: ")
        # if int(crf_value) not in range(52):
        #     print("You didn't enter correct preset value!\nExiting..")
        #     sys.exit()
        # smooth_command_list.extend(["-crf", crf_value])
        fps_value = input("Enter FPS value between 10 to 90: ")
        if int(fps_value) not in range(10, 91):
            print("You didn't enter correct FPS value!\nExiting..")
            sys.exit()
        video_filters = (
            "minterpolate=fps="
            + fps_value
            + ":mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
        )
        smooth_command_list.extend(
            [
                "-vf",
                video_filters,
                "-c:a",
                "copy",
                "-c:s",
                "copy" f"{filename}-{crf_value}CRF-{fps_value}FPS{extension}",
            ]
        )
        FfmpegProcess(smooth_command_list).run()


if __name__ == "__main__":
    run_script()
