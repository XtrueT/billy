<<<<<<< HEAD
# 主要依赖

`opencv-python==4.2.0.34
    Flask==1.1.2
    Pillow==7.1.2
    numpy==1.16.0
    tensorflow==2.0.0b1 
`

# 自定义
需要在App下创建模型文件夹（默认为model） 
其中保存着 tf 模型文件，须自行导入
可在 配置文件 config.py 中指定
    模型文件夹（默认为：/App/model）  
    模型文件名 （无默认，须指定文件名包含后缀）

# 功能

基本模块

1. 视频录制
2. 完成视频上传
3. 视频删除

=======
# 1
`absl-py==0.9.0
astor==0.8.1
click==7.1.2
Flask==1.1.2
gast==0.3.3
google-pasta==0.2.0
grpcio==1.29.0
h5py==2.10.0
importlib-metadata==1.6.0
itsdangerous==1.1.0
Jinja2==2.11.2
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.2
Markdown==3.2.2
MarkupSafe==1.1.1
numpy==1.18.5
opencv-python==4.2.0.34
Pillow==7.1.2
pkg-resources==0.0.0
protobuf==3.12.2
six==1.15.0
tb-nightly==1.14.0a20190603
tensorflow==2.0.0b1
termcolor==1.1.0
tf-estimator-nightly==1.14.0.dev2019060501
Werkzeug==1.0.1
wrapt==1.12.1
zipp==3.1.0`

# 2
需要在App下创建模型文件夹    
    model
其中保存着 tf 模型文件

配置文件 config.py中指定
    上传文件夹
    运行上传的文件后缀
    帧图保存位置
    模型文件夹
    模型文件名

# 3 
>>>>>>> 88f47f3f2a3fa1df34ae24f9d5e5ad3230b34769
主要模块 main

1. 完成视频解帧
2. 视频帧识别



