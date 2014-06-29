#!/usr/bin/python2

import json
import sys
import io
import os
import re
import copy
import threading
from PySide import QtCore, QtGui
import Gallery
import Request
from ui.main_window import Ui_MainWindow
from ui.settings import Ui_Form as Ui_Settings
from ui.flow import FlowLayout
from ui.gallery import C_QGallery


class FindThread(threading.Thread):
    def __init__(self, parent, **kwargs):
        threading.Thread.__init__(self)
        self.parent = parent
        self.kwargs = kwargs
        initial_thread = self.parent.threads.get("it", None)
        while initial_thread is not None and initial_thread.isAlive():
            continue
        force = self.kwargs.get("force", False)
        self.temp_galleries = [g for g in self.parent.galleries if
                               not g.has_metadata() or force]

    def run(self):
        self._find_galleries(self.temp_galleries, **self.kwargs)
        self.temp_galleries = [g for g in self.temp_galleries if
                               g.WebGallery is not None]
        self._get_metadata(self.temp_galleries, **self.kwargs)

    def _find_galleries(self, galleries, **kwargs):
        for gallery in galleries:
            gallery.search()

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


class MainWindow(QtGui.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.request_object = Request.RequestObject(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_settings()
        self.ui.flowLayout = FlowLayout(self.ui.scrollAreaWidgetContents)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.refreshButton.clicked.connect(self.refresh)
        self.ui.submitSettings.clicked.connect(self.save_settings)
        self.ui.cancelSettings.clicked.connect(self.load_settings)
        self.ui.statusFrame.hide()
        self.galleries = []
        # Right now only using one thread, but might have more in the future
        self.threads = {}
        self.show()
        self.find_galleries()

    def load_settings(self):
        config_file = io.open("config.json", "r", encoding="utf-8")
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
        self.config["dirs"] = []
        for line in self.ui.directories.toPlainText().splitlines():
            self.config["dirs"].append(line)
        config_file = open("config.json", "w")
        json_data = json.dumps(self.config, ensure_ascii=False).encode("utf8")
        config_file.write(json_data)
        config_file.close()

    def resizeEvent(self, event):
        event.accept()

    def refresh(self):
        if self.ui.refBox.isChecked():
            self.find_galleries()
        if self.ui.forceBox.isChecked():
            self.force()
        elif self.ui.metaBox.isChecked():
            self.get_metadata()

    def force(self):
        self.get_metadata(force=True)

    def get_metadata(self, **kwargs):
        # Keep this on seperate thread because it takes forever and the ui
        # would freeze otherwise
        self.threads["ft"] = FindThread(self, **kwargs)
        self.threads["ft"].start()

    def _kill_threads(self):
        for key in self.threads.keys():
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
            quoted_words = re.findall(r"\"(.+?)\"", search_text)
            for word in quoted_words:
                word = word.replace(" ", "_")
            search_test = search_text.replace("\"", "")
            #print re.findall(r"-(.+?)", search_text)
            self._set_visible(search_test.split())

        self.ui.searchButton.setEnabled(True)

    def _set_visible(self, search):
        galleries = [g for g in self.galleries if g.has_metadata()]
        for gallery in galleries:
            tags = [t.lower() for t in gallery.local_metadata[
                "gmetadata"]["tags"]]
            for word in search:
                #print gallery.local_metadata["gmetadata"]["title"]
                if (word.lower() in tags or word.lower() in
                   gallery.local_metadata["gmetadata"]["title"].lower()):
                    self.ui.flowLayout.addWidget(gallery.C_QGallery)
                    gallery.C_QGallery.setVisible(True)
                else:
                    self.ui.flowLayout.removeWidget(gallery.C_QGallery)
                    gallery.C_QGallery.setVisible(False)

    def hide_all_galleries(self):
        for gallery in self.galleries:
            try:
                gallery.C_QGallery.setVisible(False)
                self.ui.flowLayout.removeWidget(gallery.C_QGallery)
            except:
                pass

    def show_all_galleries(self):
        for gallery in self.galleries:
            try:
                gallery.C_QGallery.setVisible(True)
                self.ui.flowLayout.addWidget(gallery.C_QGallery)
            except:
                pass

    def find_galleries(self):
        self.hide_all_galleries()
        self._find_galleries()
        for gallery in self.galleries:
            if gallery.has_metadata():
                gallery.C_QGallery = C_QGallery(self.ui.scrollArea, gallery)
                self.ui.flowLayout.addWidget(gallery.C_QGallery)
                self.ui.flowLayout.addWidget(gallery.C_QGallery)
                gallery.C_QGallery.show()
                self.app.processEvents()

    def _find_galleries(self):
        self.galleries = []
        for folder in self.config["dirs"]:
            folder = os.path.expanduser(folder)
            bool_skip = True
            for path, dirs, files in os.walk(folder):
                if bool_skip:
                    bool_skip = False
                    continue
                self.galleries.append(Gallery.LocalGallery(self, path))


class Program(QtGui.QApplication):
    def __init__(self, args):
        super(Program, self).__init__(args)
        self.main_window = MainWindow(self)

if __name__ == "__main__":
    app = Program(sys.argv)
    sys.exit(app.exec_())
