#!/usr/bin/python2

import json
import sys
import os
import time
import requests
from PySide import QtCore, QtGui
import gallery
import search
from ui.main_window import Ui_MainWindow

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        config_file = open("config.json")
        self.config = json.load(config_file)
        config_file.close()
        self._find_galleries()
        self._get_metadata(self.galleries)

    def _find_galleries(self):
        self.galleries = []
        for folder in self.config["dirs"]:
            folder = os.path.expanduser(folder)
            count = 0
            for path, dirs, files in os.walk(folder):
                if count == 0:
                    count += 1
                    continue
                self.galleries.append(gallery.LocalGallery(path))
                count += 1
                if count % self.config["API_MAX_SEQUENTIAL_REQUESTS"] == 0:
                    time.sleep(self.config["API_TIME_WAIT"])
        
    def _get_metadata(self, galleries, **kwargs):
        if len(galleries) == 0:
            return
        refresh = kwargs.get("refresh", False)
        max_seq = kwargs.get("max_seq", self.config["API_MAX_SEQUENTIAL_REQUESTS"])
        if max_seq == 0:
            max_seq = self.config["API_MAX_SEQUENTIAL_REQUESTS"]
            time.sleep(self.config["API_TIME_WAIT"])
        data = self.config["base_request"].copy()
        for gallery in galleries[:self.config["API_MAX_ENTRIES"]]:
            if gallery.WebGallery is None:
                return
            data["gidlist"].append(gallery.WebGallery.gid)
        request = requests.post(self.config["API_URL"], data=json.dumps(data),
                                cookies=self.config["cookies"])
        if not search.validate_request(request):
            print("Failed")
            return
        for gallery, metadata in zip(galleries[:self.config["API_MAX_ENTRIES"]],
                                     request.json()["gmetadata"]):
            gallery.save_metadata(metadata)
        kwargs["max_seq"] = max_seq - 1
        self._get_metadata(galleries[self.config["API_MAX_ENTRIES"]:], **kwargs)
            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
