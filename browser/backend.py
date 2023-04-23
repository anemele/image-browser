"""后端任务"""
import os
import os.path

from .utils.deque import DeQueue
from .utils.imgpro import ImageProcessor

_USER_PATH = os.path.expanduser('~')
WALLPAPER_SRC_PATH = os.path.join(
    _USER_PATH,
    'AppData/Local/Packages/'
    'Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/'
    'LocalState/Assets',
)
WALLPAPER_DST_FILE = 'savepath.txt'

try:
    with open(WALLPAPER_DST_FILE, encoding='utf-8') as _fp:
        WALLPAPER_DST_PATH = _fp.read().strip()
    if not os.path.exists(WALLPAPER_DST_PATH):
        os.makedirs(WALLPAPER_DST_PATH)
except (FileNotFoundError, UnicodeDecodeError) as e:
    print(e)
    WALLPAPER_DST_PATH = os.path.join(_USER_PATH, 'Pictures')


class Backend:
    def __init__(self):
        # 循环链表，保存图片路径
        self._image_path_queue = DeQueue()
        # key: 图片路径，value: ImageTk.PhotoImage
        self._image_content = dict()
        # 图片处理器，输入文件路径，返回 ImageTk.PhotoImage 对象
        self._image_processor = ImageProcessor()

        self._src_path = WALLPAPER_SRC_PATH
        self._save_path = WALLPAPER_DST_PATH

        files = filter(
            os.path.isfile,
            (os.path.join(self._src_path, sth) for sth in os.listdir(self._src_path)),
        )
        for file in files:
            self._image_path_queue.append(file)
            self._image_content[file] = None

    def _get_image(self, filepath: str, *, n: bool):
        """
        依据路径尝试加载图片，加载失败则自动更新。
        :param filepath:
        :param n: 调用是否来自 _next_image
        :return:
        """
        if self._image_content[filepath] is not None:
            return filepath, self._image_content[filepath]

        image = self._image_processor.open(filepath)
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
        return self._get_image(filepath, n=True)

    def _prev_image(self):
        filepath = self._image_path_queue.prev()
        return self._get_image(filepath, n=False)

    def _here_image(self):
        filepath = self._image_path_queue.here()
        # 加载失败，加载上一张
        return self._get_image(filepath, n=False)
