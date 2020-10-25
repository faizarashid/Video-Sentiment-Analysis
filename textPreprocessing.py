from keras.preprocessing.sequence import pad_sequences
import keras.preprocessing.text
import keras.preprocessing
import time
import matplotlib.pyplot as plt
from pylab import figure, axes, pie, title, show
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import  numpy as np
import webvtt
from webvtt import WebVTT, Caption
from nltk.tokenize import sent_tokenize, word_tokenize
import re,os,shutil
import pickle


model = tf.keras.models.load_model("text_model_lstm.h5")
with open('tokenizer.pickle', 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)
def clean_text(data):
    
    # remove hashtags and @usernames
    data = re.sub(r"(#[\d\w\.]+)", '', data)
    data = re.sub(r"(@[\d\w\.]+)", '', data)
    
    # tekenization using nltk
    data = word_tokenize(data)
    
    return data
def predict(message):
    
    class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']
    max_seq_len=500
    message = [message]

    
    #texts=clean_text(message)

    seq = loaded_tokenizer.texts_to_sequences(message)
    padded = pad_sequences(seq, maxlen=max_seq_len)
    
    pred = model.predict(padded)

    return class_names[np.argmax(pred)]

def file_writing(path):
    vtt = WebVTT()
    caption = Caption()
    emotion=""
    
    for line in webvtt.read('static/subtitle.vtt'):
        emotion=predict(str(line.text))
        
        if emotion == "joy":
            caption = Caption(line.start,line.end,"<c.green> "+emotion+": "+line.text+"</c>")
            
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
        elif emotion == "anger":
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
        elif emotion == "sadness":
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
        elif emotion == "neutral":
            caption = Caption(line.start,line.end,"<c.blue> "+emotion+": "+line.text+"</c>")
        vtt.captions.append(caption)
    vtt.save('static/my_captions.vtt')
    

def text_extract():
    try: 
        
        # creating a folder named data 
        if os.path.exists('static/Text'): 
            shutil.rmtree('static/Text')
        
        os.makedirs('static/Text')
        
        
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 
    vtt_pos = WebVTT()
    vtt_neg = WebVTT()
    vtt_neu = WebVTT()
    caption = Caption()
    emotion=""
    
    for line in webvtt.read('static/subtitle.vtt'):
        emotion=predict(str(line.text))
        
        if emotion == "joy":
            caption = Caption(line.start,line.end,"<c.green> "+emotion+": "+line.text+"</c>")
            vtt_pos.captions.append(caption)
        elif emotion == "anger" or emotion == "sadness" or emotion == "fear":
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
            vtt_neg.captions.append(caption)
        elif emotion == "neutral":
            caption = Caption(line.start,line.end,"<c.blue> "+emotion+": "+line.text+"</c>")
            vtt_neu.captions.append(caption)
        
    vtt_pos.save('static/Text/positive.vtt')
    vtt_neg.save('static/Text/negative.vtt')
    vtt_neu.save('static/Text/neutral.vtt')
    

            
      






