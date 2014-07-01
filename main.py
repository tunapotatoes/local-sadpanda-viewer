#!/usr/bin/python2

from PySide import QtCore, QtGui
from decimal import Decimal
import json
import sys
import io
import os
import re
import copy
import Gallery
import Request
import Threads
from ui.main_window import Ui_MainWindow
from ui.flow import FlowLayout
from ui.gallery import C_QGallery


class Program(QtGui.QApplication):
    def __init__(self, args):
        super(Program, self).__init__(args)
        self.main_window = MainWindow(self)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.config_file = os.path.expanduser("~/.sadpanda.config")
        self.request_object = Request.RequestObject(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_settings()
        self.ui.flowLayout = FlowLayout(self.ui.scrollAreaWidgetContents)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.refreshButton.clicked.connect(self.refresh)
        self.ui.submitSettings.clicked.connect(self.save_settings)
        self.ui.cancelSettings.clicked.connect(self.load_settings)
        self.buttons = {"searchButton": self.ui.searchButton,
                        "refreshButton": self.ui.refreshButton,
                        "submitButton": self.ui.submitSettings,
                        "cancelButton": self.ui.cancelSettings}
        self.progress = Decimal(0.0)
        self.ui.statusFrame.hide()
        self.galleries = []
        # Right now only using two threads, but might have more in the future
        self.threads = {}
        self.show()
        self.find_galleries()

    def inc_progress(self, val):
        "I have reasons for doing this"
        # TODO explain reasons for doing this
        val *= Decimal(100)
        self.ui.statusFrame.show()
        self.progress += val
        self.ui.progressBar.setValue(self.progress)

    def disable_buttons(self, buttons=[]):
        if len(buttons) == 0:
            for button in self.buttons:
                self.buttons[button].setEnabled(False)
        else:
            for button in buttons:
                self.buttons[button].setEnabled(False)

    def enable_buttons(self, buttons=[]):
        if len(buttons) == 0:
            for button in self.buttons:
                self.buttons[button].setEnabled(True)
        else:
            for button in buttons:
                self.buttons[button].setEnabled(True)

    def find_galleries(self):
        self.disable_buttons()
        self._find_galleries()
        self.progress = Decimal(0.0)
        self.threads["it"] = Threads.ImageThread(self)
        self.threads["it"].start()

    def image_thread_done(self):
        self.ui.statusFrame.hide()
        self.threads.pop("it")
        self.progress = Decimal(0.0)
        self.enable_buttons()

    def rest_thread_done(self):
        self.ui.statusFrame.hide()
        self.threads.pop("rt")
        self.progress = Decimal(0.0)
        self.enable_buttons(["refreshButton", "submitButton", "cancelButton"])
        self.find_galleries()

    def _find_galleries(self):
        self.hide_all_galleries()
        self.remove_all_galleries()
        for folder in self.config["dirs"]:
            folder = os.path.expanduser(folder)
            bool_skip = True
            for path, dirs, files in os.walk(folder):
                if bool_skip:
                    bool_skip = False
                    continue
                self.galleries.append(Gallery.LocalGallery(self, path))

    def remove_all_galleries(self):
        for gallery in self.galleries:
            try:
                gallery.C_QGallery.gallery = None
                gallery.C_QGallery = None
                gallery = None
            except:
                pass
        self.galleries = []

    def add_gallery_image(self, gallery, image):
        gallery.C_QGallery = C_QGallery(self.ui.scrollArea, gallery, image)
        self.ui.flowLayout.addWidget(gallery.C_QGallery)
        gallery.C_QGallery.show()

    def load_settings(self):
        if not os.path.exists(self.config_file):
            self._write_default_config()
        config_file = io.open(self.config_file, "r", encoding="utf-8")
        self.config = json.load(config_file)
        config_file.close()
        self.ui.memberId.setText(self.config["COOKIES"]["ipb_member_id"])
        self.ui.passHash.setText(self.config["COOKIES"]["ipb_pass_hash"])
        self.ui.directories.clear()
        for directory in self.config["dirs"]:
            self.ui.directories.append(directory)

    def save_settings(self):
        self.config["COOKIES"]["ipb_member_id"] = self.ui.memberId.text()
        self.config["COOKIES"]["ipb_pass_hash"] = self.ui.passHash.text()
        old_dirs = self.config["dirs"]
        self.config["dirs"] = []
        for line in self.ui.directories.toPlainText().splitlines():
            self.config["dirs"].append(line)
        config_file = open(self.config_file, "w")
        json_data = json.dumps(self.config, ensure_ascii=False).encode("utf8")
        config_file.write(json_data)
        config_file.close()
        if old_dirs != self.config["dirs"]:
            self.find_galleries()

    def refresh(self):
        if self.ui.refBox.isChecked():
            self.find_galleries()
        if self.ui.metaBox.isChecked() or self.ui.forceBox.isChecked():
            self.get_metadata(force=self.ui.forceBox.isChecked())

    def get_metadata(self, **kwargs):
        # Keep this on seperate thread because it takes forever and the ui
        # would freeze otherwise
        self.disable_buttons(["refreshButton", "submitButton", "cancelButton"])
        self.threads["rt"] = Threads.RestThread(self, **kwargs)
        self.threads["rt"].start()

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

    def search(self):
        self.ui.searchButton.setEnabled(False)
        self.hide_all_galleries()
        search_text = self.ui.searchLine.text()
        if search_text == "":
            self.show_all_galleries()
        else:
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
            self._set_visible(words, filter_words)

        self.ui.searchButton.setEnabled(True)

    def _set_visible(self, search, filters=[]):
        galleries = [g for g in self.galleries if g.has_metadata()]
        for gallery in galleries:
            tags = [t.replace(" ", "_").lower() for t in
                    gallery.local_metadata["gmetadata"]["tags"]]
            title = gallery.local_metadata["gmetadata"]["title"].lower()
            if any(w in tags for w in filters) or self._tag_in_title(filters,
                                                                     title):
                self.ui.flowLayout.removeWidget(gallery.C_QGallery)
                gallery.C_QGallery.setVisible(False)
                continue
            if (any(w in tags for w in search) or len(
                    search) == 0 or self._tag_in_title(search, title)):
                self.ui.flowLayout.addWidget(gallery.C_QGallery)
                gallery.C_QGallery.setVisible(True)
            else:
                self.ui.flowLayout.removeWidget(gallery.C_QGallery)
                gallery.C_QGallery.setVisible(False)

    def _tag_in_title(self, tags, title):
        for tag in tags:
            if tag in title:
                return True
        return False

    def hide_all_galleries(self):
        for gallery in self.galleries:
            try:
                gallery.C_QGallery.setVisible(False)
                self.ui.flowLayout.removeWidget(gallery.C_QGallery)
                gallery.C_QGallery.setParent(None)
            except:
                pass

    def show_all_galleries(self):
        for gallery in self.galleries:
            try:
                gallery.C_QGallery.setVisible(True)
                self.ui.flowLayout.addWidget(gallery.C_QGallery)
            except:
                pass

    def _write_default_config(self):
        config_file = open(self.config_file, "w")
        default_json = {"dirs": [],
                        "API_TIME_WAIT": 5,
                        "COOKIES": {"ipb_member_id": "", "ipb_pass_hash": ""},
                        "exts": [".png", ".jpg", ".jpeg", ".gif"],
                        "API_TIME_TOO_FAST_WAIT": 100,
                        "API_TIME_REQ_DELAY": 3,
                        "image_width": 200,
                        "base_url": "http://exhentai.org/?f_doujinshi=1&f_manga=1&f_artistcg=1&f_gamecg=1&f_western=1&f_non-h=1&f_imageset=1&f_cosplay=1&f_asianporn=1&f_misc=1&f_sname=on&adv&f_search=%s&advsearch=1&f_srdd=2&f_apply=Apply+Filter&f_shash=%s&page=%s&fs_smiliar=1&fs_covers=1",
                        "HEADERS": {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0"},
                        "hash_size": 8192,
                        "base_request": {"method": "gdata", "gidlist": []},
                        "API_MAX_ENTRIES": 25,
                        "API_MAX_SEQUENTIAL_REQUESTS": 4,
                        "API_URL": "http://exhentai.org/api.php"}
        config_file.write(json.dumps(default_json,
                                     ensure_ascii=False).encode("utf8"))
        config_file.close()

if __name__ == "__main__":
    app = Program(sys.argv)
    sys.exit(app.exec_())
