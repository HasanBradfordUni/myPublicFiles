import cv2
import numpy as np
from moviepy import VideoClip

def generate_stopwatch_video(start_time, end_time, file_path):
    start_seconds = start_time[0] * 3600 + start_time[1] * 60 + start_time[2]
    end_seconds = end_time[0] * 3600 + end_time[1] * 60 + end_time[2]
    duration = end_seconds - start_seconds

    def make_frame(t):
        total_seconds = int(t) + start_seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        frame = np.zeros((200, 400, 3), dtype=np.uint8)  # Black background
        cv2.putText(frame, time_str, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)
        return frame

    video = VideoClip(make_frame, duration=duration)
    video.write_videofile(file_path, fps=30, codec="libx264")

# Example usage:
starting_hours = input("Enter the hour of the starting time (Press Enter if 0): ")
if starting_hours == '':
    starting_hours = 0
else:
    starting_hours = int(starting_hours)
starting_minutes = int(input("Enter the minute of the starting time: "))
starting_seconds = int(input("Enter the second of the starting time: "))
ending_hours = input("Enter the hour of the ending time (Press Enter if 0): ")
if ending_hours == '':
    ending_hours = 0
else:
    ending_hours = int(ending_hours)
ending_minutes = int(input("Enter the minute of the ending time: "))
ending_seconds = int(input("Enter the second of the ending time: "))

start_time = (starting_hours, starting_minutes, starting_seconds)
end_time = (ending_hours, ending_minutes, ending_seconds)
file_path = input("Enter the filepath for where to save it: ")

generate_stopwatch_video(start_time, end_time, file_path)
