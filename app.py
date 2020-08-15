from flask import Flask, render_template,request,send_from_directory,redirect,url_for,Request,Response
import videoPreprocessing
from werkzeug.utils import secure_filename
import os,re,mimetypes


app = Flask(__name__)




UPLOAD_FOLDER='D:/FYP/VSA/static/'
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
      videoPreprocessing.video()
      return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)
