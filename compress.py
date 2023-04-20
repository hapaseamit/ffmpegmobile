import os
import sys

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

    # Set CRF
    crf_value = input("Enter CRF value between 0 to 51: ")
    if int(crf_value) not in range(52):
        print("You didn't enter correct preset value!Exiting..")
        sys.exit()
    command_list.extend(["-crf", crf_value])

    # Change codec
    change_vcodec = "no"
    change_vcodec = input("Change video codec? [no]: ")
    if change_vcodec == "yes":
        video_codec = input("Enter video codec value [none]: ")
        if not video_codec:
            print(
                """You didn't enter codec value we will continue without
                changing video codec."""
            )
        else:
            command_list.extend(["-vcodec", video_codec])

    change_acodec = "no"
    change_acodec = input("Change audio codec? [no]: ")
    if change_acodec == "yes":
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
        [
            "-preset",
            preset,
            f"{filename}-{crf_value}-CRF-{extension}",
        ]
    )
    FfmpegProcess(command_list).run()


if __name__ == "__main__":
    run_script()
