""" image processor """
from typing import Optional, Tuple

from PIL import Image, ImageTk
from PIL import UnidentifiedImageError


WIDTH = 1000  # max width of image displaying frame
HEIGHT = 660  # height of that


def _auto_scale(image: Image.Image) -> Tuple[int, int]:
    # 图片适配 GUI，适当缩放，返回应当缩放的尺寸
    width, height = image.size  # 原图尺寸
    rate = width / height  # 宽高比
    if width > height:
        # 如果是横图，则宽度填满，高度随宽度缩放
        scale_width = WIDTH
        scale_height = scale_width / rate
    else:
        # 如果是竖图，则反过来
        scale_height = HEIGHT
        scale_width = scale_height * rate
    return int(scale_width), int(scale_height)


def _convert_image(image: Image.Image) -> ImageTk.PhotoImage:
    # 获取缩放尺寸
    width, height = _auto_scale(image)
    # 缩放图片
    new_image = image.resize((width, height), Image.ANTIALIAS)
    # 转化为PhotoImage图片，否则无法插入Label对象
    return ImageTk.PhotoImage(image=new_image)


def open_image(file: str) -> Optional[ImageTk.PhotoImage]:
    try:
        image = Image.open(file)
        return _convert_image(image)
    except UnidentifiedImageError:
        pass
