import os

from app.constants import *
from app.utils import *

__all__ = [
    'Backend'
]


class Backend:
    """
    GUI 与用户交互，后端程序完成任务，实现前后端分离。
    """

    def __init__(self):
        self._image_path = CircleList()  # 循环链表保存图片路径
        self._image_content = dict()  # 图片路径为key，ImageTk.PhotoImage对象为value
        self._image_processor = ImageProcessor()  # 图片处理器，依据路径返回ImageTk.PhotoImage对象

        user_path = os.path.expanduser('~')  # 获取当前用户文件夹路径
        self._src_path = os.path.join(user_path, SRC_PATH)
        self._save_path = os.path.join(ROOT_PATH, SAVE_PATH)
        if not os.path.exists(self._save_path):
            os.makedirs(self._save_path)

    def _clear_cache(self):
        """
        清空文件信息
        :return:
        """
        self._image_path.clr()
        self._image_content.clear()

    def _load_files_info(self, subdir: bool = False):
        """
        读取image path路径，将该路径下所有文件信息加载到内存。
        此处实施懒加载，初始只读取路径信息，使用时才加载图片内容。
        如果非图片，则删除。
        （另需内存管理调度，图片过多时会占用大量内存）
        :param subdir: 是否搜索子目录，默认不搜索
        :return:
        """
        self._clear_cache()

        def walk(path):
            for top, _, files in os.listdir(path):
                for sth in files:
                    filepath = os.path.join(top, sth)
                    if os.path.isfile(filepath):
                        yield filepath

        def listdir(path):
            for sth in os.listdir(path):
                filepath = os.path.join(path, sth)
                if os.path.isfile(filepath):
                    yield filepath

        func = walk if subdir else listdir
        for file in func(self._src_path):
            self._image_path.add(file)
            self._image_content[file] = None

    def _to_label_image(self, filepath: str):
        return filepath, self._image_content[filepath]

    def _get_image(self, filepath: str, *, n: bool):
        """
        依据路径尝试加载图片，加载失败则自动更新。
        :param filepath:
        :param n: 调用是否来自 _next_image
        :return:
        """
        if self._image_content[filepath] is not None:
            return self._to_label_image(filepath)

        # 此处传参 func=0，日常使用都是查看锁屏壁纸，保留宽图
        # 如果做其它用途，参看函数文档
        # 最好的方法是外部接收参数，不必修改源码
        image = self._image_processor.open_and_convert(filepath, func=0)
        if image is None:
            self._image_path.rmv()
            self._image_content.pop(filepath)
            if len(self._image_path) == 0:
                return
            if n:
                return self._next_image()
            else:
                return self._prev_image()
        self._image_content[filepath] = image
        return self._to_label_image(filepath)

    def _next_image(self):
        """
        读取下一张图片
        :return:
        """
        filepath = self._image_path.next()
        return self._get_image(filepath, n=True)

    def _prev_image(self):
        filepath = self._image_path.prev()
        return self._get_image(filepath, n=False)

    def _here_image(self):
        filepath = self._image_path.here()
        return self._get_image(filepath, n=False)  # 加载失败，默认上一张
