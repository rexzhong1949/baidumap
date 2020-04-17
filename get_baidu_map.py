'''
用途：从百度地图获取指定区域的地图图片。
如百度、谷歌等地图都是采用瓦片方式来组织地图的。
以百度地图为例，大地图被切分256*256的小图片，并按行列序号进行命名。
下载了这些小图片后，可以把它们拼接成大地图图片。
地图库里的图片是分级的，英文叫Zoom，就是地图软件里放大缩小的那个参数。
Zoom值越大，地图越细。（注意：不同Zoom值用的是不同的地图文件）
下面介绍如何获取某个经纬度区域某个Zoom值的瓦片值范围。
我用的Chrome浏览器，打开https://map.baidu.com网页，在屏幕下方找到“地图开放平台”，点击进入百度地图开放平台。
翻到下面，找到“工具支持”里面的 “坐标拾取器”，点击后打开了可拾取坐标的页面。
选择目标城市，找到你的目标区域，并用鼠标滚轮调整到你想要的Zoom。
按F12调出控制台，在顶部选择Network，监控访问的Url。
这时容易发现，控制台窗口里捕获的访问的Url形如：
https://maponline3.bdimg.com/tile/?qt=vtile&x=23143&y=6684&z=17&styles=pl&scaler=2&udt=20200407&from=jsapi2_0
其中的x=23143&y=6684&z=17就是我们要获取的瓦片编号，x为行号，y为列号，z就是Zoom值。
这样，我们就能获得我们想要的区域的瓦片编号范围了，把瓦片范围输入到代码中，就能把地图图片提取到相应目录。
另外，百度地图的原点是在左下角。个人觉得，在北半球，x增大表示往东，y增大表示往北。
'''

import requests
import os
import glob


def getTileByXYZ():  # 根据x，y，z参数获取瓦片
    #先清除目录下的png文件
    p = "./cdZoomImg"
    #获取目录下所有扩展名为png的文件的名字列表plst
    del_list = glob.glob(os.path.join(p, '*.png'))
    for f in del_list:
        if os.path.isfile(f):
            os.remove(f)

#    z = 17  #zoom值
#    xidx = [23140, 23169]   #x值范围
#    yidx = [6690, 6709]     #y值范围
    z = 19  #zoom值
    xidx = [92575, 92605]   #x值范围
    yidx = [26767, 26787]     #y值范围
    for y in range(yidx[0], yidx[1] + 1):
        for x in range(xidx[0], xidx[1] + 1):
            url = "http://online3.map.bdimg.com/tile/?qt=tile&x={x}&y={y}&z={z}&styles=pl" \
                  "&scaler=1&udt=20200401".format(x=x, y=y, z=z)
            savePngByXYZ(url, x, y, z)
        print("download map {y}/{all}".format(y=y, all=yidx[1]))


def savePngByXYZ(url, x, y, z=17):  # 保存图片
    r = requests.get(url)
    sname = "./cdZoomImg/cd_{x}_{y}.png".format(x=x, y=y)  # 注意这里对文件名的命名规则，在小图片拼接成大图片时有用
    with open(sname, 'ab') as pngf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pngf.write(chunk)
                pngf.flush()

getTileByXYZ()