# WSG84原来就会有一个警告，但是我把它忽略了
import math
import numpy as np
import pickle
from PIL import Image
import imageio
from geographiclib.geodesic import Geodesic
from geopy.geocoders import Nominatim


# ----------------------------------------haversine增强
def calc_azimuth(lat1, lon1, lat2, lon2):
    version = 2
    if version == 1:
        lat1_rad = lat1 * math.pi / 180
        lon1_rad = lon1 * math.pi / 180
        lat2_rad = lat2 * math.pi / 180
        lon2_rad = lon2 * math.pi / 180

        y = math.sin(lon2_rad - lon1_rad) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - \
            math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)

        bear = math.atan2(y, x) * 180 / math.pi

        return float((bear + 360.0) % 360.0)

        # 所谓方位角是与正北方向、顺时针之间的夹角
        # 来源：https://blog.sina.com.cn/s/blog_12d84817c0102wngo.html
    if version == 2:
        geo_dict = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
        az = geo_dict['azi1']
        return az


# -------------------------------------------python增强
def int_matrix(matrix):
    # 对int（）的增强，使之能用于矩阵
    # 传地址
    row = np.shape(matrix)[0]
    col = np.shape(matrix)[1]
    for i in range(row):
        for j in range(col):
            matrix[i, j] = int(matrix[i, j])
    return


def save_variable(variable, name):
    f = open(name, 'wb')  # 打开或创建名叫name的文档，此文件不需要有拓展名
    pickle.dump(variable, f)  # 在文件filename中写入v
    f.close()  # 关闭文件，释放内存。
    return name


def load_variable(name):
    try:
        f = open(name, 'rb')  # 表示以二进制方式读取
        r = pickle.load(f)
        f.close()
        return r

    except EOFError:
        return ""


def ndarray2img(name, arr):
    arr = arr/[np.max(arr)]
    arr *= 255  # 变换为0-255的灰度值
    im = Image.fromarray(arr)
    im = im.convert('RGB')  # 这样才能转为灰度图，如果是彩色图则改L为‘RGB’
    imageio.imsave(name, im)
    return


# ---------------------------------------------numpy增强
def argsort_matrix(matrix, order):
    # 本函数是用来补足np.sort无法对矩阵进行计算的问题
    # 本函数目前有一个问题是不知道它的相同大小元素是怎么摆顺序的
    # 本函数产出的索引好像是默认浮点型，必须int一下才可以用
    index = np.zeros([1, np.size(matrix)])
    arr = np.reshape(matrix, [1, np.size(matrix)])  # 这是拉长之后的矩阵
    if order == 1:  # 升序
        index = np.argsort(arr)  # 这是拉长之后矩阵的索引，一维数组
    if order == -1:  # 降序
        index = np.argsort(-arr)
    if order != 1 and order != -1:
        return 'order error'
    count = 0  # 这是数数
    index_of_matrix = np.zeros([np.size(matrix), 2])  # 这是矩阵的索引，第一行是最值的位置
    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]):            # 这个二重循环也许只需要一重就行了
            row = math.floor((index[0, count]+1)/np.shape(matrix)[1])  # 这是index_of_matrix第count行的点所在原矩阵的行数
            col = (index[0, count]+1) % np.shape(matrix)[1]
            if col == 0:
                col = 6
            index_of_matrix[count, 0] = row
            index_of_matrix[count, 1] = col-1
            count += 1
    return index_of_matrix


def matrixlizing_function(func_name, matrix, aug):
    # 本函数是用来使用所有的函数都可以输入矩阵的
    func_result = []
    if aug == 1:
        for i in matrix:
            a = func_name(i)
            func_result.append(a)
    if aug == 2:
        # 两个参数的要求matrix是两个同型矩阵的列表
        aug1 = matrix[0].T
        aug2 = matrix[1].T
        for i in range(len(aug1)):
            a = func_name(aug1[i], aug2[i])
            func_result.append(a)
    return func_result


def get_location_by_name(name):
    geolocator = Nominatim(user_agent='nwkami')
    location = geolocator.geocode(name)
    return [location, location.latitude, location.longitude]
