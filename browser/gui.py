"""
Image Browser GUI
前端设计与调试
"""
import tkinter as tk
from tkinter import ttk

__all__ = [
    'GUI'
]


class GUI(tk.Tk):
    init_title = 'Image Browser'

    def __init__(self):
        super().__init__()

        self.frame_info = tk.Frame(self)  # 信息组件
        self.label_info = tk.Label(self.frame_info, font=('bold', 16))  # 提示信息，替代 messagebox
        self.frame_image = tk.Frame(self)  # 显示图片的框架，背景颜色为紫色，RGB
        self.label_image_name = tk.Label(self.frame_image, text='Picture Name')  # 显示图片名称的标签
        self.label_image_content = tk.Label(self.frame_image, text='')  # 显示图片内容的标签

        self.tk_btn = Toplevel(self, background='#CCCCCC', padx=10, pady=10)
        self.update()  # 查看窗口尺寸、坐标信息前，必须先update
        self.tk_btn.set_pos(int(self.winfo_x() + self.winfo_width() - 100),
                            int(self.winfo_y() + self.winfo_height() / 2))

        self.config_gui()  # 配置界面
        self.layout_gui()  # 布局界面

    def run(self):
        self.mainloop()

    def set_title(self, path: str = None):
        if path is None:
            self.title(self.init_title)
        else:
            self.title(f'{self.init_title} - {path}')

    def config_gui(self):
        self.set_title()
        # self.geometry('1080x720')  # GUI尺寸
        # self.resizable(False, False)  # 不可调整大小

    def layout_gui(self):
        self.frame_info.pack()
        self.label_info.pack(pady=5)
        self.frame_image.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)
        self.label_image_name.pack(pady=10)
        self.label_image_content.pack(anchor=tk.CENTER)

    def raise_info(self, msg: str):
        self.label_info.config(text=msg)
        # 显示时间 2 秒
        self.label_info.after(2000, lambda: self.label_info.config(text=''))


class Toplevel(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super(Toplevel, self).__init__(*args, **kwargs)
        self.btn_next = ttk.Button(self, text='→', width=4)  # 下一张按钮
        self.btn_prev = ttk.Button(self, text='←', width=4)  # 上一张按钮
        self.btn_save = ttk.Button(self, text='♥', width=4)  # 保存按钮，将当前图片保存到 save 文件夹，相当于收藏
        self.btn_open_dir = ttk.Button(self, text='📂', width=4)

        self._offset_x = 0
        self._offset_y = 0

        self.config_gui()
        self.layout_gui()

    def config_gui(self):
        self.resizable(False, False)
        self.wm_attributes('-topmost', True)
        self.overrideredirect(True)  # -- -[] -x

        self.bind('<Button-1>', self._click)
        self.bind('<B1-Motion>', self._drag)

    def layout_gui(self):
        self.btn_prev.pack(pady=2)
        self.btn_next.pack(pady=2)
        self.btn_save.pack(pady=2)
        self.btn_open_dir.pack(pady=3)

    def _click(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _drag(self, event):
        self.set_pos(self.winfo_pointerx() - self._offset_x,
                     self.winfo_pointery() - self._offset_y)

    def set_pos(self, x, y):
        self.geometry('+{}+{}'.format(x, y))


if __name__ == '__main__':
    GUI().run()
