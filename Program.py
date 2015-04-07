#!/usr/bin/env python2


from PySide import QtGui
from time import strftime
from Logger import Logger
from ui.gallery import C_QGallery
from RequestManager import RequestManager
import sys
import os
import io
import re
import json
import logging
import Threads
import Windows
import Exceptions


class Program(QtGui.QApplication, Logger):
    PAGE_SIZE = 100
    CONFIG_DIR = os.path.expanduser("~/.lsv")
    CONFIG_FILE = os.path.expanduser("~/.sadpanda.config2")
    DEFAULT_CONFIG = {"dirs": [], "cookies": {"ipb_member_id": "",
                                              "ipb_pass_hash": ""}}

    def __init__(self, args):
        super(Program, self).__init__(args)
        self.main_window = Windows.MainWindow(self)
        self.error_window = Windows.Popup(self)
        self.galleries = []
        self.threads = {}
        self.config = {}
        self.pages = [[]]
        self.page_number = 0

    def exec_(self):
        if not os.path.exists(self.CONFIG_FILE):
            self.update_config(config=self.DEFAULT_CONFIG)
        else:
            self.load_config()
        self.find_galleries()
        return super(Program, self).exec_()

    @property
    def current_page(self):
        return self.pages[self.page_number]

    @property
    def page_count(self):
        return len(self.pages)

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

    @property
    def cookies(self):
        return self.config["cookies"]

    def load_config(self):
        config = io.open(self.CONFIG_FILE, "r", encoding="utf-8")
        self.config = json.load(config)
        self.logger.debug("Config loaded: %s" % self.config)
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
        RequestManager.COOKIES = self.cookies
        self.save_config()

    def save_config(self):
        self.logger.debug("Saving config.")
	try:
            config_file = open(self.CONFIG_FILE, "r+b")
    	except IOError:
            config_file = open(self.CONFIG_FILE, "wb")
        config_file.write(json.dumps(self.config,
                                     ensure_ascii=False).encode("utf8"))
        config_file.truncate()
        config_file.close()

    def process_search(self, search_text):
        search_text = search_text.lower()
        rating = re.search(r"rating:(\S*)", search_text)
        if rating:
            search_text = re.sub("rating:\S*", "", search_text)
            rating = rating.groups()[0]
            if rating[0] == "=" and rating[1] != "=":
                rating = "=" + rating
            try:
                eval("0" + rating)
            except:
                raise Exceptions.InvalidRatingSearch()
        filter_words = re.findall(r"[\"]?[\-][\"]?([\w]*)[\"]?",
                                  search_text)
        search_text = re.sub(r"[\"]?[\-][\"]?([\w]*)[\"]?", "",
                             search_text)
        filter_words = [w.replace(" ", "_") for w in filter_words]
        quoted_words = re.findall(r"\"([^-].+?)\"", search_text)
        quoted_words = [w.replace(" ", "_") for w in quoted_words]
        words = re.sub(r"\"([^-].+?)\"", "", search_text)
        words = words.split() + quoted_words
        words = [w.replace("\"", "") for w in words]
        self.logger.info("Search words: %s" % words)
        self.logger.info("Filter words: %s" % filter_words)
        self.logger.info("Rating function: %s" % rating)
        return words, filter_words, rating

    def search(self):
        search_text = self.main_window.search_text
        self.logger.info("Search_text: %s" % search_text)
        if search_text == "":
            self.hide_page()
            self.setup_pages()
            self.show_page()
        else:
            words, filters, rating = self.process_search(search_text)
            self.hide_page()
            galleries = []
            for gallery in self.galleries:
                title = re.sub("\W", " ", gallery.title.lower()).split()
                tags = [t.replace(" ", "_").lower() for t in gallery.tags]
                if rating and (not gallery.rating or
                               not eval(gallery.rating + rating)):
                    continue
                if any(self.in_search(tags, title, w) for w in filters):
                    continue
                if all(self.in_search(tags, title, w) for w in words) or len(words) == 0:
                    galleries.append(gallery)
            self.setup_pages(galleries)
            self.show_page()

    def in_search(self, tags, title, input_tag):
        if input_tag in title:
            return True
        for tag in tags:
            if input_tag in tag:
                return True
        return False

    def find_galleries(self):
        self.main_window.disable_all_buttons()
        self.logger.debug("Starting gallery thread.")
        assert not self.threads.get("gallery")
        self.threads["gallery"] = Threads.GalleryThread(self)
        self.threads["gallery"].start()

    def find_galleries_done(self, galleries):
        self.main_window.enable_all_buttons()
        self.galleries += galleries
        self.logger.debug("Gallery thread done.")
        self.threads.pop("gallery")
        self.setup_pages()
        self.show_page()

    def show_page(self):
        show_galleries = []
        need_images = []
        for gallery in self.current_page:
            if not gallery.C_QGallery:
                need_images.append(gallery)
            else:
                show_galleries.append(gallery)
        self.logger.info("Need images: %s" % [g.name for g in need_images])
        self.generate_images(need_images)
        self.main_window.show_galleries(show_galleries)

    def hide_page(self):
        self.main_window.hide_galleries(self.current_page)

    def generate_images(self, galleries):
        self.main_window.button_lock = True
        self.main_window.disable_all_buttons()
        self.logger.debug("Starting image thread.")
        assert not self.threads.get("image")
        self.threads["image"] = Threads.ImageThread(self, galleries)
        self.threads["image"].start()

    def image_generated(self, galleries):
        for gallery in galleries:
            gallery.C_QGallery = C_QGallery(self.main_window, gallery)
        self.main_window.show_galleries(galleries)

    def image_thread_done(self):
        self.main_window.button_lock = False
        self.main_window.enable_all_buttons()
        self.logger.debug("Image thread done.")
        self.threads.pop("image")
        self.main_window.clear_progress_bar()

    def get_metadata(self, galleries=None):
        self.logger.debug("Starting metadata thread.")
        assert not self.threads.get("metadata")
        self.main_window.disable_buttons(
            ["refreshButton", "submitButton", "cancelButton"])
        self.threads["metadata"] = Threads.SearchThread(self,
                                                        galleries=galleries)
        self.threads["metadata"].start()

    def get_metadata_done(self):
        self.logger.debug("Metadata thread done.")
        self.threads.pop("metadata")
        self.main_window.clear_progress_bar()
        self.main_window.enable_all_buttons()
        [g.update_qgallery() for g in self.galleries]

    def close(self):
        for t in self.threads:
            self.threads[t].kill = True
            self.threads[t].join()
        for gallery in self.galleries:
            gallery.__del__()
        self.quit()

    def switch_page(self):
        if self.main_window.page_number in [-1, self.page_number]:
            return
        self.main_window.reset_scrollbar()
        self.hide_page()
        self.page_number = self.main_window.page_number
        self.show_page()

    def setup_pages(self, galleries=None):
        if galleries is None:
            galleries = self.galleries
        self.pages = [galleries[i:i + self.PAGE_SIZE]
                      for i in range(0, len(galleries),
                                     self.PAGE_SIZE)] or [[]]
        if self.page_number + 1 > self.page_count:
            self.page_number = self.page_count - 1
        self.main_window.configure_combo_box()

    def inc_progress(self, val):
        self.main_window.inc_progress(val)

    def thread_exception_handler(self, id, exception):
        try:
            self.threads.pop(id)
        except KeyError:
            pass
        self.error_window.exception_hook(*exception)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    filename = strftime("%Y-%m-%d-%H.%M.%S") + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        filename=filename,
                        format="%(asctime)s: %(name)s %(levelname)s %(message)s")
    app = Program(sys.argv)
    sys.excepthook = app.error_window.exception_hook
    sys.exit(app.exec_())
