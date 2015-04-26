#!/usr/bin/env python2


from PySide import QtGui
from time import strftime
from Logger import Logger
from ui.gallery import QGallery
from RequestManager import RequestManager
from operator import attrgetter
import sys
import os
import re
import json
import logging
import Threads
import Windows
import Exceptions
import Database
from Gallery import Gallery


class Program(QtGui.QApplication, Logger):
    PAGE_SIZE = 100
    BUG_PAGE = "https://github.com/seanegoodwin/local-sadpanda-viewer/issues"
    CONFIG_DIR = os.path.expanduser("~/.lsv")
    THUMB_DIR = os.path.join(CONFIG_DIR, "thumbs")
    DEFAULT_CONFIG = {"dirs": [], "cookies": {"ipb_member_id": "",
                                              "ipb_pass_hash": ""}}

    class SortMap(object):
        NameSort = 0
        ReadCountSort = 1
        LastReadSort = 2
        RatingSort = 3

    def __init__(self, args):
        super(Program, self).__init__(args)

        self.tags = []
        self.galleries = []
        self.threads = {}
        self.config = {}
        self.pages = [[]]
        self.version = "ma.mi"
        self.page_number = 0
        self.main_window = Windows.MainWindow(self)
        self.error_window = Windows.Popup(self)

    def exec_(self):
        if not os.path.exists(self.THUMB_DIR):
            os.makedirs(self.THUMB_DIR)
        Database.setup()
        self.load_config()
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.main_window.setWindowIcon((QtGui.QIcon("icon.ico")))
        self.main_window.clear_progress_bar()
        self.setup_threads()
        self.find_galleries(initial=True)
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
        self.logger.debug("Loading config from db.")
        with Database.get_session(self) as session:
            db_config = session.query(Database.Config)
            if db_config.count() == 0:
                self.config = self.DEFAULT_CONFIG
                new_config = Database.Config()
                new_config.json = json.dumps(self.config)
                new_config.version = self.version
                session.add(new_config)
                session.commit()
            else:
                assert db_config.count() == 1
                db_config = db_config[0]
                self.config = json.loads(db_config.json)
                self.version = db_config.version
        RequestManager.COOKIES = self.config["cookies"]
        self.main_window.member_id = self.member_id
        self.main_window.pass_hash = self.pass_hash
        self.main_window.dirs = self.dirs

    def save_config(self):
        self.logger.debug("Save config to db.")
        with Database.get_session(self) as session:
            db_config = session.query(Database.Config)[0]
            db_config.json = json.dumps(self.config, ensure_ascii=False).encode("utf8")
            db_config.version = self.version
            session.add(db_config)

    def update_config(self, **kwargs):
        new_config = kwargs.get("config", {})
        self.logger.info("Updating config.")
        if new_config:
            self.config.update(new_config)
        else:
            self.dirs = self.main_window.dirs
            self.member_id = self.main_window.member_id
            self.pass_hash = self.main_window.pass_hash
        RequestManager.COOKIES = self.cookies
        self.save_config()

    def process_search(self, search_text):
        search_text = search_text.lower()
        rating = re.search(r"rating:(\S*)", search_text)
        if rating:
            search_text = re.sub("rating:\S*", "", search_text)
            rating = rating.groups()[0]
            if rating[0] == "=" and rating[1] != "=":
                rating = "=" + rating
            try:
                eval("0.0" + rating)
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

    @staticmethod
    def in_search(tags, title, input_tag):
        if input_tag in title:
            return True
        for tag in tags:
            if input_tag in tag:
                return True
        return False

    def setup_threads(self):
        self.threads["gallery"] = Threads.GalleryThread(self)
        self.threads["gallery"].start()
        self.threads["image"] = Threads.ImageThread(self)
        self.threads["image"].start()
        self.threads["metadata"] = Threads.SearchThread(self)
        self.threads["metadata"].start()

    def setup_tags(self):
        tags = []
        for gallery in self.galleries:
            tags += list(map(lambda x: x.replace(" ", "_").lower(), gallery.tags))
        self.tags = list(set(tags))
        self.tags += list(map(lambda x: "-" + x, self.tags))
        self.main_window.update_completer()

    def find_galleries(self, initial=False):
        if initial:
            self.main_window.status_messenger.set_initial_loading()
        elif not self.galleries:
            self.main_window.status_messenger.set_searching_galleries()
        self.main_window.disable_all_buttons()
        self.logger.debug("Sending start signal to gallery thread")
        self.threads["gallery"].queue.put(None)

    def find_galleries_done(self, galleries):
        self.main_window.enable_all_buttons()
        print galleries[0].time_loading[0]
        for gallery in galleries:
            gallery.C_QGallery = QGallery(self.main_window, gallery)
        self.galleries += galleries
        if self.galleries:
            self.main_window.status_messenger.hide()
        else:
            self.main_window.status_messenger.set_no_galleries()
        self.logger.debug("Gallery thread done")
        self.setup_tags()
        self.sort()
        self.setup_pages()
        self.show_page()

    def show_page(self):
        need_images = []
        for gallery in self.current_page:
            if not gallery.image:
                need_images.append(gallery)
        self.logger.info("Need images: %s" % [g.name for g in need_images])
        self.generate_images(need_images)
        self.main_window.show_galleries(self.current_page)

    def hide_page(self):
        self.main_window.hide_galleries(self.current_page)

    def generate_images(self, galleries):
        self.main_window.button_lock = True
        self.main_window.disable_all_buttons()
        self.logger.debug("Starting image thread.")
        self.threads["image"].queue.put(galleries)

    def image_generated(self, galleries):
        for gallery in galleries:
            gallery.C_QGallery.set_image()
        #     gallery.C_QGallery = C_QGallery(self.main_window, gallery)

    def image_thread_done(self):
        self.main_window.button_lock = False
        self.main_window.enable_all_buttons()
        self.logger.debug("Image thread done.")
        self.main_window.clear_progress_bar()

    def get_metadata(self, galleries=None):
        galleries = galleries or self.galleries
        self.logger.debug("Starting metadata thread")
        self.main_window.disable_buttons(
            ["refreshButton", "submitButton", "cancelButton"])
        self.threads["metadata"].queue.put(galleries)

    def get_metadata_done(self):
        self.logger.debug("Metadata thread done.")
        self.setup_tags()
        self.main_window.clear_progress_bar()
        self.main_window.enable_all_buttons()
        [g.update_qgallery() for g in self.galleries]

    def close(self):
        # for t in self.threads:
        #     if not self.threads[t].daemon:
        #         self.threads[t].kill = True
        #         self.threads[t].join()
        for gallery in self.galleries:
            gallery.__del__()
        self.quit()

    def sort(self, sort_type=None, descending=False):
        sort_type = sort_type or self.SortMap.RatingSort
        key = None
        if sort_type == self.SortMap.NameSort:
            key = attrgetter("sort_name")
        elif sort_type == self.SortMap.LastReadSort:
            key = attrgetter("last_read")
        elif sort_type == self.SortMap.RatingSort:
            key = attrgetter("sort_rating")
        elif sort_type == self.SortMap.ReadCountSort:
            key = attrgetter("read_count")

        self.galleries.sort(key=key, reverse=descending)

    def switch_page(self, *args):
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

    def thread_exception_handler(self, thread, exception):
        self.error_window.exception_hook(*exception)


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    filename = strftime("%Y-%m-%d-%H.%M.%S") + ".log"
    logging.basicConfig(level=logging.DEBUG,
                        filename=filename,
                        format="%(asctime)s: %(name)s %(levelname)s %(message)s")
    if os.name == "nt":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("lsv.ui")
    app = Program(sys.argv)
    sys.excepthook = app.error_window.exception_hook
    sys.exit(app.exec_())
