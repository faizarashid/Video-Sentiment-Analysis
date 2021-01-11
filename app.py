from flask import Flask, render_template,request,send_from_directory,redirect,url_for,Request,Response
import videoPreprocessing
from werkzeug.utils import secure_filename
import os,re,time
import textPreprocessing
import audioPreprocessing
import multimodal
import mimetypes
from shutil import copyfile
import shutil
from flask import request, send_file, Response
app = Flask(__name__)




UPLOAD_FOLDER='D:/FYP/7th Semester/Video-Sentiment-Analysis/static/'
app.config['UPLOAD_EXTENSIONS'] = ['.mp4','.srt']
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
@app.route('/test')
def test():
    return render_template('multimodal.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
def send_file_partial(path):
    """ 
        Simple wrapper around send_file which handles HTTP 206 Partial Content
        (byte ranges)
        TODO: handle all send_file args, mirror send_file's error handling
        (if it has any)
    """
    range_header = request.headers.get('Range', None)
    if not range_header: return send_file(path)
    
    size = os.path.getsize(path)    
    byte1, byte2 = 0, None
    
    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()
    
    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1
    
    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 
        206,
        mimetype=mimetypes.guess_type(path)[0], 
        direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv
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
        files=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],"text"))
        return render_template('extractedtext.html',files=files) 
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
        files=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],"Image"))
        return render_template('extractedimage.html',files=files)
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
        files=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],"audio"))
        return render_template('extractedaudio.html',files=files)
   
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
      multimodal.video_division(pathvideo,pathtext)
      timestamps=multimodal.mutimodal_analysis(pathvideo,pathtext)
     
      new_file_name = "output" + str(time.time()) + ".mp4"
      os.rename(os.path.join(app.config['UPLOAD_FOLDER'], "output.mp4"),
                    os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
      if request.form['submit_button'] == 'Extract Video':
        count=0
        if os.path.exists('static/video/positive'): 
            shutil.rmtree('static/video/Positive')
            shutil.rmtree('static/video/Negative')
            shutil.rmtree('static/video/Neutral')
        os.makedirs('static/video/Positive')
        os.makedirs('static/video/Negative')
        os.makedirs('static/video/Neutral')
        for key,value in timestamps.items():
            src='static/video/output'+str(count)+".mp4"
            if value=="Positive":
              dst='static/video/Positive/output'+str(count)+'.mp4'
            elif value=="Negative":
              dst='static/video/Negative/output'+str(count)+'.mp4' 
            else:
              dst='static/video/Neutral/output'+str(count)+'.mp4'
            print(src,dst)
            copyfile(src, dst)
            count+=1
        return render_template('extractedvideo.html')

      return render_template('multimodal.html',filename=new_file_name,timestamps=timestamps)
      




if __name__ == '__main__':
    app.run(debug=True)
