from flask import Flask, render_template,request,send_from_directory,redirect,url_for,Request,Response
import videoPreprocessing
from werkzeug.utils import secure_filename
import os,re,time
import textPreprocessing


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
        return "<h1>Text Extracted Please check Text folder with in Static folder </h1>"  
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
        videoPreprocessing.video()
        
        new_file_name = "projectwithaudio" + str(time.time()) + ".mp4"
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "projectwithaudio.mp4"),
                    os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
        return render_template('display.html',filename=new_file_name)
      if request.form['submit_button'] == 'Extract Images':

        videoPreprocessing.video_extract()
        return "<h1>Text Extracted Please check Image folder with in Static folder </h1" 
        #return render_template('extractimage.html')
      if request.form['submit_button'] == 'Extract Text':
          textPreprocessing.text_extract()

if __name__ == '__main__':
    app.run(debug=True)
