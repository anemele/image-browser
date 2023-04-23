"""前端设计"""
import tkinter as tk


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Image Browser')
        self.geometry('1080x720')  # GUI 尺寸
        # self.resizable(False, False)  # 不可调整大小

        # 显示提示信息
        self.label_banner = tk.Label(self, font=('bold', 16))
        # 放置图片和名字
        self.frame_image = tk.Frame(self)
        # 显示图片名称
        self.label_image_name = tk.Label(self.frame_image, text='Picture Name')
        # 显示图片内容
        self.label_image_content = tk.Label(self.frame_image)

        self.label_banner.pack(pady=5)
        self.frame_image.pack(pady=5)
        self.label_image_name.pack(pady=10)
        self.label_image_content.pack(anchor=tk.CENTER)

    def raise_info(self, msg: str):
        self.label_banner.config(text=msg)
        # 显示时间 2 秒
        self.label_banner.after(2000, lambda: self.label_banner.config(text=''))


if __name__ == '__main__':
    GUI().mainloop()
