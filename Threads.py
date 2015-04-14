#!/usr/bin/env python

from PySide import QtCore, QtGui
from Logger import Logger
import threading
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


class BaseThread(threading.Thread, Logger):
    id = None
    kill = False

    def __init__(self, parent, **kwargs):
        super(BaseThread, self).__init__()
        self.daemon = True
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
            return
        except:
            self.basesignals.exception.emit(self.id, sys.exc_info())


class GalleryThread(BaseThread):
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
        folder_galleries = []
        folder_gallery_candidates = []
        archive_galleries = []
        archive_gallery_candidates = []

        invalid_permissions = []
        invalid_files = []
        unsupported_files = []

        existing_paths = [g.path for g in self.parent.galleries]

        with Database.get_session(self) as session:
            db_galleries = session.query(Database.Gallery)
            db_gallery_list = [g for g in db_galleries]
            for db_gallery in db_gallery_list:
                if self.kill:
                    return
                if db_gallery.dead:
                    continue
                if db_gallery.path in existing_paths:
                    continue
                if not os.path.exists(db_gallery.path):
                    db_gallery.dead = True
                    session.add(db_gallery)
                    continue
                if db_gallery.type == Gallery.TypeMap.FolderGallery:
                    folder_gallery_candidates.append({"path": db_gallery.path,
                                                      "parent": self.parent.main_window,
                                                      "db_id": db_gallery.id})
                elif db_gallery.type == Gallery.TypeMap.ArchiveGallery:
                    archive_gallery_candidates.append({"path": db_gallery.path,
                                                       "parent": self.parent.main_window,
                                                       "db_id": db_gallery.id})
        paths = map(os.path.normpath, map(os.path.expanduser,
                                          self.parent.dirs))
        for path in paths:
            for base_folder, folders, files in scandir.walk(path):
                if self.kill:
                    return
                images = []
                for f in files:
                    ext = os.path.splitext(f)[-1].lower()
                    if ext in Gallery.IMAGE_EXTS:
                        images.append(os.path.join(base_folder, f))
                    elif ext in ArchiveGallery.ARCHIVE_EXTS:
                        archive_file = os.path.join(base_folder, f)
                        archive_gallery_candidates.append({"path": archive_file,
                                                           "parent": self.parent.main_window})
                if images:
                    folder_gallery_candidates.append({"path": base_folder,
                                                      "parent": self.parent.main_window,
                                                      "files": sorted(images, key=lambda f: f.lower())})
        gallery_candidates = folder_gallery_candidates + archive_gallery_candidates
        for gallery in gallery_candidates:
            if self.kill:
                return
            if gallery.get("path") in existing_paths:
                continue
            existing_paths.append(gallery.get("path"))
            try:
                if gallery in archive_gallery_candidates:
                    try:
                        gallery_obj = ArchiveGallery(**gallery)
                        archive_galleries.append(gallery_obj)
                    except IOError:
                        archive_galleries.remove(gallery_obj)
                        invalid_permissions.append(gallery.get("path"))
                    except zipfile.BadZipfile:
                        archive_galleries.remove(gallery_obj)
                        invalid_files.append(gallery.get("path"))
                    except NotImplementedError:
                        archive_galleries.remove(gallery_obj)
                        unsupported_files.append(gallery.get("path"))
                else:
                    folder_galleries.append(FolderGallery(**gallery))
            except AssertionError:
                pass
            except:
                exc = sys.exc_info()
                self.logger.error("%s gallery got unhandled exception" % gallery, exc_info=exc)
        self.signals.end.emit(folder_galleries + archive_galleries)
        if invalid_permissions or invalid_files or unsupported_files:
            raise Exceptions.InvalidZip(invalid_permissions, invalid_files, unsupported_files)


class ImageThread(BaseThread):
    IMAGE_WIDTH = 200
    EMIT_FREQ = 1
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
            if self.kill:
                return
            if not gallery.C_QGallery:
                gallery.load_thumbnail()
                send_galleries.append(gallery)
                self.signals.progress.emit(inc_val)
                if len(send_galleries) == self.EMIT_FREQ:
                    self.signals.gallery.emit(send_galleries)
                    send_galleries = []
        if send_galleries:
            self.signals.gallery.emit(send_galleries)


class SearchThread(BaseThread):
    API_URL = "http://exhentai.org/api.php"
    BASE_REQUEST = {"method": "gdata", "gidlist": []}
    API_MAX_ENTRIES = 25
    id = "metadata"
    inc_val = 0

    def __init__(self, parent, **kwargs):
        super(SearchThread, self).__init__(parent)
        self.galleries = kwargs.get("galleries") or self.parent.galleries
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
            if self.kill:
                return
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
                            for i in range(0, len(galleries), self.API_MAX_ENTRIES)]
        [self.get_metadata(g) for g in gallery_metalist]
        self.signals.end.emit()

    def get_metadata(self, galleries):
        assert len(galleries) <= self.API_MAX_ENTRIES
        payload = copy.deepcopy(self.BASE_REQUEST)
        payload["gidlist"] = [g.id for g in galleries]
        response = RequestManager.post(self.API_URL, payload=payload)
        self.signals.progress.emit(self.inc_val)
        for gallery in galleries:
            if self.kill:
                return
            for metadata in response["gmetadata"]:
                id = [metadata["gid"], metadata["token"]]
                if id == gallery.id:
                    gallery.update_metadata({"gmetadata": metadata})
                    gallery.update_qgallery()
                    break
