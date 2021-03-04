#-------------------------------------#
#   调用摄像头或者视频进行检测
#   调用摄像头直接运行即可
#   调用视频可以将cv2.VideoCapture()指定路径
#   视频的保存并不难，可以百度一下看看
#-------------------------------------#
import time
import os
import cv2
import numpy as np
from PIL import Image

from yolo import YOLO

def processvideo(srcfileabspath, dstpath):
    
    #-------------------------------------#
    #   调用摄像头
    #   capture=cv2.VideoCapture("1.mp4")
    #-------------------------------------#
    #capture=cv2.VideoCapture(0)
    #capture=cv2.VideoCapture("./img/IMG_20210102_130548.MOV")
    capture=cv2.VideoCapture(srcfileabspath)
    #capture = cv2.VideoCapture("./img/ch05_20150922082426t_0829-00.05.01.267-00.05.13.456.mp4")
    #capture = cv2.VideoCapture("./curve/objs/1/result.mp4")
    fps = 0.0
    fno = 0
    findex = 0
    #resultpath = "./curve/objs/"
    resultpath = dstpath
    ret = True

    dstpath = resultpath # + str(findex)
    isExists = os.path.exists(dstpath)

    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(dstpath) 
        print(dstpath +' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(dstpath +' 目录已存在')    

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 视频编解码器
    fps = capture.get(cv2.CAP_PROP_FPS)  # 帧数
    width, height = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 宽高
    out = cv2.VideoWriter(dstpath + '/result.mp4', fourcc, fps, (width, height))  # 写入视频
    '''
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)  # 写入帧
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q退出
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    '''
    while(True):
        t1 = time.time()
        # 读取某一帧
        ref,frame=capture.read()
        
        if ref == True:

            #frameplay = frame
            
            # 格式转变，BGRtoRGB
            #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            frame, ref = yolo.detect_image(frame, dstpath, fno)
            frame = np.array(frame)
            if ret == True:
                print(ret)
            #frame, boxes = yolo.detect_image(frame)
            
            # RGBtoBGR满足opencv显示格式
            #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            fps  = ( fps + (1./(time.time()-t1)) ) / 2
            #print("fps= %.2f"%(fps))
            frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if ref == True:
                out.write(frame)  # 写入帧

            frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            cv2.imshow("video",frame)
            fno += 1                
        else:
            break

        c= cv2.waitKey(1) & 0xff 
        if c==ord('q'): #==27:
            capture.release()
            ret = False
            break
        '''
        if ref == True:
            #out.write(frame)  # 写入帧
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q退出
                break
        else:
            break
        '''
    capture.release()
    out.release()
    cv2.destroyAllWindows()

    return ret

def show_files(path, all_abs_files, all_files):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path, all_abs_files, all_files)
        else:
            all_abs_files.append(os.path.abspath(cur_path)) # + file)
            all_files.append(file)

    return all_abs_files, all_files

yolo = YOLO()
resultlst = []
# 传入空的list接收文件名
abs_contents, filename = show_files("/home/wsun/srcvideo/10.30.11.182/TBC/", [], [])
# 循环打印show_files函数返回的文件名列表
for path in abs_contents:
    print(os.path.dirname(path))
    print(os.path.splitext(path)[0])

    src = path
    dst = os.path.splitext(path)[0]

    if (src.endswith(".mp4") or src.endswith(".mov") or src.endswith(".MOV")) and "result.mp4" not in src:
        print(src)
        ret = processvideo(src, dst)
        if ret == False:
            break
        else:
            resultlst.append(dst)
for item in resultlst:            
    print(item)
print("Finished")            