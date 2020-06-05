from . import main
from App import data_folder,upload_folder,model_dir
from .utils import video_to_frame
from  .vgg import vgg_model
import os
import numpy as np
import tensorflow as tf
from flask import current_app,render_template,url_for,abort,flash
from PIL import Image

@main.route('/<filename>')
def index(filename=None):
    video_dir = os.path.join(upload_folder,filename)
    # 去除后缀
    frame_folder = os.path.join(data_folder,filename[:-5])
    # 帧数图对象数组
    frames = []
    try:
        # 当解帧成功
        if video_to_frame(video_dir,frame_folder):
            for f in os.listdir(frame_folder):
                # 把所有帧数对应的url和文件名带后缀等
                frames.append({
                    'src':url_for('static',filename=f'data/{filename[:-5]}/{f}'),
                    'name':f
                })
    except Exception as e:
        print(e)
        abort(500)
    # 闪现消息提示成功
    flash("video to frame success!",category='success')
    # 生成预测该视频对应url
    text = url_for('main.predict',filename=filename)
    return render_template(
        'result.html',
        title = 'Frames',
        is_frame = True,
        frames = frames,
        text = text
    )


# 预测视频结果
@main.route('/predict/<filename>')
def predict(filename):
    line = []
    # 帧数图文件夹
    frame_folder = os.path.join(data_folder,filename[:-5])
    # 加载模型
    model = vgg_model(model_dir)
    # 得到所有的帧图
    filelist = os.listdir(frame_folder)
    for file in filelist:  
        # 以list的方式显示目录下的各个文件夹或者图片的名字
        image_path = os.path.join(frame_folder,file)
        img = Image.open(image_path)
        img = img.resize((32, 32), Image.ANTIALIAS)
        img_arr = np.array(img)
        # img_arr = 255 - img_arr
        img_arr = img_arr / 255.0
        # print("img_arr:", img_arr.shape)
        x_predict = img_arr[tf.newaxis, ...]
        # print("x_predict:", x_predict.shape)

        # 使用模型返回预测结果
        result = model.predict(x_predict)
        pred = tf.argmax(result, axis=1)
        # tf.print(pred)

        # 处理结果
        p = np.array(pred)
        #print("it is:", p)

        if p == [0]:
            line.append({'label':0,'filename':file})

        elif p == [1]:
            line.append({'label':1,'filename':file})

        elif p == [2]:
            line.append({'label':2,'filename':file})

        elif p == [3]:
            line.append({'label':3,'filename':file})
        #p.tolist()
        #line.append(p)
    # print(line)

    # 为返回为echart 的数据
    label = []
    frame = []
    for item in line:
        label.append(item['label'])
        frame.append(item['filename'])
        item['filename'] = url_for('static',filename=f"data/{filename[:-5]}/{item['filename']}")
        if item['label'] == 0:
            item['label'] = '特写'
        elif item['label'] == 1:
            item['label'] = '近景'
        elif item['label'] == 2:
            item['label'] = '中景'
        elif item['label'] == 3:
            item['label'] = '远景'
        
    return render_template(
        'result.html',
        title='Result',
        is_result = True,
        label = label,
        frame = frame,
        line = line
    )