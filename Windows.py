#!/usr/bin/env python


from PySide import QtCore, QtGui
from Logger import Logger
from ui.main_window import Ui_MainWindow
from ui.flow import FlowLayout
from ui.gallery import C_QGallery
from ui.misc import C_QFileDialog
from ui.customize import Ui_Dialog
import weakref


class MainWindow(Logger, QtGui.QMainWindow):
    progress = 0
    BUTTONS = ["searchButton",
               "refreshButton",
               "submitButton",
               "cancelButton"]

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self._app = weakref.ref(app)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.flowLayout = FlowLayout(self.ui.scrollAreaWidgetContents)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.refreshButton.clicked.connect(self.app.get_metadata)
        self.ui.submitButton.clicked.connect(self.app.update_config)
        self.ui.cancelButton.clicked.connect(self.app.load_config)
        self.ui.directories.clicked.connect(self.browse)
        position = self.frameGeometry()
        position.moveCenter(
            QtGui.QDesktopWidget().availableGeometry().center())
        self.move(position.topLeft())
        self.show()
        self.raise_()

    @property
    def app(self):
        return self._app()

    @property
    def member_id(self):
        return self.ui.memberId.text()

    @member_id.setter
    def member_id(self, val):
        self.ui.memberId.setText(val)

    @property
    def pass_hash(self):
        return self.ui.passHash.text()

    @pass_hash.setter
    def pass_hash(self, val):
        self.ui.passHash.setText(val)

    @property
    def search_text(self):
        return self.ui.searchLine.text()

    @property
    def dirs(self):
        return self.ui.directories.toPlainText().splitlines()

    @dirs.setter
    def dirs(self, val):
        self.ui.directories.clear()
        [self.ui.directories.append(v) for v in val]

    def set_button_status(self, button, status):
        getattr(getattr(self.ui, str(button)), "setEnabled")(status)

    def disable_buttons(self, buttons):
        [self.set_button_status(b, False) for b in buttons]

    def enable_buttons(self, buttons):
        [self.set_button_status(b, True) for b in buttons]

    def disable_all_buttons(self):
        self.disable_buttons(self.BUTTONS)

    def enable_all_buttons(self):
        self.enable_buttons(self.BUTTONS)

    def add_galleries(self, galleries):
        for gallery in galleries:
            self.logger.debug("Adding %s gallery" % gallery.title)
            gallery.C_QGallery = C_QGallery(self, gallery)
            #self.ui.flowLayout.addWidget(gallery.C_QGallery)
        self.show_galleries(galleries)

    def show_galleries(self, galleries):
        for gallery in galleries:
            self.logger.debug("Showing %s gallery" % gallery.title)
            #self.ui.flowLayout.addItem(gallery.C_QGallery)
            self.ui.flowLayout.addWidget(gallery.C_QGallery)
            gallery.C_QGallery.show()
            #gallery.C_QGallery.setVisible(True)
        self.ui.flowLayout.update()

    def hide_galleries(self, galleries):
        for gallery in galleries:
            self.logger.debug("Hiding %s gallery" % gallery.title)
            self.ui.flowLayout.removeWidget(gallery.C_QGallery)
            gallery.C_QGallery.hide()
            #gallery.C_QGallery.setVisible(False)
        self.ui.flowLayout.update()

    def search(self):
        self.set_button_status("searchButton", False)
        self.app.search()
        self.set_button_status("searchButton", True)

    def inc_progress(self, val):
        self.ui.statusFrame.show()
        self.progress += val
        self.ui.progressBar.setValue(self.progress)

    def clear_progress_bar(self):
        self.ui.statusFrame.hide()
        self.progress = 0
        self.ui.progressBar.setValue(self.progress)

    def browse(self):
        self.logger.debug("Browsing for file")
        browser = C_QFileDialog()
        browser.exec_()
        if browser.open_clicked:
            self.directories = browser.selectedFiles
            for directory in browser.selectedFiles:
                self.ui.directories.append(directory)

    def get_metadata(self):
        self.disable_buttons(["refreshButton", "submitButton", "cancelButton"])
        self.app.get_metadata()
        self.enable_all_buttons()


class CustomizeWindow(Logger, QtGui.QDialog):
    def __init__(self, parent, gallery):
        super(CustomizeWindow, self).__init__(parent)
        self._parent = parent
        self._gallery = weakref.ref(gallery)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.submitButton.clicked.connect(self.gallery.save_customization)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        # position = self.frameGeometry()
        # position.moveCenter(
        #     QtGui.QDesktopWidget().availableGeometry().center())
        # self.move(position.topLeft())
        self.show()
        self.raise_()

    @property
    def parent(self):
        return self._parent()

    @property
    def gallery(self):
        return self._gallery()

    @property
    def title(self):
        return self.ui.customTitle.text()

    @title.setter
    def title(self, val):
        self.ui.customTitle.setText(val)

    @property
    def tags(self):
        return self.ui.customTags.text()

    @tags.setter
    def tags(self, val):
        self.ui.customTags.setText(val)

    @property
    def url(self):
        return self.ui.exhentaiURL.text()

    @url.setter
    def url(self, val):
        self.ui.exhentaiURL.setText(val)

    @property
    def rating(self):
        return self.ui.customRating.text()

    @rating.setter
    def rating(self, val):
        self.ui.customRating.setText(val)
