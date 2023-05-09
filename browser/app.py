"""主程序"""
import hashlib
import os
import os.path
import shutil

import filetype

from .backend import Backend
from .gui import GUI


class App(GUI, Backend):
    def __init__(self):
        GUI.__init__(self)
        Backend.__init__(self)

        self.bind('<Left>', lambda _: self.display(False))  # 小键盘左键 ←
        self.bind('<Right>', lambda _: self.display())
        self.bind('<Up>', lambda _: self.display(False))  # 小键盘上键 ↑
        self.bind('<Down>', lambda _: self.display())
        self.bind('<Escape>', lambda _: self.destroy())
        self.bind('<Control-q>', lambda _: self.destroy())
        self.bind('<MouseWheel>', lambda e: self.display(e.delta < 0))
        # 双击左键，保存图片
        self.label_image_content.bind('<Double-Button-1>', self.save_image)

        # 展示第一张图片
        self.display()
        self.mainloop()

    def display(self, is_next: bool = True):
        if len(self._image_path_queue) == 0:
            self.raise_info('[Error] no image found')
            return

        if is_next:
            result = self._next_image()
        else:
            result = self._prev_image()

        if result is None:
            return
        filename, image = result

        self.label_image_name.config(
            text=f'[{self._image_path_queue.idx + 1}/{len(self._image_path_queue)}] '
            f'{os.path.basename(filename)}'
        )
        self.label_image_content.config(image=image)
        # 预留缓冲，防止图片滚动过快闪烁
        self.label_image_content.after(20)

    @staticmethod
    def get_dst(path: str) -> str:
        # 计算 md5 值，判断文件类型、获取后缀名，组成目标文件名
        # 即 <md5>.<ext>
        with open(path, 'rb') as fp:
            content = fp.read()
        hash_md5 = hashlib.md5(content)
        ext = filetype.guess_extension(content)
        if ext is None:
            return hash_md5.hexdigest()
        else:
            return f'{hash_md5.hexdigest()}.{ext}'

    def save_image(self, _):
        # 保存当前图片
        if len(self._image_path_queue) == 0:
            self.raise_info('[Error] no image to save')
            return

        # 获取当前图片路径
        src, _ = self._here_image()
        filename = self.get_dst(src)
        # 获取保存路径
        dst = os.path.join(self._save_path, filename)
        # 判断是否已经存储该图片
        if os.path.exists(dst):
            self.raise_info(f'[INFO] exists {filename}')
        else:
            shutil.copy(src, dst)
            self.raise_info(f'[INFO] saved {filename}')
