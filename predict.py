'''
predict.py有几个注意点
1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用Image.open打开图片文件进行预测。
2、如果想要保存，利用r_image.save("img.jpg")即可保存。
3、如果想要获得框的坐标，可以进入detect_image函数，读取top,left,bottom,right这四个值。
4、如果想要截取下目标，可以利用获取到的top,left,bottom,right这四个值在原图上利用矩阵的方式进行截取。
'''
import os
from PIL import Image
import cv2
import numpy as np
from yolo import YOLO

yolo = YOLO()
findex = 0
resultpath = "./curve/objs/pic/"

dstpath = resultpath + str(findex)
isExists = os.path.exists(dstpath)

if not isExists:
    # 如果不存在则创建目录
    # 创建目录操作函数
    os.makedirs(dstpath) 
    print(dstpath +' 创建成功')
else:
    # 如果目录存在则不创建，并提示目录已存在
    print(dstpath +' 目录已存在')    
while True:
    img = input('Input image filename:')
    try:
        image = Image.open(img)
    except:
        print('Open Error! Try again!')
        continue
    else:
        r_image, ret = yolo.detect_image(image, dstpath, findex)
        '''
        # 进行裁剪并保存到本地
        box = boxes
        savepath = "./curve/objs/"
        for i in range(boxes.shape[0]):
            # top, left, bottom, right = boxes[i]
            # 或者用下面这句等价
            top = boxes[i][0]
            left = boxes[i][1]
            bottom = boxes[i][2]
            right = boxes[i][3]

            top = top - 5
            left = left - 5
            bottom = bottom + 5
            right = right + 5

            # 左上角点的坐标
            top = int(max(0, np.floor(top + 0.5).astype('int32')))

            left = int(max(0, np.floor(left + 0.5).astype('int32')))
            # 右下角点的坐标
            bottom = int(min(np.shape(image)[0], np.floor(bottom + 0.5).astype('int32')))
            right = int(min(np.shape(image)[1], np.floor(right + 0.5).astype('int32')))

            # embed()

            # 问题出在这里：不能用这个方法，看两个参数是长和宽，是从图像的原点开始裁剪的，这样肯定是不对的
            # 指定裁剪的目标范围
            uncroped_image = np.array(image.copy())
            croped_region = uncroped_image[top:bottom,left:right]# 先高后宽
            # 将裁剪好的目标保存到本地
            cv2.imwrite(savepath + str(i)+".jpg",croped_region)
        '''
        r_image.show()
