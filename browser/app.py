""" main program """
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
        if len(self._image_path_queue) == 0:
            self.raise_info('[ERROR] no image found')
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
        # a delay to avoid (flash)?
        self.label_image_content.after(20)

    @staticmethod
    def get_dst(path: str) -> str:
        # return a filename with format <md5>.<ext>
        with open(path, 'rb') as fp:
            content = fp.read()
        hash_md5 = hashlib.md5(content)
        hexdigest = hash_md5.hexdigest()
        ext = filetype.guess_extension(content)
        if ext is None:
            return hexdigest
        else:
            return f'{hexdigest}.{ext}'

    def save_image(self, _):
        if len(self._image_path_queue) == 0:
            self.raise_info('[ERROR] no image to save')
            return

        # get the source path
        src, _ = self._here_image()
        filename = self.get_dst(src)
        # get the destiny path
        dst = os.path.join(self._save_path, filename)

        if os.path.exists(dst):
            self.raise_info(f'[INFO] exists {filename}')
        else:
            shutil.copy(src, dst)
            self.raise_info(f'[INFO] saved {filename}')
