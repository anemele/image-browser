from pathlib import Path
from typing import Dict, Optional, Tuple

from PIL import ImageTk

from .constants import WALLPAPER_SRC_PATH
from .utils.deque import DeQueue
from .utils.imgpro import open_image


class Backend:
    def __init__(self):
        files = [file for file in WALLPAPER_SRC_PATH.glob('*') if file.is_file()]

        # a circular linked list, save the image file path
        self._image_path_queue: DeQueue = DeQueue(files)
        # key: image file path，value: ImageTk.PhotoImage
        self._image_content: Dict[Path, Optional[ImageTk.PhotoImage]] = {
            file: None for file in files
        }

    def _get_image(self, filepath: Path) -> Optional[Optional[ImageTk.PhotoImage]]:
        """依据路径尝试加载图片，加载失败则自动更新。"""
        if self._image_content.get(filepath) is not None:
            return self._image_content[filepath]

        image = open_image(filepath)
        if image is None:
            self._image_path_queue.pop()
            self._image_content.pop(filepath)
            if len(self._image_path_queue) == 0:
                return

        self._image_content[filepath] = image
        return self._image_content[filepath]

    @property
    def next(self) -> Optional[Tuple[Path, ImageTk.PhotoImage]]:
        while True:
            filepath = self._image_path_queue.next()
            if filepath is None:
                break
            image = self._get_image(filepath)
            if image is not None:
                return filepath, image

    @property
    def prev(self) -> Optional[Tuple[Path, ImageTk.PhotoImage]]:
        while True:
            filepath = self._image_path_queue.prev()
            if filepath is None:
                break
            image = self._get_image(filepath)
            if image is not None:
                return filepath, image

    @property
    def here(self) -> Optional[Tuple[Path, ImageTk.PhotoImage]]:
        filepath = self._image_path_queue.here()
        if filepath is None:
            return
        image = self._get_image(filepath)
        if image is not None:
            return filepath, image
