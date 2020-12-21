from flask import Flask, render_template,request,send_from_directory,redirect,url_for,Request,Response
import videoPreprocessing
from werkzeug.utils import secure_filename
import os,re,time
import textPreprocessing
import audioPreprocessing
import multimodal
app = Flask(__name__)




UPLOAD_FOLDER='D:/FYP/7th Semester/Video-Sentiment-Analysis/static/'
app.config['UPLOAD_EXTENSIONS'] = ['.mp4','.srt']
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/demo',methods=['POST'])
def text():
    
    
    file=request.files["mysubfile"]
    path=os.path.join(app.config['UPLOAD_FOLDER'], "subtitle.vtt")
    file.save(path)
    for filename in os.listdir('static/'):
        if filename.startswith('my_captions'):  # not to remove other files
            os.remove('static/' + filename)
    if request.form['submit_button'] == 'Extract Text':
        textPreprocessing.text_extract()
        return render_template('extractedtext.html') 
    if request.form['submit_button'] == 'Upload & Visualize':
        textPreprocessing.file_writing("subtitle.vtt")
        new_file_name = "my_captions" + str(time.time()) + ".vtt"
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "my_captions.vtt"),
                    os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
        return render_template('demo.html',filename=new_file_name)

@app.route('/upload', methods=['POST'])
def upload_file():
   if request.method == 'POST' :

        # save each "charts" file
      for filename in os.listdir('static/'):
        if filename.startswith('sample'):  # not to remove other files
          os.remove('static/' + filename)
      for file in request.files.getlist('myfile'):
        if file.filename.endswith(".mp4"):
            path=os.path.join(app.config['UPLOAD_FOLDER'], "sample.mp4")
            file.save(path)
        else:
            path=os.path.join(app.config['UPLOAD_FOLDER'], "subtitles.vtt")
            file.save(path)
    
      for filename in os.listdir('static/'):
        if filename.startswith('projectwithaudio'):  # not to remove other files
            os.remove('static/' + filename)
      if request.form['submit_button'] == 'Upload & Visualize':
        videoPreprocessing.video(UPLOAD_FOLDER)
        
        new_file_name = "projectwithaudio" + str(time.time()) + ".mp4"
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "projectwithaudio.mp4"),
                    os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
        return render_template('display.html',filename=new_file_name)
      
      if request.form['submit_button'] == 'Extract Images':

        videoPreprocessing.image_extract()
        return render_template('extractedimage.html')
      elif request.form['submit_button'] == 'Extract Video':

        videoPreprocessing.video_extract()
        return render_template('extractedimage.html')
        #return render_template('extractimage.html')
      elif request.form['submit_button'] == 'Extract Text':
          textPreprocessing.text_extract()
@app.route('/audio', methods=['POST'])
def audio():
  if request.method == 'POST' :

        # save each "charts" file

    for file in request.files.getlist('myaudiofile'):
      if file.filename.endswith(".mp4"):
        path1=os.path.join(app.config['UPLOAD_FOLDER'], "sample.mp4")
        file.save(path1)
        print("file saved")
      if file.filename.endswith(".vtt"):
        path2=os.path.join(app.config['UPLOAD_FOLDER'], "subtitles.vtt")
        file.save(path2)
    
    if request.form['submit_button'] == 'Upload & Visualize':
        audioPreprocessing.detach_audios("static/sample.mp4","static/subtitles.vtt")
        dic=audioPreprocessing.audio("static/audio/")
        audioPreprocessing.audiovisualize(dic)
        new_file_name = "output" + str(time.time()) + ".mp4"
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "output.mp4"),
                    os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
        return render_template('display.html',filename=new_file_name)
      
    elif request.form['submit_button'] == 'Extract Audio':
        audioPreprocessing.detach_audios("static/sample.mp4","static/subtitles.vtt")
        dic=audioPreprocessing.audio("static/audio/")
        audioPreprocessing.audio_extract(dic)
        return render_template('extractedaudio.html')
   
@app.route('/mmanalysis', methods=['POST'])
def multi_modal():
      for filename in os.listdir('static/'):
        if filename.startswith('sample'):  # not to remove other files
          os.remove('static/' + filename)
      for file in request.files.getlist('mymmfile'):
        if file.filename.endswith(".mp4"):
            pathvideo=os.path.join(app.config['UPLOAD_FOLDER'], "sample.mp4")
            file.save(pathvideo)
        else:
            pathtext=os.path.join(app.config['UPLOAD_FOLDER'], "subtitles.vtt")
            file.save(pathtext)
    

      for filename in os.listdir('static/'):
        if filename.startswith('output'):  # not to remove other files
            os.remove('static/' + filename)
      multimodal.mutimodal_analysis(pathvideo,pathtext)
     
      new_file_name = "output" + str(time.time()) + ".mp4"
      os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "output.mp4"),
                    os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
      return render_template('multimodal.html',filename=new_file_name)
      




if __name__ == '__main__':
    app.run(debug=True)
