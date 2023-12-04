""" main program """
import hashlib
import shutil
from pathlib import Path

try:
    import filetype
except ImportError:
    filetype = None

from .backend import Backend
from .constants import WALLPAPER_DST_PATH
from .gui import GUI


class App(GUI):
    def __init__(self):
        GUI.__init__(self)

        self._backend = Backend()

        self.bind('<Left>', lambda _: self.display(False))  # left ←
        self.bind('<Right>', lambda _: self.display())
        self.bind('<Up>', lambda _: self.display(False))  # up ↑
        self.bind('<Down>', lambda _: self.display())
        self.bind('<Escape>', lambda _: self.destroy())
        self.bind('<Control-q>', lambda _: self.destroy())
        self.bind('<MouseWheel>', lambda e: self.display(e.delta < 0))
        # double click to save the current image
        self.label_image_content.bind('<Double-Button-1>', self.save_image)

        # initial display
        self.display()
        self.mainloop()

    def display(self, is_next: bool = True):
        index = self._backend._image_path_queue.idx
        if index is None:
            self.raise_info('[ERROR] no image found')
            return
        length = len(self._backend._image_path_queue)

        result = self._backend.next if is_next else self._backend.prev
        if result is None:
            self.raise_info('[ERROR] no image found')
            return
        path, image = result

        self.label_image_name.config(text=f'[{ index+ 1}/{length}]  {path.name}')
        self.label_image_content.config(image=image)
        # a delay to avoid (flash)?
        self.label_image_content.after(20)

    def save_image(self, _):
        # get the source path
        here = self._backend.here
        if here is None:
            self.raise_info('[ERROR] no image to save')
            return
        src, _ = here
        filename = get_dst(src)

        # get the destiny path
        dst = WALLPAPER_DST_PATH / filename

        if dst.exists():
            self.raise_info(f'[INFO] exists {filename}')
        else:
            shutil.copy(src, dst)
            self.raise_info(f'[INFO] saved {filename}')


def get_dst(path: Path) -> str:
    # return a filename with format <md5>.<ext>
    content = path.read_bytes()

    hexdigest = hashlib.md5(content).hexdigest()

    if filetype is None:
        return hexdigest

    ext = filetype.guess_extension(content)
    return hexdigest if ext is None else f'{hexdigest}.{ext}'
