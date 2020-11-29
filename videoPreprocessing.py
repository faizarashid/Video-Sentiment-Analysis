# Importing all necessary libraries 
from cv2 import cv2 
import os 
import shutil
import numpy as np
import face_recognition
from matplotlib import pyplot as plt
import moviepy.editor
import tensorflow as tf
import glob

def video_into_frames():

  
    # Read the video from specified path 
    cam = cv2.VideoCapture("static/sample.mp4") 
    
    try: 
        
        # creating a folder named data 
        if os.path.exists('static/data'): 
            shutil.rmtree('static/data')
        
        os.makedirs('static/data')
       
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 
    
    # frame 
    currentframe = 0
    
    while(True): 
        
        # reading from frame 
        ret,frame = cam.read() 
    
        if ret: 
            # if video is still left continue creating images 
            name ='static/data/frame' + str(currentframe) + '.jpg'
            #print ('Creating...' + name) 
    
            # writing the extracted images 
            cv2.imwrite(name, frame) 
    
            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += 1
        else: 
            break
    
    # Release all space and windows once done 
    print("frames",currentframe)
    cam.release() 
    cv2.destroyAllWindows() 

def video_from_frames(fps):
    img_array = []
#count=0

    for count in range(len(os.listdir('static/data'))):
        #print (count)
        #print (len(os.listdir('/content/data')))
        
        filename = 'static/data/frame' + str(count) + '.jpg'
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    out = cv2.VideoWriter('static/project.avi',fourcc, fps, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def combine_audio(vidname, audname, outname,fps):
	import moviepy.editor as mpe
	my_clip = mpe.VideoFileClip(vidname)
	audio_background = mpe.AudioFileClip(audname)
	final_clip = my_clip.set_audio(audio_background)
	final_clip.write_videofile(outname,fps=fps) 

def predict():
    facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    Category = ["Angry", "Disgust","Fear", "Happy", "Neutral", "Sad","Surprise"]
    #Category = ["Negative", "Neutral","Positive"]
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    model = tf.keras.models.load_model("model.h5")
    # Initialize variables
    face_locations = []
    
    for count in range(len(os.listdir('static/data'))):
        # Grab a single frame of video
        filename = 'static/data/frame' + str(count) + '.jpg'
        # Quit when the input video file ends
        frame = cv2.imread(filename)
        
        
       
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        
        gray_fr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find all the faces in the current frame of video
        
        face_locations = facec.detectMultiScale(gray_fr, 1.3, 5,minSize=(48, 48))
        #print(rgb_frame.shape,gray_fr.shape)
        # Display the results
        #    x    y       w      h
        face=0
        for top, right, bottom, left in face_locations:
            # Draw a box around the face
            face=face+1
        
            fc = gray_fr[right:right+left, top:top+bottom]
        
            #plt.imshow(cv2.cvtColor(fc, cv2.COLOR_BGR2RGB),cmap="gray")
            #plt.show()
            roi = cv2.resize(fc, (48, 48))
            
            prediction=model.predict(roi[np.newaxis, :, :, np.newaxis])
            pred=Category[np.argmax(prediction)]
            # Blue color in BGR 
            if pred=="Negative" or pred=="Angry" or pred=="Disgust" or pred=="Fear" or pred=="Sad":
                rgb_value=(0,0,255)

            elif pred=="Neutral":
                rgb_value=(255,0,0)
            elif pred=="Positive" or pred=="Surprise" or pred=="Happy" :  
                rgb_value=(0,255,0)
            cv2.putText(frame, pred, (top,right), font, 1, rgb_value, 2)
            #print("left : ",left," Top: ",top," Right: ",right," Bottom: ",bottom)
            cv2.rectangle(frame, (top,right), (top+bottom,right+left),rgb_value, 2)
            
        # Display the resulting image
            #plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            #plt.show()
        
        
        if os.path.isfile(filename):
            cv2.imwrite(filename, frame)
            if pred=="Negative" or pred=="Angry" or pred=="Disgust" or pred=="Fear" or pred=="Sad":
                cv2.imwrite('static/Image/negative/frame'+ str(count) + '.jpg', frame)
            elif pred=="Neutral":
                cv2.imwrite('static/Image/neutral/frame'+ str(count) + '.jpg', frame)

            elif pred=="Positive" or pred=="Surprise" or pred=="Happy" :  
                cv2.imwrite('static/Image/positive/frame'+ str(count) + '.jpg', frame)

    

def video(path):
    
    # Replace the parameter with the location of the video
    video = moviepy.editor.VideoFileClip("static/sample.mp4")
    audio = video.audio
    #Replace the parameter with the location along with filename
    audio.write_audiofile("static/audio.mp3") 
    
   # video_into_frames()
    #predict()
    cam = cv2.VideoCapture("static/sample.mp4") 
    fps = cam.get(cv2.CAP_PROP_FPS)
    video_from_frames(fps)
    
    combine_audio("static/project.avi","static/audio.mp3","static/projectwithaudio.mp4",25)
def image_extract():
    
    # Replace the parameter with the location of the video
    video = moviepy.editor.VideoFileClip("static/sample.mp4")
    audio = video.audio
    #Replace the parameter with the location along with filename
    audio.write_audiofile("static/audio.mp3") 
    
    video_into_frames()
    predict()

    
def video_extract():
    video = moviepy.editor.VideoFileClip("static/sample.mp4")
    audio = video.audio
    #Replace the parameter with the location along with filename
    audio.write_audiofile("static/audio.mp3") 
    
    try: 
        
        # creating a folder named data 
        if os.path.exists('static/Video') :
            shutil.rmtree('static/Video')
        
        os.makedirs('static/Video')
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 
    #video_into_frames()
    #predict()

    
