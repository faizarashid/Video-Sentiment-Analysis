def video_from_frames(fps,path):
    img_array = []
#count=0
    filelist = glob.glob("static/data/*.jpg")
    print(filelist)
    for infile in sorted(filelist): 
    #do some fancy stuff

        #print (count)
        #print (len(os.listdir('/content/data')))
        
        print(infile)
        img = cv2.imread(infile)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    if path is 'static/data':
     out = cv2.VideoWriter('static/project.avi',fourcc, fps, size)
    elif path is 'static/Image/positive':
     out = cv2.VideoWriter('static/Video/positive.avi',fourcc, fps, size)
    elif path is 'static/Image/negative':
     out = cv2.VideoWriter('static/Video/negative.avi',fourcc, fps, size)
    elif path is 'static/Image/neutral':
     out = cv2.VideoWriter('static/Video/positive.avi',fourcc, fps, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()




    video_from_frames(25,'static/Image/positive')
    video_from_frames(25,'static/Image/negative')
    video_from_frames(25,'static/Image/nuetral')



    
def audio(path):
    audio_fpath = path
    audio_clips = os.listdir(audio_fpath)
    model = tf.keras.models.load_model("audio_model_2.h5")
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
        print(fname,pred)
        os.remove(fname)
    return

def mutimodal_analysis(video,subtitle):
    #loop iterate through folder which contains video files
    #Detach audio from videos
    #perform text, video, audio analysis on data
    #combine videos
    #display video
    audioPreprocessing.detach_audios(video,subtitle)
    predictions=audioPreprocessing.audio("static/audio/")
    for i in range(len(audio_clips)):
        videoPreprocessing.video_into_frames()
        videoPreprocessing.predict()
        videoPreprocessing.video_from_frames(fps=30)


    return

 cam = cv2.VideoCapture("static/sample.mp4") 
        fps = cam.get(cv2.CAP_PROP_FPS)
        videoPreprocessing.video_from_frames(fps)
        predFile='static/video/Pvideo'+str(i)+'mp4'
        videoPreprocessing.combine_audio(fname,audname,predFile,fps)