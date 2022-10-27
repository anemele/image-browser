"""
Image Browser Main Program

"""
import hashlib
import os
import shutil
from tkinter import filedialog

import filetype

from browser.backend import *
from browser.gui import *

__all__ = [
    'Application'
]


class Application(GUI, Backend):  # 继承GUI类
    def __init__(self):
        GUI.__init__(self)
        Backend.__init__(self)

        self.config_gui()
        self.init()  # App 初始化
        self.focus_force()  # 获取焦点

    def config_gui(self):
        # 按钮绑定方法
        self.tk_btn.btn_next.config(command=lambda: self._display())
        self.tk_btn.btn_prev.config(command=lambda: self._display(-1))
        self.tk_btn.btn_save.config(command=self._save_image)
        self.tk_btn.btn_open_dir.config(command=self._open_dir)

        self.bind('<Left>', lambda e: self._display(-1))  # 小键盘左键 ←
        self.bind('<Right>', lambda e: self._display())
        self.bind('<Control-q>', lambda e: self._exit_app())
        self.bind('<MouseWheel>',
                  lambda event: self._display(-1)
                  if event.delta > 0
                  else self._display())
        self.label_image_content.bind('<Double-Button-1>', lambda event: self._save_image())  # 双击左键，保存

    def init(self):
        subdir = False  # 默认不遍历子目录
        self._load_files_info(subdir)  # 加载文件信息
        self.title(f'{self.init_title} - {self._src_path}')
        self._display()  # 展示第一张图片

    def _display(self, direction: int = 1):
        """
        展示图片
        :param direction: 文件列表指针移动方向，0是当前，1是向下，-1是向上
        :return:
        """
        if len(self._image_path) == 0:
            self.raise_info('No image found')
            return

        if direction == 1:
            result = self._next_image()
        elif direction == -1:
            result = self._prev_image()
        elif direction == 0:
            result = self._here_image()
        else:
            return
        if result is None:
            return
        filename, image = result

        self.label_image_name.config(text='[%d/%d] %s' % (
            self._image_path.idx + 1,
            len(self._image_path),
            os.path.basename(filename)
        ))
        self.label_image_content.config(image=image)
        self.label_image_content.after(20)  # 预留缓冲，防止图片滚动过快闪烁

    def _save_image(self):
        if len(self._image_path) == 0:
            self.raise_info('No image to save.')
            return

        def get_dst(path):
            with open(path, 'rb') as fp:
                content = fp.read()
            hash_md5 = hashlib.md5(content)
            ext = filetype.guess_extension(content)
            if ext is None:
                return hash_md5.hexdigest()
            else:
                return f'{hash_md5.hexdigest()}.{ext}'

        src, _ = self._here_image()
        filename = get_dst(src)
        dst = os.path.join(self._save_path, filename)
        if os.path.exists(dst):
            self.raise_info(f'[Exists] {filename}')
        else:
            shutil.copy(src, dst)
            self.raise_info(f'[Saved] {filename}')

    def _open_dir(self):
        path = filedialog.askdirectory()
        if path:
            self._src_path = path
            self.label_image_name.config(text='Picture Name')
            self.label_image_content.config(image=None)
            self.init()

    def _exit_app(self):
        self.destroy()
