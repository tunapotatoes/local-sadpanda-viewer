#!/usr/bin/python2
from PySide import QtCore, QtGui
from decimal import Decimal
import copy
import threading
import Gallery


class ImageThread(threading.Thread):
    """
    Seperated this functionality because creating this many image thumbnails is
    expensive and would freeze the main thread for a few seconds.
    """
    def __init__(self, parent, **kwargs):
        super(ImageThread, self).__init__()
        self.parent = parent
        self.signals = ImageThread.Signals()
        self.signals.image_signal.connect(self.parent.add_gallery_image)
        self.signals.progress_signal.connect(self.parent.inc_progress)
        self.signals.end_signal.connect(self.parent.image_thread_done)

    def run(self):
        self.create_images()
        self.signals.end_signal.emit()

    class Signals(QtCore.QObject):
        image_signal = QtCore.Signal(Gallery.LocalGallery, QtGui.QImage)
        progress_signal = QtCore.Signal(Decimal)
        end_signal = QtCore.Signal()

        def __init__(self):
            super(ImageThread.Signals, self).__init__()

    def create_images(self):
        try:
            inc_val = Decimal(1.0) / Decimal(len(self.parent.galleries))
        except ZeroDivisionError:
            pass
        for gallery in self.parent.galleries:
            if gallery.has_metadata():
                image = QtGui.QImage(gallery.files[0]).scaledToWidth(
                    self.parent.config["image_width"],
                    QtCore.Qt.SmoothTransformation)
                self.signals.image_signal.emit(gallery, image)
            self.signals.progress_signal.emit(inc_val)


class RestThread(threading.Thread):
    def __init__(self, parent, **kwargs):
        super(RestThread, self).__init__()
        self.parent = parent
        self.kwargs = kwargs
        self.signals = self.Signals()
        self.signals.end_signal.connect(self.parent.rest_thread_done)
        self.signals.progress_signal.connect(self.parent.inc_progress)
        image_thread = self.parent.threads.get("it", None)
        while image_thread is not None and image_thread.isAlive():
            continue
        force = self.kwargs.get("force", False)
        self.temp_galleries = [g for g in self.parent.galleries if
                               not g.has_metadata() or force]

    def run(self):
        self._find_galleries(self.temp_galleries, **self.kwargs)
        self.signals.end_signal.emit()

    class Signals(QtCore.QObject):
        end_signal = QtCore.Signal()
        progress_signal = QtCore.Signal(Decimal)


        def __init__(self):
            super(RestThread.Signals, self).__init__()

    def _find_galleries(self, galleries, **kwargs):
        finished_galleries = []
        # This is a very rough estimate.
        inc_val = Decimal(1.0) / Decimal(len(galleries))
        for gallery in galleries:
            gallery.search()
            if gallery.WebGallery is not None:
                finished_galleries.append(gallery)
            self.signals.progress_signal.emit(inc_val)
            if len(finished_galleries) == self.parent.config[
                    "API_MAX_ENTRIES"]:
                self._get_metadata(finished_galleries)
                finished_galleries = []
        self._get_metadata(finished_galleries)
                

    def _get_metadata(self, galleries, **kwargs):
        if len(galleries) == 0:
            return
        data = copy.deepcopy(self.parent.config["base_request"])
        for gallery in galleries[:self.parent.config["API_MAX_ENTRIES"]]:
            data["gidlist"].append(gallery.WebGallery.gid)
        if len(data["gidlist"]) == 0:
            return
        request = self.parent.request_object.request(
            self.parent.config["API_URL"], "post", data)
        for gallery in galleries[:self.parent.config["API_MAX_ENTRIES"]]:
            for metadata in request.json()["gmetadata"]:
                if gallery.WebGallery.validate_data(metadata):
                    gallery.save_metadata(metadata)
                    break
        self._get_metadata(galleries[self.parent.config["API_MAX_ENTRIES"]:],
                           **kwargs)
