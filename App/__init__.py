# 在App 文件夹下建立一个__init__.py
"""
The flask application package.

"""

# 实例化一个flask 应用
import os
from flask import Flask
from config import config

app = Flask(__name__)

#添加配置信息
app.config.from_object(config.get('development'))

# 
data_folder = app.config['DATA_FOLDER']

# 模型文件
model_dir = os.path.join(app.config['MODEL_FOLDER'],app.config['MODEL_FILENAME'])

# 上传文件夹
upload_folder = app.config['UPLOAD_FOLDER']
# 允许的后缀
allowed_extensions = app.config['ALLOWED_EXTENSIONS']
# 引入当前模块下的内容


from . import views

