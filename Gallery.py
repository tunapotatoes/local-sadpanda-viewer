#!/usr/bin/env python
import os
import hashlib
import io
import json
import re
import shutil
import Windows
import Exceptions
from Logger import Logger
import weakref
import zipfile
import tempfile
import contextlib


class Gallery(Logger):
    IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webm"]
    HASH_SIZE = 8192
    BASE_EX_URL = "http://exhentai.org/g/%s/%s/"
    BUTTONS = ["editButton", "openButton"]

    def __init__(self, parent):
        self.parent = parent
        self.metadata = {}
        self.C_QGallery = None
        self.force_metadata = False

    @property
    def parent(self):
        return self._parent()

    @parent.setter
    def parent(self, val):
        self._parent = weakref.ref(val)

    def __del__(self):
        self.C_QGallery = None

    @property
    def title(self):
        return self.ctitle or self.extitle or self.name

    @property
    def ctitle(self):
        return self.metadata.get("cmetadata", {}).get("title", "")

    @ctitle.setter
    def ctitle(self, val):
        self.metadata["cmetadata"] = self.metadata.get("cmetadata", {})
        self.metadata["cmetadata"]["title"] = val

    @property
    def extitle(self):
        return self.metadata.get("gmetadata", {}).get("title", "")

    @extitle.setter
    def extitle(self, val):
        self.metadata["gmetadata"] = self.metadata.get("gmetadata", {})
        self.metadata["gmetadata"]["title"] = val

    @property
    def extags(self):
        return self.metadata.get("gmetadata", {}).get("tags", [])

    @extags.setter
    def extags(self, val):
        self.metadata["gmetadata"] = self.metadata.get("gmetadata", {})
        self.metadata["gmetadata"]["tags"] = val

    @property
    def ctags(self):
        return self.metadata.get("cmetadata", {}).get("tags", [])

    @ctags.setter
    def ctags(self, val):
        self.metadata["cmetadata"] = self.metadata.get("cmetadata", {})
        self.metadata["cmetadata"]["tags"] = val

    @property
    def tags(self):
        return self.extags + self.ctags

    @property
    def rating(self):
        return self.crating or self.exrating

    @property
    def crating(self):
        return self.metadata.get("cmetadata", {}).get("rating")

    @crating.setter
    def crating(self, val):
        self.metadata["cmetadata"] = self.metadata.get("cmetadata", {})
        self.metadata["cmetadata"]["rating"] = val

    @property
    def exrating(self):
        return self.metadata.get("gmetadata", {}).get("rating")

    @exrating.setter
    def exrating(self, val):
        self.metadata["gmetadata"] = self.metadata.get("gmetadata", {})
        self.metadata["gmetadata"]["rating"] = val

    @property
    def gid(self):
        return self.metadata.get("gmetadata", {}).get("gid")

    @gid.setter
    def gid(self, val):
        self.metadata["gmetadata"] = self.metadata.get("gmetadata", {})
        self.metadata["gmetadata"]["gid"] = val

    @property
    def token(self):
        return self.metadata.get("gmetadata", {}).get("token")

    @token.setter
    def token(self, val):
        self.metadata["gmetadata"] = self.metadata.get("gmetadata", {})
        self.metadata["gmetadata"]["token"] = val

    @property
    def id(self):
        return [self.gid, self.token]

    @id.setter
    def id(self, val):
        self.gid = val[0]
        self.token = val[1]

    def set_button_status(self, button, status):
        try:
            getattr(getattr(self.C_QGallery, button), "setEnabled")(status)
        except AttributeError:
            pass

    def disable_buttons(self, buttons):
        [self.set_button_status(b, False) for b in buttons]

    def enable_buttons(self, buttons):
        [self.set_button_status(b, True) for b in buttons]

    def disable_all_buttons(self):
        self.disable_buttons(self.BUTTONS)

    def enable_all_buttons(self):
        self.enable_buttons(self.BUTTONS)

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
            try:
                old_id = self.id
                self.id = Gallery.process_ex_url(self.customize_window.url)
                if self.id != old_id:
                    self.force_metadata = True
                    self.parent.app.get_metadata([self])
            except:
                raise Exceptions.InvalidExUrl()
        self.customize_window.close()
        self.customize_window = None
        self.update_qgallery()
        self.save_metadata()

    def load_metadata(self):
        metadata = io.open(self.metadata_file, "r", encoding="utf-8")
        self.metadata = json.load(metadata)

    def update_metadata(self, new_metadata):
        self.logger.debug("Update metadata with %s" % new_metadata)
        self.metadata.update(new_metadata)
        self.force_metadata = False
        self.save_metadata()

    def save_metadata(self):
        self.metadata = self.clean_metadata(self.metadata)
        metadata_file = open(self.metadata_file, "wb")
        metadata_file.write(json.dumps(self.metadata,
                                       ensure_ascii=False).encode("utf8"))
        metadata_file.close()

    def generate_image_hash(self, source):
        sha1 = hashlib.sha1()
        self.logger.debug("Generate sha1 for first image in folder.")
        buff = source.read(self.HASH_SIZE)
        while len(buff) > 0:
            sha1.update(buff)
            buff = source.read(self.HASH_SIZE)
        return sha1.hexdigest()

    def update_qgallery(self):
        if self.C_QGallery:
            self.C_QGallery.update()

    def clean_metadata(self, metadata):
        self.logger.debug("Cleaning metadata.\nInput data: %s" % metadata)
        if isinstance(metadata, dict):
            metadata = {key: self.clean_metadata(metadata[key])
                        for key in metadata}
        elif isinstance(metadata, list):
            metadata = [self.clean_metadata(val) for val in metadata]
        elif isinstance(metadata, str):
            metadata = re.sub("&#039;", "'", metadata)
            metadata = re.sub("&quot;", "\"", metadata)
            metadata = re.sub("(&amp;)", "&", metadata)
            #metadata = re.sub("&#(\d+)(;|(?=\s))", "", metadata)
        self.logger.debug("Output data: %s" % metadata)
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


