#!/usr/bin/env python
from Logger import Logger
import os


class Processes(Logger):
    IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webm"]

    @classmethod
    def find_dirs(cls, queue, paths):
        self = cls()
        paths = map(os.path.expanduser, paths)
        dirs = []
        for path in paths:
            skip = True
            for folder, _, _ in os.walk(path):
                if skip:
                    skip = False
                    continue
                for _, _, files in os.walk(folder):
                    images = []
                    for f in files:
                        ext = os.path.splitext(f)[1]
                        if ext in cls.IMAGE_EXTS:
                            images.append(os.path.join(folder, f))
                    if images:
                        self.logger.debug("For %s gallery, %s files found" %
                                          (folder, images))
                        dirs.append((folder,
                                     sorted(images, key=lambda f: f.lower())))
                    break
        queue.put(dirs)
        queue.close()
