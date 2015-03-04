#!/usr/bin/env python

from PySide import QtCore, QtGui
from Logger import Logger
import threading
import weakref
import copy
import scandir
import os
import sys
import math
from decimal import Decimal
import Gallery
from RequestManager import RequestManager
from Search import Search


class BaseThread(threading.Thread, Logger):
    id = None

    def __init__(self, parent, **kwargs):
        super(BaseThread, self).__init__()
        self._parent = weakref.ref(parent)
        self.basesignals = self.BaseSignals()
        self.basesignals.exception.connect(self.parent.thread_exception_handler)

    class BaseSignals(QtCore.QObject):
        exception = QtCore.Signal(str, tuple)

    @property
    def parent(self):
        return self._parent()

    def _run(self):
        raise NotImplementedError

    def run(self):
        try:
            self._run()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.basesignals.exception.emit(self.id, sys.exc_info())


class GalleryThread(BaseThread):
    IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webm"]
    ARCHIVE_EXTS = [".zip"]
    id = "gallery"

    def __init__(self, parent, **kwargs):
        super(GalleryThread, self).__init__(parent)
        self.signals = self.Signals()
        self.signals.end.connect(self.parent.find_galleries_done)

    class Signals(QtCore.QObject):
        end = QtCore.Signal(list)

    def _run(self):
        self.find_galleries()

    def find_galleries(self):
        paths = map(os.path.expanduser, self.parent.dirs)
        dirs = []
        archives = []
        for path in paths:
            for base_folder, folders, files in scandir.walk(path):
                images = []
                for f in files:
                    ext = os.path.splitext(f)[-1].lower()
                    if ext in self.IMAGE_EXTS:
                        images.append(os.path.join(base_folder, f))
                    elif ext in self.ARCHIVE_EXTS:
                        archives.append(os.path.join(base_folder, f))
                if images:
                    dirs.append((base_folder,
                                 sorted(images, key=lambda f: f.lower())))
        existing_paths = [g.path for g in self.parent.galleries]
        folder_galleries = [Gallery.FolderGallery(self.parent.main_window,
                                                  r[0], r[1])
                            for r in dirs if r[0] not in existing_paths]
        archive_galleries = []
        for r in archives:
            if r in existing_paths:
                continue
            try:
                archive_galleries.append(
                    Gallery.ArchiveGallery(self.parent.main_window, r))
            except AssertionError:
                pass
        self.signals.end.emit(folder_galleries + archive_galleries)


class ImageThread(BaseThread):
    IMAGE_WIDTH = 200
    id = "image"

    def __init__(self, parent, galleries, **kwargs):
        super(ImageThread, self).__init__(parent)
        self.galleries = galleries
        self.signals = self.Signals()
        self.signals.progress.connect(self.parent.inc_progress)
        self.signals.gallery.connect(self.parent.image_generated)
        self.signals.end.connect(self.parent.image_thread_done)

    class Signals(QtCore.QObject):
        progress = QtCore.Signal(Decimal)
        gallery = QtCore.Signal(list)
        end = QtCore.Signal()

    def _run(self):
        self.generate_images()
        self.signals.end.emit()

    def generate_images(self):
        try:
            inc_val = Decimal(100.0) / Decimal(len(self.galleries))
        except ZeroDivisionError:
            return
        send_galleries = []
        for gallery in self.galleries:
            if not gallery.C_QGallery:
                if isinstance(gallery, Gallery.FolderGallery):
                    gallery.image = QtGui.QImage(gallery.files[0])
                elif isinstance(gallery, Gallery.ArchiveGallery):
                    gallery.image = QtGui.QImage()
                    assert gallery.image.loadFromData(gallery.raw_image.read())
                gallery.image = gallery.image.scaledToWidth(
                    self.IMAGE_WIDTH, QtCore.Qt.SmoothTransformation)
                send_galleries.append(gallery)
                self.signals.progress.emit(inc_val)
                if len(send_galleries) > 25:
                    self.signals.gallery.emit(send_galleries)
                    send_galleries = []
        if send_galleries:
            self.signals.gallery.emit(send_galleries)


class SearchThread(BaseThread):
    API_URL = r"http://exhentai.org/api.php"
    BASE_REQUEST = {"method": "gdata", "gidlist": []}
    API_MAX_ENTRIES = 25
    id = "metadata"

    def __init__(self, parent, **kwargs):
        super(SearchThread, self).__init__(parent)
        self.galleries = kwargs.get("galleries") or self.parent.galleries
        self.force_search = kwargs.get("force_search", False)
        self.force_metadata = kwargs.get("force_metadata", False)
        self.signals = self.Signals()
        self.signals.progress.connect(self.parent.inc_progress)
        self.signals.end.connect(self.parent.get_metadata_done)

    class Signals(QtCore.QObject):
        end = QtCore.Signal()
        progress = QtCore.Signal(Decimal)

    def _run(self):
        self.search()

    def search(self):
        search_galleries = [g for g in self.galleries if
                            g.gid is None or self.force_search]
        self.logger.debug("Search galleries: %s" % [g.name
                                                    for g in search_galleries])
        try:
            self.inc_val = (Decimal(100.0) /
                            Decimal(len(search_galleries) +
                                    math.ceil(len(search_galleries) / 25)))
        except ZeroDivisionError:
            self.inc_val = 0
        need_metadata_galleries = []
        for gallery in search_galleries:
            search_results = Search.search_by_gallery(gallery)
            self.signals.progress.emit(self.inc_val)
            if search_results:
                gallery.id = Gallery.Gallery.process_ex_url(search_results)
            if gallery.gid:
                need_metadata_galleries.append(gallery)
            if len(need_metadata_galleries) == 3:
                self.get_metadata(need_metadata_galleries)
                need_metadata_galleries = []
        if need_metadata_galleries:
            self.get_metadata(need_metadata_galleries)
        galleries = [g for g in self.galleries if g.force_metadata]
        gallery_metalist = [galleries[i:i + self.API_MAX_ENTRIES]
                            for i in range(0, len(galleries),
                                           self.API_MAX_ENTRIES)]
        [self.get_metadata(g) for g in gallery_metalist]
        self.signals.end.emit()

    def get_metadata(self, galleries):
        assert len(galleries) <= self.API_MAX_ENTRIES
        payload = copy.deepcopy(self.BASE_REQUEST)
        payload["gidlist"] = [g.id for g in galleries]
        response = RequestManager.post(self.API_URL, payload=payload)
        self.signals.progress.emit(self.inc_val)
        for gallery in galleries:
            for metadata in response["gmetadata"]:
                id = [metadata["gid"], metadata["token"]]
                if id == gallery.id:
                    gallery.update_metadata({"gmetadata": metadata})
                    gallery.update_qgallery()
                    break
