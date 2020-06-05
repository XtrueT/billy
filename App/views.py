"""
	The flask route views
"""
import os
from flask import request,json,render_template,flash,abort,send_from_directory,redirect,url_for,current_app
from werkzeug.utils import secure_filename
from App import app,upload_folder,allowed_extensions
from .utils import make_result,allowed_file
from .main import main


@app.route('/')
def index():
    videos = os.listdir(upload_folder)
    return render_template(
        'index.html',
        title='Index',
        videos = videos
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
            file.save(os.path.join(upload_folder, filename))
            flash("upload success!",category='success')
            url = url_for('main.index',filename=filename)
        return make_result(message='upload success!',data=url),200


@app.errorhandler(404)
def internal_error(e):
    return render_template('error.html',error=e,code=404)


app.register_blueprint(main,url_prefix='/main')
