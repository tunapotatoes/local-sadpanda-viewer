#!/usr/bin/env python


from PySide import QtGui
import sys
import os
import io
import re
import json
import logging
from Logger import Logger
import Threads
import Windows
from Gallery import Gallery
from time import strftime
from RequestManager import RequestManager


class Program(QtGui.QApplication, Logger):
    CONFIG_FILE = os.path.expanduser("~/.sadpanda.config2")
    DEFAULT_CONFIG = {"dirs": [], "cookies": {"ipb_member_id": "",
                                              "ipb_pass_hash": ""}}
    galleries = []
    threads = {}
    config = {}

    def __init__(self, args):
        super(Program, self).__init__(args)
        self.setGraphicsSystem("opengl")
        self.main_window = Windows.MainWindow(self)
        if not os.path.exists(self.CONFIG_FILE):
            self.update_config(config=self.DEFAULT_CONFIG)
        else:
            self.load_config()
        self.find_galleries()

    @property
    def member_id(self):
        return self.config["cookies"]["ipb_member_id"]

    @member_id.setter
    def member_id(self, val):
        self.config["cookies"]["ipb_member_id"] = val

    @property
    def pass_hash(self):
        return self.config["cookies"]["ipb_pass_hash"]

    @pass_hash.setter
    def pass_hash(self, val):
        self.config["cookies"]["ipb_pass_hash"] = val

    @property
    def dirs(self):
        return self.config["dirs"]

    @dirs.setter
    def dirs(self, val):
        self.config["dirs"] = val

    def load_config(self):
        config = io.open(self.CONFIG_FILE, "r", encoding="utf-8")
        self.config = json.load(config)
        config.close()
        RequestManager.COOKIES = self.config["cookies"]
        self.main_window.member_id = self.member_id
        self.main_window.pass_hash = self.pass_hash
        self.main_window.dirs = self.dirs

    def update_config(self, **kwargs):
        new_config = kwargs.get("config", {})
        if new_config:
            self.logger.debug("Updating config with %s" % new_config)
            self.config.update(new_config)
        else:
            self.dirs = self.main_window.dirs
            self.member_id = self.main_window.member_id
            self.pass_hash = self.main_window.pass_hash
        RequestManager.COOKIES = self.config["cookies"]
        self.save_config()

    def save_config(self):
        self.logger.debug("Saving config.")
        config_file = open(self.CONFIG_FILE, "wb")
        config_file.write(json.dumps(self.config,
                                     ensure_ascii=False).encode("utf8"))
        config_file.close()

    def add_galleries(self, galleries):
        self.galleries += galleries
        self.main_window.add_galleries(galleries)

    def remove_galleries(self, galleries):
        self.main_window.hide_galleries(galleries)
        for gallery in galleries:
            self.logger.debug("Removing %s gallery." % gallery.title)
            self.galleries.remove(gallery)

    def process_search(self, search_text):
        filter_words = re.findall(r"[\"]?[\-][\"]?([\w]*)[\"]?",
                                  search_text)
        search_text = re.sub(r"[\"]?[\-][\"]?([\w]*)[\"]?", "",
                             search_text)
        filter_words = [w.replace(" ", "_").lower() for w in filter_words]
        quoted_words = re.findall(r"\"([^-].+?)\"", search_text)
        quoted_words = [w.replace(" ", "_") for w in quoted_words]
        words = re.sub(r"\"([^-].+?)\"", "", search_text)
        words = words.split() + quoted_words
        words = [w.replace("\"", "").lower() for w in words]
        self.logger.info("Search words: %s" % words)
        self.logger.info("Filter words: %s" % filter_words)
        return words, filter_words

    def search(self):
        search_text = self.main_window.search_text
        #self.main_window.hide_galleries(self.galleries)
        self.logger.info("Search_text: %s" % search_text)
        if search_text == "":
            self.main_window.show_galleries(self.galleries)
        else:
            show_galleries = []
            hide_galleries = []
            words, filters = self.process_search(search_text)
            for gallery in self.galleries:
                tags = [t.replace(" ", "_").lower() for t in gallery.tags]
                title = re.sub("\W", " ", gallery.title.lower()).split()
                if any(w in tags for w in filters) or any(w in title
                                                          for w in filters):
                    hide_galleries.append(gallery)
                elif all(w in tags for w in words) or len(words) == 0 or all(
                        w in title for w in words):
                    show_galleries.append(gallery)
                else:
                    hide_galleries.append(gallery)

            self.main_window.show_galleries(show_galleries)
            self.main_window.hide_galleries(hide_galleries)
        
    def find_galleries(self):
        self.logger.debug("Starting gallery thread.")
        assert not self.threads.get("gallery")
        self.main_window.disable_all_buttons()
        self.threads["gallery"] = Threads.GalleryThread(self)
        self.threads["gallery"].start()

    def find_galleries_done(self):
        self.logger.debug("Gallery thread done.")
        self.threads.pop("gallery")
        self.main_window.clear_progress_bar()
        self.main_window.enable_all_buttons()

    def get_metadata(self, galleries=None):
        self.logger.debug("Starting metadata thread.")
        assert not self.threads.get("metadata")
        self.main_window.disable_buttons(
            ["refreshButton", "submitButton", "cancelButton"])
        self.threads["metadata"] = Threads.SearchThread(self, galleries=galleries)
        self.threads["metadata"].start()

    def get_metadata_done(self):
        self.logger.debug("Metadata thread done.")
        self.threads.pop("metadata")
        self.main_window.clear_progress_bar()
        self.main_window.enable_all_buttons()
        [g.update_qgallery() for g in self.galleries]



    def _kill_threads(self):
        for key in self.threads:
            if self.threads[key].isAlive():
                self.threads[key]._Thread__stop()

    def closeEvent(self, event=None):
        self._kill_threads()
        if event is None:
            self.close()
        else:
            event.accept()





    def inc_progress(self, val):
        self.main_window.inc_progress(val)

if __name__ == "__main__":
    filename = strftime("%Y-%m-%d %H:%M:%S") + ".log"
    # logging.basicConfig(level=logging.DEBUG,
    #                     filename=filename,
    #                     format="%(asctime)s: %(name)s %(levelname)s %(message)s")
    app = Program(sys.argv)
    sys.exit(app.exec_())
