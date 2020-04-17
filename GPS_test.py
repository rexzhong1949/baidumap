import serial
import pynmea2
import time
import math
import base64


x = base64.b64decode("MTA2LjQ1ODE4Mzg1MTgy").decode()
y = base64.b64decode("MjkuNTcwODAwODgwNTQ5").decode()
Lnglat_bd09 = [x,y]
print("Lnglat_bd09:{x},{y}".format(x=x, y=y))

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323
def gcj02tobd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]

def wgs84togcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]

def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def millerToXY (lon, lat):
    """
    经纬度转换为平面坐标系中的x,y 利用米勒坐标系
    :param lon: 经度
    :param lat: 维度
    :return:
    """
    L = 6381372*math.pi*2
    W = L
    H = L/2
    mill = 2.3
    x = lon*math.pi/180
    y = lat*math.pi/180
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
    x = (W/2)+(W/(2*math.pi))*x
    y = (H/2)-(H/(2*mill))*y
    xy_coordinate = [int(round(x)), int(round(y))]
    return xy_coordinate


# 经纬度反算切片行列号 3857坐标系
def deg2num(lat_deg, lon_deg, zoom):
    print("deg2num:",lat_deg,lon_deg,zoom)
    lat_rad = math.radians(lat_deg)
    n = 2 ** zoom
    print(n)
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def WGS84_to_WebMercator(lng, lat):
    '''
    实现WGS84向web墨卡托的转换
    :param lng: WGS84经度
    :param lat: WGS84纬度
    :return: 转换后的web墨卡托坐标
    '''
    x = lng * 20037508.342789 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34789 / 180
    return x, y

ser = serial.Serial("COM3", 9600)
str = '$GNRMC'
while True:
    line = ser.readline()
    str = line.decode()
    # print(str)
    if str.startswith('$GNGGA'):
        rmc_wgs84 = pynmea2.parse(str)
        print("UTC: ", rmc_wgs84.timestamp)
        print(rmc_wgs84)
        print("rmc_wgs84.gps_qual=", rmc_wgs84.gps_qual)
        if rmc_wgs84.gps_qual == 1:      #定位成功，执行后续操作
            print("origin rmc_wgs84.lon: ", rmc_wgs84.lon)
            print("origin rmc_wgs84.lat: ", rmc_wgs84.lat)
            Lng_wgs84 = float(rmc_wgs84.lon)
            Lat_wgs84 = float(rmc_wgs84.lat)
            du = int(Lng_wgs84/100.0)
            Lng_wgs84 = du + (Lng_wgs84-du*100.0)/60.0
            du = int(Lat_wgs84/100.0)
            Lat_wgs84 = du + (Lat_wgs84-du*100.0)/60.0
            print("Latitude:  ", Lng_wgs84)
            print("Longitude: ", Lat_wgs84)
            Lnglat_gcj02 = wgs84togcj02(Lng_wgs84, Lat_wgs84)
            print("Lnglat_gcj02: ", Lnglat_gcj02)
            Lnglat_bd09 = gcj02tobd09(Lnglat_gcj02[0], Lnglat_gcj02[1])
            print("Lnglat_bd09:", Lnglat_bd09)

            xxx = int(Lnglat_gcj02[0]*222866.0575/(2**(19-19)))
            yyy = int(Lnglat_gcj02[1] * 289268.1516/(2 ** (19 - 19)))
            print("像素坐标：",xxx,yyy)
            print("Tile xy:",int(xxx/256),int(yyy/256))



#3.通过百度的网络API进行转换
#http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=116.308999&y=40.059225
#通过这个API传入GPS经纬度坐标，然后获取返回值进行解析，这个方法可以在多数平台使用，缺点是需要访问网络。
