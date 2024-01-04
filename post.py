
import os
import json
import time
from datetime import datetime
from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

def post_clips():
    with open('run.json', 'r') as f:
        data = json.load(f)

    movie_folder = data["movie_folder"]
    hashtags = data["hashtags"]
    clip_dir = os.path.join(movie_folder, "tiktok")
    total_no_clips = 0
    for file in os.listdir(clip_dir):
        if os.path.isfile(os.path.join(clip_dir, file)):
            total_no_clips+=1

    video = os.path.join(clip_dir,"final1.mp4")
    videos = [
        {
            'path': video,
            'description': hashtags
        }
    ]

    now = time.time()
    #now = int(datetime(2023,12,29,8,45).timestamp())
    schedule_time = now + 3600
    i=2
    while i<=total_no_clips:
        video = os.path.join(clip_dir, f"final{i}.mp4")
        u = datetime.fromtimestamp(schedule_time)
        videos.append({'path':video, 'description':hashtags, 'schedule':datetime(u.year,u.month,u.day,u.hour,u.minute)})
        schedule_time += 3600
        i+=1

    auth = AuthBackend(cookies='cookies.txt')
    upload_videos(videos=videos, auth=auth)

post_clips()

