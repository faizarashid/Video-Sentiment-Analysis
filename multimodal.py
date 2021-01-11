import subprocess
import webvtt
import os 
import shutil
import audioPreprocessing
import videoPreprocessing
import textPreprocessing
from cv2 import cv2
from collections import Counter

time_stamps={}
def video_division(video,subtitle):
    if os.path.exists('static/video'): 
        shutil.rmtree('static/video')
        
    os.makedirs('static/video')
    count =0
    for line in webvtt.read(subtitle):
        filename="static/video/video"+str(count)+".mp4"
        
        #cmd = ["ffmpeg","-i", video, "-ss", line.start,  "-to", line.end, "-c:v","copy","-c:a","copy", filename]
        cmd = ["ffmpeg", "-ss", line.start,  "-to", line.end,"-i", video, filename]
        subprocess.run(cmd, stderr=subprocess.STDOUT)
        count+=1

    return

def mutimodal_analysis(video,subtitle):
    #loop iterate through folder which contains video files
    #Detach audio from videos
    #perform text, video, audio analysis on data
    #combine videos
    #display video
   
    line=[]
    count=1
    for text in webvtt.read(subtitle):
        line.append(str(text))
        stamps=text.start+" "+text.end
        time_stamps[stamps]=count
        count+=1

    audioPreprocessing.detach_audios(video,subtitle)
    pred_audio=audioPreprocessing.audio("static/audio/")
    print(pred_audio)
    f= open("combine.txt","w+")
    count=1
    val_list = list(time_stamps.values())
    key_list = list(time_stamps.keys())
    l=os.listdir('static/video/')
    for i in range(len(l)):
        fname='static/video/video'+str(i)+'.mp4'
        audname='static/audio/audio'+str(i)+'.mp3'
        videoPreprocessing.video_into_frames(fname)
        pred_video=videoPreprocessing.predict()
        max_value = max(pred_video.values())  # maximum value
        max_keys = [k for k, v in pred_video.items() if v == max_value]
        pred_text=textPreprocessing.pred_line(line[i])
        audio_res=pred_audio[audname]
        print(max_keys[0],pred_text,audio_res)
        filename="static/video/output"+str(i)+".mp4"
        emotion=checking(max_keys[0],pred_text,audio_res)
        if emotion=="Positive":
            cmd=["ffmpeg", "-i",fname, "-vf", "drawtext=text='Multi Modal Positive ':x=100:y=160:fontsize=30:fontcolor=green :box=1: boxcolor=black@0.5:boxborderw=5" ,"-c:a" ,"copy", filename]
        elif emotion=="Negative":
            cmd=["ffmpeg", "-i",fname, "-vf", "drawtext=text='Multi Modal Negative ':x=100:y=160:fontsize=30:fontcolor=red:box=1: boxcolor=black@0.5:boxborderw=5" ,"-c:a" ,"copy", filename]
        else:
            cmd=["ffmpeg", "-i",fname, "-vf", "drawtext=text=' Neutral ':x=100:y=160:fontsize=30:fontcolor=blue:box=1: boxcolor=black@0.5:boxborderw=5" ,"-c:a" ,"copy", filename]
        subprocess.run(cmd, stderr=subprocess.STDOUT)
        f.write("file '"+filename+"'\n")
        k=val_list.index(count)
        time_stamps[key_list[k]]=emotion
        count+=1
    f.close()   
    videos_combine('static/video/video')
    return time_stamps


def videos_combine(video_path):
    cmd= ["ffmpeg" ,"-f", "concat","-safe","0" ,"-i", "combine.txt","-c", "copy", "static/output.mp4"]
    #video_division("D:/FYP/7th Semester/Test Videos/selena-gomez-this-is-the-year-official.mp4","D:/FYP/7th Semester/Test Videos/thiss the year.vtt")
    subprocess.run(cmd, stderr=subprocess.STDOUT)
    for filename in os.listdir('static/video/'):
        if filename.startswith('video'):  # not to remove other files
            os.remove('static/video/' + filename)
    return

def checking(val1,val2,val3):
    l=[val1,val2,val3]
    if l.count(val1)>1:
        return val1
    elif l.count(val2)>1:
        return val2
    else: 
        return "Neutral"

