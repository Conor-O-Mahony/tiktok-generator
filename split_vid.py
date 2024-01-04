import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import sys

def movie_split(file_name,folder_name,start_time,end_time,clip_length):
    temp = os.path.join(folder_name,'temp_audio.mp3')

    output_path = os.path.join(folder_name, "clips")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    movie_dir = os.path.join(folder_name,file_name)
    movie = VideoFileClip(movie_dir)

    current_time = start_time
    clip_number = 1
    
    while current_time+clip_length < end_time:
        output = os.path.join(output_path, f"clip{clip_number}.mp4")
        clip = movie.subclip(current_time, current_time+clip_length)
        cropped_clip = clip.crop(x1=100,x2=1180)
        scaled_clip = cropped_clip.fx(vfx.resize,(1080,536),width= 1080)
        scaled_clip.write_videofile(output,temp_audiofile=temp)

        clip_number+=1
        current_time+=clip_length

    output = os.path.join(output_path, f"clip{clip_number}.mp4")
    clip = movie.subclip(current_time, end_time)
    cropped_clip = clip.crop(x1=100,x2=1180)
    scaled_clip = cropped_clip.fx(vfx.resize,(1080,536),width= 1080)
    scaled_clip.write_videofile(output,temp_audiofile=temp)
    print("Video split into",clip_number+1,"parts.")

movie_split(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))