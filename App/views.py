"""
	The flask route views
"""
import os,shutil
from flask import request,json,render_template,flash,abort,send_from_directory,redirect,url_for,current_app
from werkzeug.utils import secure_filename
from App import app,upload_folder,allowed_extensions,data_folder
from .utils import make_result,allowed_file
from .main import main


@app.route('/')
def index():
    videos = os.listdir(upload_folder)
    frames = os.listdir(data_folder)
    urls = []
    if len(frames) > 0:
        for f in frames:
            urls.append({
                'src':url_for('static',filename=f"data/{f}/{f}_0.jpg"),
                'title':f"{f}.webm"
            })
    return render_template(
        'index.html',
        title='Index',
        videos=videos,
        urls=urls
    )


@app.route('/video/<filename>')
def video(filename):
    href = url_for('main.index',filename=filename)
    src = url_for('static',filename=f'uploads/{filename}')
    return render_template(
        'result.html',
        title = 'Video',
        is_video = True,
        video_src = src,
        video_href = href
    )


@app.route('/screen',methods=['GET','POST'])
def screen():
    if request.method == 'GET':
        return render_template(
            'screen.html',
            title='Record'
        )
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part',category='error')
            return make_result(message='No file part!')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        url = ''
        if file.filename == '':
            flash('No selected file',category='error')
            return make_result(message='No selected file')
        if file and allowed_file(file.filename,allowed_extensions):
            filename = secure_filename(file.filename)
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)
            file.save(os.path.join(upload_folder, filename))
            flash("upload success!",category='success')
            url = url_for('main.index',filename=filename)
        return make_result(message='upload success!',data=url),200



@app.route('/remove/<filename>',methods=['DELETE'])
def remove(filename):
    try:
        video_dir = os.path.join(upload_folder,filename)
        frame_folder = os.path.join(data_folder,filename[:-5])
        if os.path.isfile(video_dir):
            os.remove(video_dir)
        if os.path.exists(frame_folder):
            # 递归删除文件
            shutil.rmtree(frame_folder)
        return make_result(message='删除成功'),200
    except Exception as e:
        print(e)
        return make_result(message='删除失败',code=500),500



@app.errorhandler(404)
def internal_error(e):
    return render_template('error.html',error=e,code=404)


app.register_blueprint(main,url_prefix='/main')
