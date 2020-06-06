import os
import sys
import cv2

def video_to_frame(video_src_path, frame_save_path, frame_width=720, frame_height=480, interval=10):
    """
    将视频按固定间隔读取写入图片
    :param video_src_path: 视频所在位置
    :param frame_save_path:　保存视频帧文件夹
    :param frame_width:　保存帧宽
    :param frame_height:　保存帧高
    :param interval:　保存帧间隔
    :return:　帧图保存文件夹路径
    """

    cap = cv2.VideoCapture(video_src_path)
    frame_index = 0
    frame_count = 0
    if cap.isOpened():
        success = True
        # 视频名
        video_name = video_src_path.replace('\\','/').split('/')[-1][:-5]
        print(f'正在读取{video_name}')
        if not os.path.exists(frame_save_path):
            # 创建文件夹
            os.makedirs(frame_save_path)
        save_folder = os.path.join(frame_save_path,video_name)
    else:
        success = False
        print("读取失败!")
    while (success):
        success, frame = cap.read()
        print("\r---> 正在读取第%d帧:" % frame_index, success,end='', flush=True)
        if frame_index % interval == 0 and success:  
            resize_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(save_folder + "_%d.jpg" % frame_count, resize_frame)
            frame_count += 1
        frame_index += 1
    cap.release()
    print()
    return True

