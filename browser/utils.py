from io import BytesIO

import PIL
from PIL import Image, ImageTk

__all__ = [
    'CircleList',
    'ImageProcessor'
]


# 循环表
class CircleList(list):
    def __init__(self):
        super().__init__()
        self.__offset = -1

    @property
    def idx(self):
        if self.__len__() == 0:
            return -1
        return self.__offset % self.__len__()

    def add(self, obj):
        self.append(obj)

    def rmv(self):
        self.pop(self.idx)

    def clr(self):
        self.clear()
        self.__offset = -1

    def upd(self, obj):
        self[self.idx] = obj

    def here(self):
        return self[self.idx]

    def next(self):
        self.__offset += 1
        return self.here()

    def prev(self):
        self.__offset -= 1
        return self.here()


# 图片处理器
class ImageProcessor:
    _weight = 1000  # 显示图片的最大宽度
    _height = 660  # 显示图片的最大高度

    def _auto_scale(self, image: Image.Image):
        # 将图片适配GUI，做适当缩放，返回应当缩放的尺寸
        width, height = image.size  # 获取原图尺寸
        rate = width / height  # 宽高比
        if width > height:  # 如果是横图，则宽度填满，高度随宽度缩放
            scale_width = self._weight
            scale_height = scale_width / rate
        else:  # 如果是竖图，则反过来
            scale_height = self._height
            scale_width = scale_height * rate
        return int(scale_width), int(scale_height)

    @staticmethod
    def open_image(file: str):
        # ~~此处使用缓存，避免二次打开文件，产生过多系统调用~~
        # ~~读取文件，转换为 Image 对象，同时识别其文件类型~~
        # 设计不周，耦合太高，就此罢了
        try:
            with open(file, 'rb') as fp:
                bytes_ = fp.read()
            image = Image.open(BytesIO(bytes_))
            # ext = filetype.guess_extension(bytes_)
            return image  # , ext
        except PIL.UnidentifiedImageError:
            pass

    def convert_image(self, image: Image.Image):
        width, height = self._auto_scale(image)  # 获取缩放尺寸
        new_image = image.resize((width, height), Image.ANTIALIAS)  # 缩放图片
        photo_image = ImageTk.PhotoImage(image=new_image)  # 转化为PhotoImage图片，否则无法插入Label对象
        return photo_image

    def open_and_convert(self, file: str, *, func: int = None):
        """
        打开并转化图片
        :param file: 图片路径
        :param func: 可选，过滤规则。
        0:保留宽图
        1:保留长图
        :return:
        """

        image = self.open_image(file)
        if image is None:
            return

        if (func is None) \
                or (func == 0 and image.width > image.height) \
                or (func == 1 and image.width < image.height):
            return self.convert_image(image)
