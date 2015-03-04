#!/usr/bin/env python


from PySide import QtCore, QtGui
from Logger import Logger
from ui.main_window import Ui_MainWindow
from ui.flow import FlowLayout
from ui.misc import C_QFileDialog
from ui.customize import Ui_Dialog
import weakref
import Exceptions


class MainWindow(Logger, QtGui.QMainWindow):
    progress = 0
    BUTTONS = ["searchButton",
               "refreshButton",
               "submitButton",
               "cancelButton",
               "searchLine",
               "nextButton",
               "prevButton",
               "pageBox"]

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.button_lock = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.flowLayout = FlowLayout(self.ui.scrollAreaWidgetContents)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.refreshButton.clicked.connect(self.refresh_button_handler)
        self.ui.submitButton.clicked.connect(self.app.update_config)
        self.ui.cancelButton.clicked.connect(self.app.load_config)
        self.ui.nextButton.clicked.connect(self.next_page)
        self.ui.prevButton.clicked.connect(self.prev_page)
        self.ui.directories.clicked.connect(self.browse)
        position = self.frameGeometry()
        position.moveCenter(
            QtGui.QDesktopWidget().availableGeometry().center())
        self.move(position.topLeft())
        self.show()
        self.raise_()

    def closeEvent(self, event=None):
        self.app.close()

    def refresh_button_handler(self):
        if self.ui.galleryBox.isChecked():
            self.app.find_galleries()
        if self.ui.metaBox.isChecked():
            self.app.get_metadata()

    def next_page(self):
        next_page = self.page_number + 1
        if next_page == self.max_page:
            return
        self.page_number = next_page

    def prev_page(self):
        prev_page = self.page_number - 1
        if prev_page == -1:
            return
        self.page_number = prev_page

    def reset_scrollbar(self):
        scrollbar = self.ui.scrollArea.verticalScrollBar()
        scrollbar.setValue(scrollbar.minimum())

    @property
    def page_number(self):
        return self.ui.pageBox.currentIndex()

    @page_number.setter
    def page_number(self, val):
        self.ui.pageBox.setCurrentIndex(val)

    @property
    def max_page(self):
        return self.ui.pageBox.count()

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
        getattr(getattr(self.ui, button), "setEnabled")(status)

    def disable_buttons(self, buttons):
        [self.set_button_status(b, False) for b in buttons]

    def enable_buttons(self, buttons):
        if self.button_lock:
            return
        [self.set_button_status(b, True) for b in buttons]

    def disable_all_buttons(self):
        self.disable_buttons(self.BUTTONS)
        [g.disable_all_buttons() for g in self.app.current_page]

    def enable_all_buttons(self):
        self.enable_buttons(self.BUTTONS)
        [g.enable_all_buttons() for g in self.app.current_page]

    def show_galleries(self, galleries):
        for gallery in galleries:
            assert gallery in self.app.current_page
            self.logger.debug("Showing %s gallery" % gallery.title)
            self.ui.flowLayout.addWidget(gallery.C_QGallery)
            gallery.C_QGallery.show()
        self.ui.flowLayout.update()

    def hide_galleries(self, galleries):
        for gallery in galleries:
            assert gallery in self.app.current_page
            self.logger.debug("Hiding %s gallery" % gallery.title)
            self.ui.flowLayout.removeWidget(gallery.C_QGallery)
            try:
                gallery.C_QGallery.hide()
            except AttributeError:
                pass
        self.ui.flowLayout.update()

    def search(self):
        self.disable_all_buttons()
        self.app.search()
        self.enable_all_buttons()

    def inc_progress(self, val):
        self.ui.statusFrame.show()
        self.progress += val
        self.ui.progressBar.setValue(self.progress)

    def clear_progress_bar(self):
        self.ui.statusFrame.hide()
        self.progress = 0
        self.ui.progressBar.setValue(self.progress)

    def browse(self):
        self.logger.debug("Browsing for files.")
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

    def configure_combo_box(self):
        self.ui.pageBox.currentIndexChanged.connect(lambda x: None)
        self.ui.pageBox.clear()
        self.ui.pageBox.addItems(list(map(lambda x: "Page " + str(x),
                                          range(1, self.app.page_count + 1))))
        self.ui.pageBox.currentIndexChanged.connect(self.app.switch_page)


class CustomizeWindow(Logger, QtGui.QDialog):
    def __init__(self, app, gallery):
        super(CustomizeWindow, self).__init__(app)
        self._gallery = weakref.ref(gallery)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.submitButton.clicked.connect(self.gallery.save_customization)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup | QtCore.Qt.WindowSystemMenuHint)
        # position = self.frameGeometry()
        # position.moveCenter(
        #     QtGui.QDesktopWidget().availableGeometry().center())
        # self.move(position.topLeft())
        self.show()
        self.raise_()

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


class Popup(QtGui.QMessageBox, Logger):

    def __init__(self, app):
        super(Popup, self).__init__()
        self.app = app

    def exception_hook(self, extype, exvalue, extraceback):
        fatal = True  # Default to true for unhandled exceptions
        if issubclass(extype, Exceptions.BaseException):
            fatal = exvalue.fatal
            self.setText(exvalue.msg)
        else:
            self.setText("An unhandled %s exception has occurred. The program will now shutdown." % str(extype))
            self.logger.error("An unhandled %s exception occured." % str(extype))
        #  self.logger.error(traceback.print_tb(extraceback))
        #self.logger.error("".join(traceback.format_tb(extraceback)))
        self.logger.error("Exception details: ",
                          exc_info=(extype, exvalue, extraceback))
        self.show()
        self.exec_()
        if fatal:
            self.app.close()
        else:
            self.app.main_window.enable_all_buttons()
            self.app.main_window.clear_progress_bar()
