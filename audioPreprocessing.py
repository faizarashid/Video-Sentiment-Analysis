import os
import matplotlib.pyplot as plt
from cv2 import cv2 
import moviepy.editor
#for loading and visualizing audio files
import librosa
import librosa.display
import tensorflow as tf
import multimodal
import shutil
from keras.preprocessing import image
import numpy as np
Category = ["Angry","Calm", "Disgust","Fear", "Happy", "Neutral", "Sad","Surprise"]


def detach_audios(video,subtitle):
    multimodal.video_division(video,subtitle)
    if os.path.exists('static/audio'): 
        shutil.rmtree('static/audio')
        
    os.makedirs('static/audio')
    
    for count in range(len(os.listdir('static/video/'))):
        filename='static/video/video' + str(count) + '.mp4'
        video = moviepy.editor.VideoFileClip(filename)
        audio = video.audio
    #Replace the parameter with the location along with filename
        audio_file="static/audio/audio"+str(count)+".mp3"
        audio.write_audiofile(audio_file) 
        count+=1
    return 

def audio(path):
    predictions={}
    audio_fpath = path
    audio_clips = os.listdir(audio_fpath)
    model = tf.keras.models.load_model("audio_15_epochs.h5")

    for i in range(len(audio_clips)):
        x, sr = librosa.load(audio_fpath+audio_clips[i], sr=44100)
        librosa.display.waveplot(x, sr=sr)
        X = librosa.stft(x)
        Xdb = librosa.amplitude_to_db(abs(X))
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
        plt.axis('off')
        fname="static/audio/audioimage"+str(i)+".jpeg"
        plt.savefig(fname, bbox_inches='tight', pad_inches=0)
        plt.close()
        img = image.load_img(fname, target_size=(300, 300))
        x = image.img_to_array(img)
            #img = cv2.resize(img,(150,150))
        img = x.reshape( -1,300, 300,3)

        classes = model.predict(img)
        pred=Category[np.argmax(classes)]
        if  pred=="Angry" or pred=="Disgust" or pred=="Fear" or pred=="Sad":
            pred="Negative"  
        elif pred=="Calm" or pred=="Surprise" or pred=="Happy" :  
            pred="Positive"
        elif pred=="Neutral":
            pred="Neutral"
        else:
            pred="Neutral"
        predictions[audio_fpath+audio_clips[i]]=pred

        os.remove(fname)

    return predictions

#detach_audios("D:/FYP/7th Semester/Test Videos/selena-gomez-this-is-the-year-official.mp4","D:/FYP/7th Semester/Test Videos/thiss the year.vtt")
#print(audio("static/audio/"))
