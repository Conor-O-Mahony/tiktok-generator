from moviepy.editor import *
import os
import sys

def merge_clips(movie_folder,background_folder,clip_length):
    clip_dir = os.path.join(movie_folder, "clips")
    background_dir = os.path.join(background_folder, "clips")
    temp = os.path.join(movie_folder,'final_temp_audio.mp3')
    i=1

    total_no_clips = 0
    for file in os.listdir(clip_dir):
        if os.path.isfile(os.path.join(clip_dir, file)):
            total_no_clips+=1

    merge_dir = os.path.join(movie_folder,"tiktok")
    if not os.path.exists(merge_dir):
        os.mkdir(merge_dir)
    
    while i<=total_no_clips:
        filename = f"clip{i}.mp4"
        movie_clip_dir = os.path.join(clip_dir, filename)
        background_clip_dir = os.path.join(background_dir, filename)

        movie_clip = VideoFileClip(movie_clip_dir)
        background_clip = VideoFileClip(background_clip_dir)
        bar = ImageClip("crop_bar.png").set_duration(clip_length)

        clips = [[bar],
                 [movie_clip],
                [background_clip],
                [bar]]

        final = clips_array(clips)
        final_path = os.path.join(merge_dir,f"final{i}.mp4")
        final.write_videofile(final_path,temp_audiofile=temp)
        i+=1

merge_clips(sys.argv[1],sys.argv[2],int(sys.argv[3]))
