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
import re
import pickle

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
    model = tf.keras.models.load_model("text_model_lstm.h5")
    
    #texts=clean_text(message)
    with open('tokenizer.pickle', 'rb') as handle:
      loaded_tokenizer = pickle.load(handle)
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
        elif emotion == "fear":
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
        elif emotion == "anger":
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
        elif emotion == "sadness":
            caption = Caption(line.start,line.end,"<c.red> "+emotion+": "+line.text+"</c>")
        elif emotion == "neutral":
            caption = Caption(line.start,line.end,"<c.blue> "+emotion+": "+line.text+"</c>")
        vtt.captions.append(caption)
    vtt.save('static/my_captions.vtt')
    
    

            
      






