"""
Image Browser GUI
前端设计与调试
"""
import tkinter as tk
from tkinter import ttk

__all__ = [
    'GUI'
]


class FrameInfo(tk.Frame):

    def __init__(self, master, **kwargs):
        super(FrameInfo, self).__init__(master, **kwargs)

        self.label_banner = tk.Label(self, font=('bold', 16))

        self.layout_gui()

    def layout_gui(self):
        self.label_banner.pack(pady=5)

    def raise_info(self, msg: str):
        self.label_banner.config(text=msg)
        # 显示时间 2 秒
        self.label_banner.after(2000, lambda: self.label_banner.config(text=''))


class FrameImage(tk.Frame):

    def __init__(self, master, **kwargs):
        super(FrameImage, self).__init__(master, **kwargs)

        self.label_image_name = tk.Label(self, text='Picture Name')  # 显示图片名称的标签
        self.label_image_content = tk.Label(self, text='')  # 显示图片内容的标签

        self.layout_gui()

    def layout_gui(self):
        self.label_image_name.pack(pady=10)
        self.label_image_content.pack(anchor=tk.CENTER)


class MenuBar(tk.Menu):

    def __init__(self, master, **kwargs):
        super(MenuBar, self).__init__(master, **kwargs)

        self.file_menu = tk.Menu(self, tearoff=False)

        self.config_gui()

    def config_gui(self):
        self.add_cascade(
            label='File',
            menu=self.file_menu
        )


class MenuPost(tk.Menu):

    def __init__(self, master, **kwargs):
        super(MenuPost, self).__init__(master, **kwargs)

        # self.add_command(label='♥')
        # self.add_command(label='📂')


class GUI(tk.Tk):
    init_title = 'Image Browser'

    def __init__(self):
        super().__init__()

        self.frame_info = FrameInfo(self)  # 显示信息
        self.frame_image = FrameImage(self)  # 显示图片
        # self.menu_bar = MenuBar(self, tearoff=False)  # 菜单栏
        self.menu_post = MenuPost(self, tearoff=False)  # 右键菜单
        # self.tk_btn = Toplevel(self, background='#CCCCCC', padx=10, pady=10)

        self.config_gui()  # 配置界面
        self.layout_gui()  # 布局界面
        # self.tk_btn.init_pos()  # 设置按钮位置

    def set_title(self, path: str = None):
        if path is None:
            self.title(self.init_title)
        else:
            self.title(f'{self.init_title} - {path}')

    def config_gui(self):
        self.set_title()
        self.geometry('1080x720')  # GUI 尺寸
        # self.resizable(False, False)  # 不可调整大小
        # self.config(menu=self.menu_bar)
        self.frame_image.label_image_content.bind(
            '<Button-3>', lambda event: self.menu_post.post(event.x_root, event.y_root)
        )

    def layout_gui(self):
        self.frame_info.pack()
        self.frame_image.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)


class Toplevel(tk.Toplevel):

    def __init__(self, master, **kwargs):
        super(Toplevel, self).__init__(master, **kwargs)

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

    def init_pos(self):
        # 菜单栏靠右水平居中
        self.master.update()  # 查看窗口尺寸、坐标信息前，必须先update
        self.set_pos(
            int(self.master.winfo_x() + self.master.winfo_width() * 0.9),
            int(self.master.winfo_y() + self.master.winfo_height() / 2)
        )

    def set_pos(self, x, y):
        self.geometry('+{}+{}'.format(x, y))


if __name__ == '__main__':
    GUI().mainloop()
