import cv2
import numpy as np


def img_ascii(img, r=3):
    # img: input img
    # r:  raito params #由于不同控制台的字符长宽比不同，所以比例需要适当调整。
    # window cmd：r=3/linux console r=

    grays = "@%#*+=-:. "  # 由于控制台是白色背景，所以先密后疏/黑色背景要转置一下
    gs = 10  # 10级灰度
    # grays2 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^.` "
    # gs2 = 67              #67级灰度

    # 宽（列）和高（行数）
    w = img.shape[1]
    h = img.shape[0]
    ratio = r * float(w) / h  # 调整长宽比-根据终端改变r

    scale = w // 100  # 缩放尺度/取值步长，向下取整，每100/50个像素取一个 值越小图越小(scale 越大)

    for y in range(0, h, int(scale * ratio)):  # 根据缩放长度 遍历高度 y对于h，x对应w
        strline = ''
        for x in range(0, w, scale):  # 根据缩放长度 遍历宽度
            idx = img[y][x] * gs // 255  # 获取每个点的灰度  根据不同的灰度填写相应的 替换字符
            if idx == gs:
                idx = gs - 1
            strline += grays[idx]  # 写入控制台
        print(strline)
        # sys.stdout.flush()


def print256():
    # 控制带自带的256色输出功能，demo如下
    # from：#https://askubuntu.com/questions/821157/print-a-256-color-test-pattern-in-the-terminal

    print("Color indexes should be drawn in bold text of the same color.")

    colored = [0] + [0x5f + 40 * n for n in range(0, 5)]  # array combined [0, 95, 135, 175, 215, 255]
    colored_palette = [
        "%02x/%02x/%02x" % (r, g, b)  # 转为16进制
        for r in colored
        for g in colored
        for b in colored
    ]

    grayscale = [0x08 + 10 * n for n in range(0, 24)]
    grayscale_palette = [
        "%02x/%02x/%02x" % (a, a, a)
        for a in grayscale
    ]

    normal = "\033[38;5;%sm"
    bold = "\033[1;38;5;%sm"
    reset = "\033[0m"

    for (i, color) in enumerate(colored_palette + grayscale_palette, 16):
        index = (bold + "%4s" + reset) % (i, str(i) + ':')
        hex = (normal + "%s" + reset) % (i, color)
        newline = '\n' if i % 6 == 3 else ''
        print(index, hex, newline, )
    ##ref
    # https://en.wikipedia.org/wiki/ANSI_escape_code
    # https://github.com/grawity/code/blob/master/term/xterm-color-chooser
    # https://unix.stackexchange.com/questions/404414/print-true-color-24-bit-test-pattern/404415#404415


def get_color_dict():
    based = range(0, 16)
    based_palette = [
        "%02x" % l  # 转为16进制
        for l in based
    ]

    colored = [0] + [0x5f + 40 * n for n in range(0, 5)]  # array combined [0, 95, 135, 175, 215, 255]
    colored_palette = [
        "%02x%02x%02x" % (r, g, b)  # 转为16进制
        for r in colored
        for g in colored
        for b in colored
    ]

    grayscale = [0x08 + 10 * n for n in range(0, 24)]
    grayscale_palette = [
        "%02x/%02x/%02x" % (a, a, a)
        for a in grayscale
    ]

    color_256 = based_palette + colored_palette + grayscale_palette
    # 生成一个字典
    color_dict = {color: i for (i, color) in enumerate(color_256)}
    # 通过rgb值近似到00/5f/87/af/d7/ff来得到彩色值

    # 输出显示各种颜色
    index = ''
    for (i, color) in enumerate(color_256):
        index += "\033[38;5;%sm#" % i  # 其中#为各个颜色的输出显示
    # print(index)

    return color_dict


# 首先定义函数，利用颜色字典将RGB颜色转换为真彩对应数值
def cvtrgb(rgb, color_dict):
    xx = ''
    # 根据上面生成的颜色字典来，对于不同取值区间赋予不同的值
    for i in range(3):
        if rgb[i] < 95:
            xx += '00'
        elif rgb[i] < 135:
            xx += '5f'
        elif rgb[i] < 175:
            xx += '87'
        elif rgb[i] < 215:
            xx += 'af'
        elif rgb[i] < 225:
            xx += 'd7'
        else:
            xx += 'ff'
    name = ''.join(xx)

    value = color_dict[name]
    return value


# 随后对输入图进行遍历，将所有的RGB值转换为相应的真彩值
def cvtimg(img, color_dict):
    ascii_img = np.array(img[:, :, 0], dtype=np.string_)
    for h in range(img.shape[0]):
        for w in range(img.shape[1]):
            ascii_img[h, w] = cvtrgb(img[h, w, :], color_dict)  # 调用换色函数
    return ascii_img  # 返回值中每一个像素已经是真彩值


def img_color_ascii(img, r=3):
    # img: input img
    # r:  raito params #由于不同控制台的字符长宽比不同，所以比例需要适当调整。
    # window cmd：r=3/linux console r=

    grays = "@%#*+=-:. "  # 由于控制台是白色背景，所以先密后疏/黑色背景要转置一下
    gs = 10  # 10级灰度
    # grays2 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^.` "
    # gs2 = 67              #67级灰度

    # 宽（列）和高（行数）
    w = img.shape[1]
    h = img.shape[0]
    ratio = r * float(w) / h  # 调整长宽比-根据终端改变r

    scale = w // 100  # 缩放尺度/取值步长，向下取整，每100/50个像素取一个 值越小图越小(scale 越大)

    for y in range(0, h, int(scale * ratio)):  # 根据缩放长度 遍历高度 y对于h，x对应w
        strline = ''
        for x in range(0, w, scale):  # 根据缩放长度 遍历宽度
            idx = img[y][x] * gs // 255  # 获取每个点的灰度  根据不同的灰度填写相应的 替换字符
            if idx == gs:
                idx = gs - 1  # 防止溢出
            # 改变这里，将真彩值利用命令行格式化输出赋予
            color_id = "\033[38;5;%sm%s" % (img[y][x], grays[2])  # 输出！
            strline += color_id  # 按行写入控制台
        print(strline)


if __name__ == "__main__":
    img0 = cv2.imread("zxm.png")
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()

    # 使用前面定义的颜色字典，颜色转换函数cvtrgb和图像映射哈数cvtimg
    ass = cvtimg(img, get_color_dict())
    # ass = np.array(ass, dtype=np.int)  # 将array转化为int类型
    ass = np.array(ass, dtype=np.int32)  # 将array转化为int类型
    img_color_ascii(ass, 2.5)  # 彩色绘图函数,r=2.5调整比例,由于命令行行距存在需要微调r因子
