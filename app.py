from flask import Flask, render_template,request,send_from_directory,redirect,url_for,Request,Response
import videoPreprocessing
from werkzeug.utils import secure_filename
import os,re,time


app = Flask(__name__)




UPLOAD_FOLDER='D:/FYP/Video-Sentiment-Analysis/static/'
app.config['UPLOAD_EXTENSIONS'] = ['.mp4']
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

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/upload', methods=['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['myfile']
      path=os.path.join(app.config['UPLOAD_FOLDER'], "sample.mp4")
      f.save(path)
      for filename in os.listdir('static/'):
        if filename.startswith('projectwithaudio'):  # not to remove other files
            os.remove('static/' + filename)
      videoPreprocessing.video()
      
      new_file_name = "projectwithaudio" + str(time.time()) + ".mp4"
      os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "projectwithaudio.mp4"),
                os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
      return render_template('display.html',filename=new_file_name)

if __name__ == '__main__':
    app.run(debug=True)
