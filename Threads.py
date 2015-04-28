#!/usr/bin/env python

from PySide import QtCore, QtGui
from Logger import Logger
import threading
import Queue
import weakref
import copy
import scandir
import os
import zipfile
import sys
import math
from decimal import Decimal
from Gallery import Gallery, FolderGallery, ArchiveGallery
import Exceptions
import Database
from RequestManager import RequestManager
from Search import Search


Lock = threading.Lock()
class BaseThread(threading.Thread, Logger):
    id = None
    dead = False

    def __init__(self, parent, **kwargs):
        super(BaseThread, self).__init__()
        self.daemon = True
        self.queue = Queue.Queue()
        self.parent = parent
        self.basesignals = self.BaseSignals()
        self.basesignals.exception.connect(self.parent.thread_exception_handler)

    class BaseSignals(QtCore.QObject):
        exception = QtCore.Signal(str, tuple)

    @property
    def parent(self):
        return self._parent()

    @parent.setter
    def parent(self, val):
        self._parent = weakref.ref(val)

    def _run(self):
        raise NotImplementedError

    def run(self):
        while True:
            restart = False
            try:
                self._run()
            except (KeyboardInterrupt, SystemExit):
                return
            except:
                exc_info = sys.exc_info()
                extype = exc_info[0]
                exvalue = exc_info[1]
                if issubclass(extype, Exceptions.BaseException):
                    restart = exvalue.thread_restart
                self.basesignals.exception.emit(self, exc_info)
                if restart:
                    try:
                        while True:
                            self.queue.get(False)
                    except Queue.Empty:
                        pass




class GalleryThread(BaseThread):
    id = "gallery"

    def __init__(self, parent, **kwargs):
        super(GalleryThread, self).__init__(parent)
        self.signals = self.Signals()
        self.signals.end.connect(self.parent.find_galleries_done)
        self.existing_paths = [g.path for g in self.parent.galleries]
        self.loaded = False

    class Signals(QtCore.QObject):
        end = QtCore.Signal(list)

    def _run(self):
        while True:
            self.queue.get()
            if not self.loaded:
                self.load_from_db()
            else:
                self.find_galleries()

    def load_from_db(self):
        candidates = {"folder": [], "archive": []}
        with Database.get_session(self) as session:
            db_galleries = session.query(Database.Gallery)
            db_gallery_list = [g for g in db_galleries]
            for db_gallery in db_gallery_list:
                if db_gallery.dead:
                    continue
                if db_gallery.path in self.existing_paths:
                    continue
                if not os.path.exists(db_gallery.path):
                    db_gallery.dead = True
                    session.add(db_gallery)
                    continue
                candidate = {"path": db_gallery.path,
                             "parent": self.parent.main_window,
                             "db_id": db_gallery.id,
                             "db_obj": db_gallery,
                             "loaded": True}
                if db_gallery.type == Gallery.TypeMap.FolderGallery:
                    candidates["folder"].append(candidate)
                elif db_gallery.type == Gallery.TypeMap.ArchiveGallery:
                    candidates["archive"].append(candidate)
            self.create_from_dict(candidates)
        self.loaded = True

    def find_galleries(self):
        candidates = {"folder": [], "archive": []}
        paths = map(os.path.normpath, map(os.path.expanduser,
                                          self.parent.dirs))
        for path in paths:
            for base_folder, folders, files in scandir.walk(path):
                images = []
                for f in files:
                    ext = os.path.splitext(f)[-1].lower()
                    if ext in Gallery.IMAGE_EXTS:
                        images.append(os.path.join(base_folder, f))
                    elif ext in ArchiveGallery.ARCHIVE_EXTS:
                        archive_file = os.path.join(base_folder, f)
                        candidates["archive"].append({"path": archive_file,
                                                      "parent": self.parent.main_window})
                if images:
                    candidates["folder"].append({"path": base_folder,
                                                 "parent": self.parent.main_window,
                                                 "files": sorted(images, key=lambda f: f.lower())})
        self.create_from_dict(candidates)

    def create_from_dict(self, candidates):
        invalid_permissions = []
        invalid_files = []
        unsupported_files = []
        gallery_candidates = []
        galleries = []
        gallery_candidates += candidates["folder"]
        gallery_candidates += candidates["archive"]
        for gallery in gallery_candidates:
            if gallery.get("path") in self.existing_paths:
                continue
            self.existing_paths.append(gallery.get("path"))
            gallery_obj = None
            try:
                if gallery in candidates["archive"]:
                    try:
                        gallery_obj = ArchiveGallery(**gallery)
                        galleries.append(gallery_obj)
                    except IOError:
                        galleries.remove(gallery_obj)
                        gallery_obj = None
                        invalid_permissions.append(gallery.get("path"))
                    except zipfile.BadZipfile:
                        galleries.remove(gallery_obj)
                        gallery_obj = None
                        invalid_files.append(gallery.get("path"))
                    except NotImplementedError:
                        galleries.remove(gallery_obj)
                        gallery_obj = None
                        unsupported_files.append(gallery.get("path"))
                else:
                    gallery_obj = FolderGallery(**gallery)
                    galleries.append(gallery_obj)
            except AssertionError:
                gallery_obj = None
                pass
            except:
                gallery_obj = None
                exc = sys.exc_info()
                self.logger.error("%s gallery got unhandled exception" % gallery, exc_info=exc)
            if gallery.get("loaded", False):
                if gallery_obj:
                    gallery_obj.load_from_db_object(gallery.get("db_obj"))
                else:
                    with Database.get_session(self) as session:
                        db_id = gallery.get("db_id")
                        db_gallery = session.query(Database.Gallery).filter(Database.Gallery.id == db_id)[0]
                        db_gallery.dead = True
                        session.add(db_gallery)
        self.signals.end.emit(galleries)
        if invalid_permissions or invalid_files or unsupported_files:
            raise Exceptions.InvalidZip(invalid_permissions, invalid_files, unsupported_files)



