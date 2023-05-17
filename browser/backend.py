""" backend tasks """
import os
import os.path


from .constants import WALLPAPER_SRC_PATH, WALLPAPER_DST_PATH
from .utils.deque import DeQueue
from .utils.imgpro import open_image


class Backend:
    def __init__(self):
        # a circular linked list, save the image file path
        self._image_path_queue = DeQueue()
        # key: image file path，value: ImageTk.PhotoImage
        self._image_content = dict()

        self._src_path = WALLPAPER_SRC_PATH
        self._save_path = WALLPAPER_DST_PATH

        files = filter(
            os.path.isfile,
            (os.path.join(self._src_path, sth) for sth in os.listdir(self._src_path)),
        )
        for file in files:
            self._image_path_queue.append(file)
            self._image_content[file] = None

    def _get_image(self, filepath: str, n: bool, /):
        """
        依据路径尝试加载图片，加载失败则自动更新。
        :param filepath:
        :param n: 调用是否来自 _next_image
        :return:
        """
        if self._image_content[filepath] is not None:
            return filepath, self._image_content[filepath]

        image = open_image(filepath)
        if image is None:
            self._image_path_queue.pop()
            self._image_content.pop(filepath)
            if len(self._image_path_queue) == 0:
                return
            if n:
                return self._next_image()
            else:
                return self._prev_image()
        self._image_content[filepath] = image
        return filepath, self._image_content[filepath]

    def _next_image(self):
        filepath = self._image_path_queue.next()
        return self._get_image(filepath, True)

    def _prev_image(self):
        filepath = self._image_path_queue.prev()
        return self._get_image(filepath, False)

    def _here_image(self):
        filepath = self._image_path_queue.here()
        return self._get_image(filepath, False)
