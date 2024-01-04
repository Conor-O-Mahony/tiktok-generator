import tkinter
import customtkinter
import json
import os
import sys
import subprocess
from pathlib import Path
import threading 
import signal

class Redirect():
    
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see('end')


def chop_vid():
    if 'video_select' in globals():
        chop_status.configure(text='Running')
        try:
            global p
            start = int(start_var.get())
            end = int(end_var.get())
            clip_length = int(vid_length.get())

            with open('run.json', 'r') as f:
                data = json.load(f)

            data['movie_start'] = start
            data['movie_end'] = end
            data['clip_length'] = clip_length

            movie_name = data['movie_name']
            movie_folder = data['movie_folder']

            with open('run.json', 'w') as f:
                json.dump(data,f)

            p = subprocess.Popen(["python","split_vid.py", movie_name, movie_folder, str(start), str(end), str(clip_length)], stdout=subprocess.PIPE, bufsize=1, text=True)
            while p.poll() is None:
                msg = p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)

            chop_status.configure(text='Complete!')
            return

        except:
            chop_status.configure(text='Error: Invalid Parameters')
            return

    else:
        chop_status.configure(text='Error: No Video Selected')
        return


def chop_bg():
    if 'bg_select' in globals():
        bg_status.configure(text='Running')
        try:
            global p2
            start = 0
            end = int(end_var.get()) - int(start_var.get())
            clip_length = int(vid_length.get())

            with open('run.json', 'r') as f:
                data = json.load(f)

            data['movie_start'] = start
            data['movie_end'] = end
            data['clip_length'] = clip_length

            bg_name = data['background_name']
            bg_folder = data['background_folder']

            with open('run.json', 'w') as f:
                json.dump(data,f)

            p2 = subprocess.Popen(["python","split_bg.py", bg_name, bg_folder, str(start), str(end), str(clip_length)], stdout=subprocess.PIPE, bufsize=1, text=True)
            while p2.poll() is None:
                msg = p2.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)

            bg_status.configure(text='Complete!')
            return

        except:
            bg_status.configure(text='Error: Invalid Parameters')
            return

    else:
        bg_status.configure(text='Error: No Video Selected')
        return

def gen_tiktok():
    gen_status.configure(text='Running')
    try:
        global p3
        with open('run.json', 'r') as f:
            data = json.load(f)

        movie_folder = data['movie_folder']
        background_folder = data['background_folder']
        clip_length = data['clip_length']

        p3 = subprocess.Popen(["python","merge_splits.py", movie_folder, background_folder, str(clip_length)], stdout=subprocess.PIPE, bufsize=1, text=True)
        while p3.poll() is None:
            msg = p3.stdout.readline().strip() # read a line from the process output
            if msg:
                print(msg)

        gen_status.configure(text='Complete!')
        return

    except:
        gen_status.configure(text='Error: Clips Not Generated')
        return

def upload_tiktoks():
    upload_status.configure(text='Running')

    path = Path('cookies.txt')

    if not path.is_file():
        upload_status.configure(text='cookies.txt Not Located')
        return

    try:
        global p4
        descripton = str(desc_var.get())
        if descripton == '':
            upload_status.configure(text='Set A Description')
            return
        
        with open('run.json', 'r') as f:
            data = json.load(f)

        data['hashtags'] = descripton

        with open('run.json', 'w') as f:
            json.dump(data,f)


        p4 = subprocess.Popen(["python","post.py"], stdout=subprocess.PIPE, bufsize=1, text=True)
        while p4.poll() is None:
            msg = p4.stdout.readline().strip() # read a line from the process output
            if msg:
                print(msg)

        upload_status.configure(text='Complete!')
        return
    except:
        upload_status.configure(text='TikToks Weren\'t Located')
        return

def run():
    def function(target_fn):
        thread = threading.Thread(target=target_fn)
        thread.start()
        thread.join()
    targets = [chop_vid,chop_bg,gen_tiktok,upload_tiktoks]
    for target in targets:
        function(target)

def die():
    try:
        os.kill(p.pid, signal.SIGTERM)
    except:
        pass
    try:
        os.kill(p2.pid, signal.SIGTERM)
    except:
        pass
    try:
        os.kill(p3.pid, signal.SIGTERM)
    except:
        pass
    try:
        os.kill(p4.pid, signal.SIGTERM)
    except:
        pass

def close():
    os.kill(os.getpid(), signal.SIGTERM)

#Uses light/dark mode of system
customtkinter.set_appearance_mode("System")

customtkinter.set_default_color_theme("blue")

#App frame
app = customtkinter.CTk()
app.geometry("700x720")
app.title("TikTok Generator")

#UI Elements
title = customtkinter.CTkLabel(app, text="Autogenerate and Schedule TikToks from Video Source.")
title.pack()
customtkinter.CTkLabel(app, text="(If the program breaks, close it to restart.)").pack()

