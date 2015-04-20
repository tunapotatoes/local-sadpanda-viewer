#!/usr/bin/env python
import os
import hashlib
import io
import json
import re
import uuid
import shutil
import Windows
import Exceptions
import zipfile
import tempfile
import Database
import sys
import contextlib
import scandir
from Boilerplate import GalleryBoilerplate
from ui.gallery import C_QGallery
from PySide import QtGui, QtCore
from time import time
from datetime import datetime

class Gallery(GalleryBoilerplate):
    IMAGE_EXTS = [".png", ".jpg", ".jpeg"]
    HASH_SIZE = 8192
    IMAGE_WIDTH = 200
    BASE_EX_URL = "http://exhentai.org/g/%s/%s/"
    DB_ID_FILENAME = ".dbid"
    thumbnail_path = None
    image_hash = None
    metadata = None
    C_QGallery = None
    metadata_file = None
    force_metadata = False
    customize_window = None
    image = None
    db_id = None
    db_uuid = None
    name = None
    read_count = 0
    last_read = None
    files = None

    class TypeMap(object):
        FolderGallery = 0
        ArchiveGallery = 1

    def __repr__(self):
        return self.name

    def __init__(self, **kwargs):
        self.metadata = {}
        self.old_metadata = {}
        try:
            self.old_metadata = self.load_old_metadata()
        except:
            exc = sys.exc_info()
            self.logger.warning("Failed to load old metadata.", exc_info=exc)
        self.parent = kwargs.get("parent")
        self.db_file = os.path.join(self.path, self.DB_ID_FILENAME)
        self.db_id = kwargs.get("db_id") or self.find_in_db()
        self.load_metadata()
        self.update_metadata(self.old_metadata)

    def __del__(self):
        self.C_QGallery = None

    @property
    def true_name(self):
        name = self.title
        pairs = [("{", "}"), ("(", ")"), ("[", "]")]
        regex = ur"\s*\%s[^%s]*\%s"
        for pair in pairs:
            name = re.sub(regex % (pair[0], pair[0], pair[1]), "",  name)
        return name.lstrip()

    def set_rating(self, rating):
        self.crating = str(rating)
        self.save_metadata()


    def customize(self):
        self.customize_window = Windows.CustomizeWindow(self.parent, self)
        self.customize_window.tags = ", ".join(self.ctags)
        self.customize_window.title = self.ctitle
        if self.gid:
            self.customize_window.url = self.generate_ex_url()
        self.customize_window.rating = self.crating

    def save_customization(self):
        self.ctags = list(filter(None, map(lambda x: re.sub("^\s+", "", x),
                                           self.customize_window.tags.split(","))))
        self.ctitle = self.customize_window.title
        self.crating = self.customize_window.rating
        if self.customize_window.url:
            old_id = self.id
            try:
                self.id = Gallery.process_ex_url(self.customize_window.url)
            except:
                raise Exceptions.InvalidExUrl()
            if self.id != old_id:
                self.force_metadata = True
                self.get_metadata()
        self.customize_window.close()
        self.customize_window = None
        self.parent.app.setup_tags()
        self.save_metadata()
        self.update_qgallery()

    def find_in_db(self):
        db_id = None
        if os.path.exists(self.db_file):
            try:
                db_id = self.load_db_file()
            except:
                self.logger.warning("DB UUID file invalid.")
                self.delete_db_file()
        # Todo - Implement searching locally
        # if not db_id:
        #     with Database.get_session(self) as session:
        #         dead_galleries = session.query(Database.Gallery).filter(Database.Gallery.dead == True)

        if not db_id:
            with Database.get_session(self) as session:
                db_gallery = Database.Gallery()
                if isinstance(self, ArchiveGallery):
                    db_gallery.type = self.TypeMap.ArchiveGallery
                    db_gallery.path = self.archive_file
                else:
                    db_gallery.type = self.TypeMap.FolderGallery
                    db_gallery.path = self.path
                self.db_uuid = str(uuid.uuid1())
                db_gallery.uuid = self.db_uuid
                session.add(db_gallery)
                session.commit()
                db_id = db_gallery.id
                self.db_id = db_id
                self.save_db_file()
        return db_id

    def load_metadata(self):
        with Database.get_session(self) as session:
            db_gallery = session.query(Database.Gallery).filter(Database.Gallery.id == self.db_id)
            assert db_gallery.count() == 1
            db_gallery = db_gallery[0]
            self.thumbnail_path = db_gallery.thumbnail_path
            self.image_hash = db_gallery.image_hash
            self.db_uuid = db_gallery.uuid
            self.read_count = db_gallery.read_count
            self.last_read = db_gallery.last_read
            if isinstance(self, ArchiveGallery):
                self.archive_file = db_gallery.path
                self.path = os.path.dirname(self.archive_file)
            else:
                self.path = db_gallery.path
            for metadata in db_gallery.metadata_collection.all():
                self.metadata[metadata.name] = json.loads(metadata.json)

    def update_metadata(self, new_metadata):
        self.metadata.update(new_metadata)
        self.force_metadata = False
        self.save_metadata()

    def save_metadata(self):
        self.logger.info("Saving gallery metadata")
        self.metadata = self.clean_metadata(self.metadata)
        self.save_db_file()
        with Database.get_session(self) as session:
            db_gallery = session.query(Database.Gallery).filter(Database.Gallery.id == self.db_id)[0]
            db_metadata_list = db_gallery.metadata_collection.all()
            for name in self.metadata:
                db_metadata = next((m for m in db_metadata_list if m.name == name), None)
                if not db_metadata:
                    self.logger.debug("Creating new metadata table %s" % name)
                    db_metadata = Database.Metadata()
                    db_metadata.gallery = db_gallery
                    db_gallery.metadata_collection.append(db_metadata)
                    session.add(db_metadata)
                    session.add(db_gallery)
                db_metadata.name = name
                db_metadata.json = unicode(json.dumps(self.metadata[name], ensure_ascii=False).encode("utf8"))
                session.commit()  # Have to run this on each iteration in case a new metadata table was created
            db_gallery.thumbnail_path = self.thumbnail_path
            db_gallery.image_hash = self.image_hash
            db_gallery.read_count = self.read_count
            db_gallery.last_read = self.last_read
            if isinstance(self, ArchiveGallery):
                db_gallery.path = self.archive_file
            else:
                db_gallery.path = self.path
            session.add(db_gallery)

    def save_db_file(self):
        self.logger.debug("Saving DB UUID file.")
        try:
            db_file = open(self.db_file, "r+b")
        except IOError:
            db_file = open(self.db_file, "wb")
        try:
            db_file.write(self.db_uuid)
            db_file.truncate()
        finally:
            db_file.close()

    def delete_db_file(self):
        raise NotImplementedError

    def load_db_file(self):
        self.logger.debug("Loading DB UUID file.")
        db_file = open(self.db_file, "rb")
        db_uuid = str(db_file.read())
        self.logger.info("DB UUID loaded from file: %s" % db_uuid)
        db_file.close()
        db_id = self.validate_db_uuid(db_uuid)
        return db_id

    def validate_db_uuid(self, db_uuid):
        assert uuid.UUID(db_uuid)
        db_id = None
        with Database.get_session(self) as session:
            db_gallery = session.query(Database.Gallery).filter(Database.Gallery.uuid == db_uuid, Database.Gallery.dead == True)
            assert db_gallery.count() == 1
            db_gallery[0].dead = False
            session.add(db_gallery[0])
            db_id = db_gallery[0].id
        return db_id

    def generate_hash(self, source):
        sha1 = hashlib.sha1()
        buff = source.read(self.HASH_SIZE)
        while len(buff) > 0:
            sha1.update(buff)
            buff = source.read(self.HASH_SIZE)
        return sha1.hexdigest()

    def update_qgallery(self):
        if self.C_QGallery:
            self.C_QGallery.update()

    def clean_metadata(self, metadata):
        if isinstance(metadata, dict):
            metadata = {key: self.clean_metadata(metadata[key])
                        for key in metadata}
        elif isinstance(metadata, list):
            metadata = [self.clean_metadata(val) for val in metadata]
        elif isinstance(metadata, unicode):
            metadata = re.sub("&#039;", "'", metadata)
            metadata = re.sub("&quot;", "\"", metadata)
            metadata = re.sub("(&amp;)", "&", metadata)
            #metadata = re.sub("&#(\d+)(;|(?=\s))", "", metadata)
        return metadata

    def generate_ex_url(self):
        return self.BASE_EX_URL % (self.gid, self.token)

    @classmethod
    def process_ex_url(cls, url):
        split_url = url.split("/")
        if split_url[-1]:
            return int(split_url[-2]), split_url[-1]
        else:
            return int(split_url[-3]), split_url[-2]

    def load_old_metadata(self):
        raise NotImplementedError

    def get_image(self):
        raise NotImplementedError

    def generate_image_hash(self):
        raise NotImplementedError

    def resize_image(self):
        return self.get_image().scaledToWidth(self.IMAGE_WIDTH,
                                              QtCore.Qt.SmoothTransformation)

    def verify_hash(self):
        image_hash = self.generate_image_hash()
        if self.image_hash != image_hash:
            try:
                os.remove(self.thumbnail_path)
            except OSError:
                pass
            return False
        return True

    def load_thumbnail(self):
        if not self.thumbnail_path or not os.path.exists(self.thumbnail_path) or not self.verify_hash():
            self.thumbnail_path = os.path.join(self.parent.app.THUMB_DIR, str(uuid.uuid1()))
            self.image = self.resize_image()
            self.logger.debug("Saving new thumbnail")
            assert self.image.save(self.thumbnail_path, "JPG")
            self.image_hash = self.generate_image_hash()
            self.save_metadata()
        else:
            self.image = QtGui.QImage(self.thumbnail_path)

    def open_file(self):
        self.read_count += 1
        self.last_read = int(time())
        self.save_metadata()
        self.update_qgallery()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.files[0]))

    def open_on_ex(self):
        QtGui.QDesktopServices.openUrl(self.generate_ex_url())

    def open_folder(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.path))

    def get_metadata(self):
        self.parent.app.get_metadata([self])

    @property
    def local_last_read_time(self):
        if self.last_read:
            return datetime.fromtimestamp(self.last_read).strftime("%Y-%m-%d")