class ImageThread(BaseThread):
    EMIT_FREQ = 5
    id = "image"

    def __init__(self, parent, **kwargs):
        super(ImageThread, self).__init__(parent)
        self.signals = self.Signals()
        self.signals.progress.connect(self.parent.inc_progress)
        self.signals.gallery.connect(self.parent.image_generated)
        self.signals.end.connect(self.parent.image_thread_done)

    class Signals(QtCore.QObject):
        progress = QtCore.Signal(Decimal)
        gallery = QtCore.Signal(list)
        end = QtCore.Signal()

    def _run(self):
        while True:
            galleries = self.queue.get()
            self.generate_images(galleries)
            self.signals.end.emit()

    def generate_images(self, galleries):
        try:
            inc_val = Decimal(100.0) / Decimal(len(galleries))
        except ZeroDivisionError:
            return
        send_galleries = []
        for gallery in galleries:
            if not gallery.image:
                try:
                    gallery.load_thumbnail()
                    send_galleries.append(gallery)
                except:
                    exc = sys.exc_info()
                    self.logger.error("%s gallery failed to get image" % gallery, exc_info=exc)
                self.signals.progress.emit(inc_val)
                if len(send_galleries) == self.EMIT_FREQ:
                    self.signals.gallery.emit(send_galleries)
                    send_galleries = []
        if send_galleries:
            self.signals.gallery.emit(send_galleries)
        with Database.get_session(self) as session:
            dead_galleries = session.query(Database.Gallery).filter(Database.Gallery.dead == True)
            for gallery in dead_galleries:
                try:
                    os.remove(dead_galleries.thumbnail_path)
                except OSError:
                    pass


class SearchThread(BaseThread):
    API_URL = "http://exhentai.org/api.php"
    BASE_REQUEST = {"method": "gdata", "gidlist": []}
    API_MAX_ENTRIES = 25
    id = "metadata"
    inc_val = 0

    def __init__(self, parent, **kwargs):
        super(SearchThread, self).__init__(parent)
        self.signals = self.Signals()
        self.signals.progress.connect(self.parent.inc_progress)
        self.signals.end.connect(self.parent.get_metadata_done)

    class Signals(QtCore.QObject):
        end = QtCore.Signal()
        progress = QtCore.Signal(Decimal)

    def _run(self):
        while True:
            galleries = self.queue.get()
            self.search(galleries)

    def search(self, galleries):
        search_galleries = [g for g in galleries if
                            g.gid is None]
        self.logger.debug("Search galleries: %s" % [g.name for g in search_galleries])
        try:
            self.inc_val = (Decimal(100.0) /
                            Decimal(len(search_galleries) +
                                    math.ceil(len(search_galleries) / 25)))
        except ZeroDivisionError:
            pass
        need_metadata_galleries = []
        for gallery in search_galleries:
            search_results = Search.search_by_gallery(gallery)
            self.signals.progress.emit(self.inc_val)
            if search_results:
                gallery.id = Gallery.process_ex_url(search_results)
            if gallery.gid:
                need_metadata_galleries.append(gallery)
            if len(need_metadata_galleries) == 3:
                self.get_metadata(need_metadata_galleries)
                need_metadata_galleries = []
        if need_metadata_galleries:
            self.get_metadata(need_metadata_galleries)
        force_galleries = [g for g in galleries if g.force_metadata]
        force_gallery_metalist = [force_galleries[i:i + self.API_MAX_ENTRIES]
                                  for i in range(0, len(galleries), self.API_MAX_ENTRIES)]
        [self.get_metadata(g) for g in force_gallery_metalist]
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