class FolderGallery(Gallery):
    def __init__(self, parent, path, files):
        super(FolderGallery, self).__init__(parent)
        self.path = path
        self.name = os.path.normpath(self.path).split(os.sep)[-1]
        self.metadata_file = os.path.join(self.path, ".metadata.json")
        self.files = files
        if not os.path.exists(self.metadata_file):
            self.update_metadata({})
        else:
            self.load_metadata()
        self.save_metadata()
        self.load_metadata()

    def generate_image_hash(self):
        with open(self.files[0], "rb") as image:
            super(FolderGallery, self).generate_image_hash(image)


class ArchiveGallery(Gallery):

    def __init__(self, parent, archive):
        super(ArchiveGallery, self).__init__(parent)
        self.archive = archive
        self.name, self.archive_type = os.path.splitext(os.path.basename(self.archive))
        self.raw_files = self.find_files()
        self.temp_dir = tempfile.mkdtemp()
        try:
            self.load_metadata()
        except ValueError:
            self.update_metadata({})

    @property
    def path(self):
        return self.archive

    @contextlib.contextmanager
    def archive_file(self, mode):
        assert mode is not "w"   # Extremely dangerous
        if self.archive_type == ".zip":
            archive = zipfile.ZipFile(self.archive, mode)
        yield archive
        archive.close()

    def __del__(self):
        super(ArchiveGallery, self).__del__()
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def extract(self):
        with self.archive_file("r") as archive:
            archive.extractall(self.temp_dir)

    @property
    def raw_image(self):
        with self.archive_file("r") as archive:
            return archive.open(self.raw_files[0])

    @property
    def files(self):
        if not os.path.exists(os.path.join(self.temp_dir, self.raw_files[0])):
            self.extract()
        return list(map(lambda f: os.path.join(self.temp_dir, f), self.raw_files))

    def find_files(self):
        raw_files = []
        with self.archive_file("r") as archive:
            for f in archive.namelist():
                # Really shouldn't be duplicating this code but it's late and I'm tired
                ext = os.path.splitext(f)[-1].lower()
                if ext in self.IMAGE_EXTS:
                    raw_files.append(f)
        return sorted(raw_files, key=lambda f: f.lower())

    def load_metadata(self):
        with self.archive_file("r") as archive:
            self.metadata = json.loads(archive.comment.decode("utf-8"))

    def save_metadata(self):
        with self.archive_file("a") as archive:
            archive.comment = json.dumps(self.metadata).encode("utf-8")

    def generate_image_hash(self):
        super(ArchiveGallery, self).generate_image_hash(self.raw_image)
