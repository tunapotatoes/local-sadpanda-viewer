#!/usr/bin/env python

from PySide import QtCore, QtGui
from Logger import Logger
import threading
import weakref
import copy
from decimal import Decimal
from Gallery import Gallery
from RequestManager import RequestManager
from Processes import Processes
from multiprocessing import Process, Queue
from Search import Search
import math


class BaseThread(threading.Thread, Logger):
    def __init__(self, parent, **kwargs):
        super(BaseThread, self).__init__()
        self._parent = weakref.ref(parent)

    @property
    def parent(self):
        return self._parent()


class GalleryThread(BaseThread):
    IMAGE_WIDTH = 200

    def __init__(self, parent, **kwargs):
        super(GalleryThread, self).__init__(parent)
        self.signals = self.Signals()
        self.signals.end.connect(self.parent.find_galleries_done)
        self.signals.progress.connect(self.parent.inc_progress)
        self.signals.gallery.connect(self.parent.add_galleries)

    class Signals(QtCore.QObject):
        gallery = QtCore.Signal(list)
        progress = QtCore.Signal(Decimal)
        end = QtCore.Signal()

    def run(self):
        queue = Queue()
        process = Process(target=Processes.find_dirs,
                          args=(queue, self.parent.dirs))
        process.start()
        results = queue.get()
        process.join()
        existing_paths = [g.path for g in self.parent.galleries]
        galleries = [Gallery(self.parent.main_window, r[0], r[1])
                     for r in results if r[0] not in existing_paths]
        try:
            inc_val = Decimal(100.0) / Decimal(len(galleries))
        except ZeroDivisionError:
            self.signals.end.emit()
            return
        for gallery in galleries:
            gallery.image = QtGui.QImage(gallery.files[0]).scaledToWidth(
                self.IMAGE_WIDTH, QtCore.Qt.SmoothTransformation)
            self.signals.gallery.emit([gallery])
            self.signals.progress.emit(inc_val)
        self.signals.end.emit()


class SearchThread(BaseThread):
    API_URL = "http://exhentai.org/api.php"
    BASE_REQUEST = {"method": "gdata", "gidlist": []}
    API_MAX_ENTRIES = 25

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

    def run(self):
        search_galleries = [g for g in self.galleries if
                            g.gid is None or self.force_search]
        self.logger.debug("Search galleries: %s" % search_galleries)
        try:
            inc_val = (Decimal(100.0) /
                       Decimal(len(search_galleries) +
                               math.ceil(len(search_galleries) / 25)))
        except ZeroDivisionError:
            inc_val = 0
            pass
        for gallery in search_galleries:
            search_results = Search.search_by_gallery(gallery)
            self.signals.progress.emit(inc_val)
            if search_results is not None:
                gallery.id = Gallery.process_ex_url(search_results)

        galleries = [g for g in self.galleries if
                     g.gid is not None or self.force_metadata]

        gallery_metalist = [galleries[i:i + self.API_MAX_ENTRIES]
                            for i in range(0, len(galleries),
                                           self.API_MAX_ENTRIES)]
        for gallery_list in gallery_metalist:
            payload = copy.deepcopy(self.BASE_REQUEST)
            [payload["gidlist"].append(g.id) for g in gallery_list]
            response = RequestManager.post(self.API_URL, payload=payload)
            self.signals.progress.emit(inc_val)
            for gallery in gallery_list:
                for metadata in response["gmetadata"]:
                    id = [metadata["gid"], metadata["token"]]
                    if id == gallery.id:
                        gallery.update_metadata({"gmetadata": metadata})
                        break
        self.signals.end.emit()