def open_video():
    global video_select

    video_select = tkinter.filedialog.askopenfilename(title="Select The Main Video")

    path = Path(video_select).parts

    with open('run.json', 'r') as f:
        data = json.load(f)

    data['movie_folder'] = path[-2]
    data['movie_name'] = path[-1]

    with open('run.json', 'w') as f:
        json.dump(data,f)

    video_dir.configure(text=os.path.join(path[-2],path[-1]))

video_frame = customtkinter.CTkFrame(app)
main_select_button = customtkinter.CTkButton(video_frame, text="Select The Main Video", command=open_video)
main_select_button.grid(row=0,column=0,padx=10)
video_dir = customtkinter.CTkLabel(video_frame, text='')
video_dir.grid(row=1,column=0,padx=10)

def open_background():
    global bg_select

    bg_select = tkinter.filedialog.askopenfilename(title="Select The Background Video")

    path = Path(bg_select).parts

    with open('run.json', 'r') as f:
        data = json.load(f)

    data['background_folder'] = path[-2]
    data['background_name'] = path[-1]

    with open('run.json', 'w') as f:
        json.dump(data,f)
    
    bg_dir.configure(text=os.path.join(path[-2],path[-1]))

background_select_button = customtkinter.CTkButton(video_frame, text="Select The Background Video", command=open_background)
background_select_button.grid(row=0,column=1,padx=10)
bg_dir = customtkinter.CTkLabel(video_frame, text='')
bg_dir.grid(row=1,column=1,padx=10)
video_frame.pack(pady=20)

seconds_frame = customtkinter.CTkFrame(app)

vid_start_button = customtkinter.CTkLabel(seconds_frame, text='Video Starts At (Seconds)')
vid_start_button.grid(row=0,column=0,padx=10)
start_var = tkinter.StringVar()
start = customtkinter.CTkEntry(seconds_frame, width=100,height=40,textvariable=start_var)
start.grid(row=1,column=0,padx=10)

vid_ends_button = customtkinter.CTkLabel(seconds_frame, text='Video Ends At (Seconds)')
vid_ends_button.grid(row=0,column=1,padx=10)
end_var = tkinter.StringVar()
end = customtkinter.CTkEntry(seconds_frame, width=100,height=40,textvariable=end_var)
end.grid(row=1,column=1,padx=10)

vid_length_button = customtkinter.CTkLabel(seconds_frame, text='Set A Clip Length (Seconds)')
vid_length_button.grid(row=0,column=2,padx=10)
vid_length = tkinter.StringVar()
length = customtkinter.CTkEntry(seconds_frame, width=100,height=40,textvariable=vid_length)
length.grid(row=1,column=2,padx=10)

seconds_frame.pack()

customtkinter.CTkLabel(app, text='Enter A Description (Title + Hashtags)').pack()
desc_var = tkinter.StringVar()
desc = customtkinter.CTkEntry(app, width=500,height=40,textvariable=desc_var)
desc.pack()

button_frame = customtkinter.CTkFrame(app)
chop_video = customtkinter.CTkButton(button_frame, text="Chop Main Video",command=threading.Thread(target=chop_vid).start)
chop_video.grid(row=0,column=0,padx=10)
chop_status = customtkinter.CTkLabel(button_frame, text="")
chop_status.grid(row=1,column=0,padx=10)
chop_background = customtkinter.CTkButton(button_frame, text="Chop Background Video",command=threading.Thread(target=chop_bg).start)
chop_background.grid(row=0,column=1,padx=10)
bg_status = customtkinter.CTkLabel(button_frame, text="")
bg_status.grid(row=1,column=1,padx=10)
gener_tiktok = customtkinter.CTkButton(button_frame, text="Generate TikToks",command=threading.Thread(target=gen_tiktok).start)
gener_tiktok.grid(row=0,column=2,padx=10)
gen_status = customtkinter.CTkLabel(button_frame, text="")
gen_status.grid(row=1,column=2,padx=10)
upload_tiktok = customtkinter.CTkButton(button_frame, text="Upload TikToks",command=threading.Thread(target=upload_tiktoks).start)
upload_tiktok.grid(row=0,column=3,padx=10)
upload_status = customtkinter.CTkLabel(button_frame, text="")
upload_status.grid(row=1,column=3,padx=10)
button_frame.pack(pady=20)

run_all = customtkinter.CTkButton(app, text="Run All",command=threading.Thread(target=run).start)
run_all.pack()
run_status = customtkinter.CTkLabel(app, text="")
run_status.pack()

terminal = customtkinter.CTkTextbox(app, width=400)
terminal.pack()

old_stdout = sys.stdout    
# assing Redirect with widget Text 
sys.stdout = Redirect(terminal)

#app.grid_columnconfigure(4, minsize=100)

kill_switch = customtkinter.CTkButton(app, text="Kill All Tasks", fg_color='Red',command=die)
kill_switch.pack(pady=20)

#Run The App
app.protocol("WM_DELETE_WINDOW", close)
app.mainloop()