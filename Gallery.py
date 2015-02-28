#!/usr/bin/env python
import os
import hashlib
import io
import json
import re
import Windows
import Exceptions
from Logger import Logger
import weakref


class Gallery(Logger):
    IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webm"]
    HASH_SIZE = 8192
    BASE_EX_URL = "http://exhentai.org/g/%s/%s/"
    BUTTONS = ["editButton", "openButton"]

    def __init__(self, parent, folder_path, files):
        self._parent = weakref.ref(parent)
        self.metadata = {}
        self.C_QGallery = None
        self.force_metadata = False
        self.path = os.path.join(folder_path)
        self.files = files
        #self.files = Gallery.find_images(self.path)
        assert len(self.files) > 0
        self.metadata_file = os.path.join(self.path, ".metadata.json")
        if not os.path.exists(self.metadata_file):
            self.update_metadata({})
        else:
            self.load_metadata()

        #  Workaround to ensure everything gets cleaned
        self.save_metadata()
        self.load_metadata()
        # Name represents the name from the path
        self.name = os.path.normpath(self.path).split(os.sep)[-1]

    @property
    def parent(self):
        return self._parent()

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

    @classmethod
    def find_images(cls, folder_path):
        images = []
        for path, dirs, files in os.walk(folder_path):
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext in Gallery.IMAGE_EXTS:
                    images.append(os.path.join(folder_path, f))
            break
        return sorted(images, key=lambda f: f.lower())

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

    def generate_image_hash(self):
        sha1 = hashlib.sha1()
        with open(self.files[0], "rb") as image:
            self.logger.debug("Generate sha1 for first image in folder.")
            buff = image.read(self.HASH_SIZE)
            while len(buff) > 0:
                sha1.update(buff)
                buff = image.read(self.HASH_SIZE)
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
