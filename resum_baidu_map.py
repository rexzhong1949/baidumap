'''
用途：将下载到本地的百度地图小图片拼接成大图片
一系列小图片放在目录"./cdZoomImg"中，文件名例如“cd_23140_6690.png”
其中23140代表横坐标，6690代表列坐标。
在拼接大图的时候，先把图拼成竖长的条形图，然后再合成为大图。

'''
import os
import glob
from PIL import Image
import numpy as np

def complieImg():
    #先清除目标目录下的png文件
    p = "./complexLevel"
    #获取目录下所有扩展名为png的文件的名字列表plst
    del_list = glob.glob(os.path.join(p, '*.png'))
    for f in del_list:
        if os.path.isfile(f):
            os.remove(f)

    # 命名规则：cd_x_y.png 左下坐标系
    # 同一个x 同1列，y增加，图片在上面
    # 假设输入排好序了
    p = "./cdZoomImg"
    #获取目录下所有扩展名为png的文件的名字列表plst
    plst = glob.glob(os.path.join(p, '*.png'))
    #假设文件已排好序，因此x的最小值就是第一个文件plst[0]中的第一个数字
    #plst[0]是一个字符串，形如“./cdZoomImg\cd_23140_6690.png”
    #(plst[0].split("\\")是以字符\来分割字符串“./cdZoomImg\cd_23140_6690.png”，
    # 得到一个列表['./cdZoomImg', 'cd_23140_6690.png']。
    #所以plst[0].split("\\")[1]就是字符串'cd_23140_6690.png'。然后再用字符.来分割，得到
    #字符串列表['cd_23140_6690', 'png']，再用字符_来分割字符串'cd_23140_6690'，取第二个元素，就得到了23140
    xmin = ((plst[0].split("\\")[1]).split(".")[0]).split('_')[1]
    #print(xmin)

    # 3维数组
    alst = []

    qlst = []

    '''
    遍历文件列表,具有相同横坐标的文件的文件名、横坐标、纵坐标形成列表，用于后面拼接。
    '''
    row_num = xmin
    for f in plst:
        # 将文件名解析成列表，形如：['cd', '23140', '6690']
        w = ((f.split("\\")[1]).split(".")[0]).split('_')
        w[0] = f
        #w成为形如['./cdZoomImg\\cd_23140_6690.png', '23140', '6690']的列表

        if w[1] == row_num: #将行号相同的文件名列表加入到qlst
            qlst.append(w.copy())
        else:   #读到另外的行号，表示前面一个行号的文件名列表提取完毕，都在qlst里面，将qlst加入到alst
            alst.append(qlst.copy())

            #更新目标行号，并清空qlst，用于存放新行号的文件名列表
            row_num = w[1]
            qlst = []   #清空qlst，用于容纳新的行
            qlst.append(w.copy())   #目前w里面是新行的第一个文件名，若没有这一行，将导致图像的底部缺失一块拼图。


    #计算最终生成的大图的长和宽。每个小图片都是256*256，256 * len(alst[0])代表纵向长度，256 * len(alst)代表横向宽度
    m2 = [256 * len(alst[0]), 256 * len(alst)]  # im2=Image.new('RGBA', (m2[0], m2[1]))
    print(m2)
    psave = "./complexLevel"
    file_num = len(alst)
    file_saved_num = 0
    for k in alst:  # k里面装的是x相同的值，y应该递增
        plen = len(k)   #alst中的每个元素都是一个列表，容纳要排成一个竖排图像的文件名列表
        msize = [256, 256 * (plen + 1)]
        #创建一个指定大小的图像文件，它的大小就是一个竖条图片的大小。
        toImage = Image.new('RGBA', (msize[0], msize[1]))
        for i in range(plen):
            #逐个读取一个竖条图片中的文件，再粘贴到目标文件中指定位置
            fromImage = Image.open(k[plen - i - 1][0])
            toImage.paste(fromImage, (0 * msize[0], i * msize[0]))  #x坐标固定为0是因为竖条图片的宽度也是256，等于要粘贴的图片的宽度
        sname = "/m_{x}.png".format(x=k[0][1])
        toImage.save(psave + sname)
        file_saved_num += 1
        print( "file saved {file_saved_num} of {file_num}".format(file_saved_num=file_saved_num,file_num=file_num ))
    print("complieImg finished!")

def complieImgInY():
    # 合并长条形图片，x变化，y不变. 长图是complieImg()里生成的
    p = "./complexLevel"
    plst = glob.glob(os.path.join(p, '*.png'))
    xmin = ((plst[0].split("\\")[1]).split(".")[0]).split('_')[1]
    ima21 = Image.open(plst[0])
    w = np.array(ima21).shape

    psave = "./complexLevel"
    plen = len(plst)
    msize = [w[1] * plen, w[0]]

    toImage = Image.new('RGBA', (int(msize[0]), int(msize[1])))
    for i in range(plen):
        fromImage = Image.open(plst[i])
        toImage.paste(fromImage, (int(i * 256), 0))
    sname = "/01-final_Map.png"
    toImage.save(psave + sname)  # 保存图片
    print("Create 01-final_Map.png finished!!!")

complieImg()
complieImgInY()