import subprocess
import webvtt
import os 
import shutil
import audioPreprocessing
import videoPreprocessing
import textPreprocessing
from cv2 import cv2
def video_division(video,subtitle):
    if os.path.exists('static/video'): 
        shutil.rmtree('static/video')
        
    os.makedirs('static/video')
    count =0
    f= open("combine.txt","w+")
    for line in webvtt.read(subtitle):
        filename="static/video/video"+str(count)+".mp4"
        
        #cmd = ["ffmpeg","-i", video, "-ss", line.start,  "-to", line.end, "-c:v","copy","-c:a","copy", filename]
        cmd = ["ffmpeg", "-ss", line.start,  "-to", line.end,"-i", video, filename]
        subprocess.run(cmd, stderr=subprocess.STDOUT)
        count+=1
    f.close()
    return

def mutimodal_analysis(video,subtitle):
    #loop iterate through folder which contains video files
    #Detach audio from videos
    #perform text, video, audio analysis on data
    #combine videos
    #display video
    f= open("combine.txt","w+")
    line=[]
    for text in webvtt.read(subtitle):
        line.append(str(text))

    audioPreprocessing.detach_audios(video,subtitle)
    pred_audio=audioPreprocessing.audio("static/audio/")
    print(pred_audio)
    for i in range(len('static/video/')):
        fname='static/video/video'+str(i)+'.mp4'
        audname='static/audio/audio'+str(i)+'.mp3'
        f.write("file '"+fname+"'\n")
        videoPreprocessing.video_into_frames(fname)
        pred_video=videoPreprocessing.predict()
        max_value = max(pred_video.values())  # maximum value
        max_keys = [k for k, v in pred_video.items() if v == max_value]
        pred_text=textPreprocessing.pred_line(line[i])
        audio_res=pred_audio[audname]
        print(max_keys,pred_text,audio_res)
        filename="static/video/output"+str(i)+".mp4"
        cmd=["ffmpeg", "-i",fname, "-vf", "drawtext=text='My text starting ':x=640:y=360:fontsize=24:fontcolor=white" ,"-c:a" ,"copy", filename]
        f.write("file '"+filename+"'\n")
    f.close()   

    return


def videos_combine(video_path):
    cmd= ["ffmpeg" ,"-f", "concat" ,"-safe","0" ,"-i", "combine.txt","-c", "copy", "output.mp4"]
    #video_division("D:/FYP/7th Semester/Test Videos/selena-gomez-this-is-the-year-official.mp4","D:/FYP/7th Semester/Test Videos/thiss the year.vtt")
    subprocess.run(cmd, stderr=subprocess.STDOUT)
    for filename in os.listdir('static/video/'):
        if filename.startswith('video'):  # not to remove other files
            os.remove('static/video/' + filename)
    return