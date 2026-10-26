import os
import subprocess

def burn_subtitles(video_path, srt_relative_path, output_path, ffmpeg_path):
    video_full = os.path.abspath(video_path)
    output_full = os.path.abspath(output_path)
    
    # FFmpeg command to filter and burn subtitles
    command = [
        ffmpeg_path,
        "-i", video_full,
        "-vf", f"subtitles={srt_relative_path}",
        output_full
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video with burned-in captions generated at: {output_path}")
    except Exception as e:
        print(f"Error burning captions: {e}")

if __name__ == "__main__":
    # Update FFmpeg executable path according to your machine installation
    ffmpeg_exe_path = r"C:\ffmpeg\bin\ffmpeg.exe"
    video_file = "videos/sample_video.mp4"
    srt_file = "captions/output.srt"
    output_file = "videos/output_video.mp4"

    burn_subtitles(video_file, srt_file, output_file, ffmpeg_exe_path)