class FolderGallery(Gallery):
    def __init__(self, **kwargs):
        self.path = os.path.normpath(kwargs.get("path"))
        self.name = os.path.normpath(self.path).split(os.sep)[-1]
        self.metadata_file = os.path.join(self.path, ".metadata.json")
        super(FolderGallery, self).__init__(**kwargs)
        files = kwargs.get("files") or self.find_files()
        assert len(files) > 0
        self.files = list(map(os.path.normpath, files))

    def get_image(self):
        image = QtGui.QImageReader()
        image.setDecideFormatFromContent(True)
        image.setFileName(self.files[0])
        image = image.read()
        assert image.width()
        return image

    def generate_image_hash(self):
        with open(self.files[0], "rb") as image:
            return self.generate_hash(image)

    def find_files(self):
        found_files = []
        for base_folder, folders, files in scandir.walk(self.path):
            for f in files:
                ext = os.path.splitext(f)[-1].lower()
                if ext in self.IMAGE_EXTS:
                    found_files.append(os.path.join(base_folder, f))
            break
        return found_files

    def delete_db_file(self):
        os.remove(self.db_file)

    def load_old_metadata(self):
        metadata = {}
        if os.path.exists(self.metadata_file):
            with io.open(self.metadata_file, "r", encoding="utf-8") as metadata_file:
                try:
                    metadata = json.load(metadata_file)
                except ValueError as e:
                    e = str(e)
                    if "Extra data:" in e:
                        column = int(re.search(r"column\s(\d+)", e).groups()[0])
                        metadata.seek(0)
                        metadata = json.loads(metadata.read()[:column - 1])
        return metadata


