"""图片处理器"""
from typing import Optional, Tuple

import PIL
from PIL import Image, ImageTk


_weight = 1000  # 显示图片的最大宽度
_height = 660  # 显示图片的最大高度


class ImageProcessor:
    def _auto_scale(self, image: Image.Image) -> Tuple[int, int]:
        # 图片适配 GUI，适当缩放，返回应当缩放的尺寸
        width, height = image.size  # 原图尺寸
        rate = width / height  # 宽高比
        if width > height:
            # 如果是横图，则宽度填满，高度随宽度缩放
            scale_width = _weight
            scale_height = scale_width / rate
        else:
            # 如果是竖图，则反过来
            scale_height = _height
            scale_width = scale_height * rate
        return int(scale_width), int(scale_height)

    def _convert_image(self, image: Image.Image) -> ImageTk.PhotoImage:
        # 获取缩放尺寸
        width, height = self._auto_scale(image)
        # 缩放图片
        new_image = image.resize((width, height), Image.ANTIALIAS)
        # 转化为PhotoImage图片，否则无法插入Label对象
        return ImageTk.PhotoImage(image=new_image)

    def open(self, file: str) -> Optional[ImageTk.PhotoImage]:
        try:
            image = Image.open(file)
            return self._convert_image(image)
        except PIL.UnidentifiedImageError:
            pass