class ArchiveGallery(Gallery):
    ARCHIVE_EXTS = [".zip"]
    DB_ID_KEY = "lsv-db_id"

    def __init__(self, **kwargs):
        self.archive_file = os.path.normpath(kwargs.get("path"))
        self.path = os.path.dirname(self.archive_file)
        self.name, self.archive_type = os.path.splitext(os.path.basename(self.archive_file))
        with self.archive("a") as archive:
            archive.testzip()
            archive.comment = ""
        super(ArchiveGallery, self).__init__(**kwargs)
        self.raw_files = self.find_files()
        assert len(self.raw_files) > 0
        self.temp_dir = os.path.normpath(tempfile.mkdtemp())

    def get_image(self):
        image = QtGui.QImage()
        assert image.loadFromData(self.raw_image.read())
        return image

    @contextlib.contextmanager
    def archive(self, mode):
        assert mode is not "w"   # Extremely dangerous
        archive = None
        try:
            archive = zipfile.ZipFile(self.archive_file, mode)
            yield archive
        finally:
            archive.close()

    def __del__(self):
        super(ArchiveGallery, self).__del__()
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def extract(self):
        with self.archive("r") as archive:
            archive.extractall(self.temp_dir)

    @property
    def raw_image(self):
        with self.archive("r") as archive:
            return archive.open(self.raw_files[0])

    @property
    def files(self):
        if not os.path.exists(os.path.join(self.temp_dir, self.raw_files[0])):
            self.extract()
        return list(map(lambda f: os.path.normpath(os.path.join(
            self.temp_dir, f)), self.raw_files))

    def find_files(self):
        raw_files = []
        with self.archive("r") as archive:
            for f in archive.namelist():
                # Really shouldn't be duplicating this code but it's late and I'm tired
                ext = os.path.splitext(f)[-1].lower()
                if ext in self.IMAGE_EXTS:
                    raw_files.append(f)
        return sorted(raw_files, key=lambda f: f.lower())

    def save_db_file(self):
        self.logger.debug("Saving DB UUID")
        with self.archive("a") as archive:
            db_json = {self.DB_ID_KEY: self.db_uuid}
            archive.comment = json.dumps(db_json, ensure_ascii=False).encode("utf-8")

    def delete_db_file(self):
        self.logger.debug("Deleting DB UUID")
        with self.archive("a") as archive:
            archive.comment = json.dumps({}, ensure_ascii=False).encode("utf-8")

    def load_db_file(self):
        self.logger.debug("Loading DB UUID")
        with self.archive("r") as archive:
            db_json = json.loads(archive.comment.decode("utf-8")) or {}
            self.db_uuid = db_json.get(self.DB_ID_KEY)
            db_id = self.validate_db_uuid(self.db_uuid)
            return db_id

    def load_old_metadata(self):
        with self.archive("r") as archive:
            old_metadata = json.loads(archive.comment.decode("utf-8")) or {}
            old_metadata.pop(self.DB_ID_KEY, None)
            return old_metadata

    def generate_image_hash(self):
        return self.generate_hash(self.raw_image)

    def generate_archive_hash(self):
        with open(self.archive, "rb") as archive:
            return self.generate_hash(archive)

