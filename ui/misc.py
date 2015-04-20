#!/usr/bin/env python

import os
from PySide import QtCore, QtGui
import qtawesome as qta


class C_QCompleter(QtGui.QCompleter):

    def pathFromIndex(self, index):
        path = super(C_QCompleter, self).pathFromIndex(index)
        path_list = str((self.widget().text())).split(" ")
        if len(path_list):
            path = "%s %s" % (" ".join(path_list[:-1]), path)
        return path.lstrip()

    def splitPath(self, path):
        return [str(path.split(" ")[-1])]


class C_QStar(QtGui.QLabel):
    COLOR = "#F1F1F1"
    SIZE = 25
    PXMSIZE = (SIZE, SIZE)
    MAX_NUMBER = 5

    def __init__(self, parent, number):
        super(C_QStar, self).__init__()
        self.parent = parent
        self.number = number
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.mouseMoveEvent(event)

    def mouseMoveEvent(self, event):
        position = self.validate_position()
        if position:
            self.parent.setup_rating(self.get_rating(position))

    def validate_position(self):
        cursor = QtGui.QCursor()
        pos = cursor.pos()
        rect = self.geometry()
        relative_pos = self.mapFromGlobal(pos)
        if self.underMouse():
            return relative_pos

    def get_rating(self, pos):
        if pos.x() >= self.SIZE / 2:
            return self.number
        else:
            return self.number - .5

    def leaveEvent(self, event):
        self.parent.setup_rating()

    def mousePressEvent(self, event):
        position = self.validate_position()
        if position:
            event.accept()
            if event.button() == QtCore.Qt.LeftButton:
                self.parent.gallery.set_rating(self.get_rating(position))
            elif event.button() == QtCore.Qt.RightButton:
                self.parent.gallery.set_rating("")

    def set_full_star(self):
        self.setPixmap(qta.icon("fa.star", color=self.COLOR).pixmap(*self.PXMSIZE))

    def set_half_star(self):
        self.setPixmap(qta.icon("fa.star-half-o", color=self.COLOR).pixmap(*self.PXMSIZE))

    def set_empty_star(self):
        self.setPixmap(qta.icon("fa.star-o", color=self.COLOR).pixmap(*self.PXMSIZE))


class C_QLabel(QtGui.QLabel):
    clicked = QtCore.Signal()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        else:
            super(C_QLabel, self).mousePressEvent(event)

class C_QScrollArea(QtGui.QScrollArea):
    def keyPressEvent(self, event):
        key = event.key()
        scrollbar = self.verticalScrollBar()
        if key == QtCore.Qt.Key_Home:
            scrollbar.setValue(scrollbar.minimum())
        elif key == QtCore.Qt.Key_End:
            scrollbar.setValue(scrollbar.maximum())
        else:
            super(C_QScrollArea, self).keyPressEvent(event)


class C_QTextEdit(QtGui.QTextEdit):
    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(C_QTextEdit, self).__init__(parent)
        self.setToolTip("Right click for file browser")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.clicked.emit()
        else:
            super(C_QTextEdit, self).mousePressEvent(event)


class C_QFileDialog(QtGui.QFileDialog):
    def __init__(self, parent=None):
        super(C_QFileDialog, self).__init__(parent)
        self.open_clicked = False
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        #self.setFileMode(self.DirectoryOnly)
        buttons = self.findChildren(QtGui.QPushButton)
        self.openButton = [x for x in buttons if "open" in str(
            x.text()).lower()][0]
        self.openButton.clicked.disconnect()
        self.openButton.clicked.connect(self.openClicked)
        self.tree = self.findChild(QtGui.QTreeView)
        self.setOption(QtGui.QFileDialog.ShowDirsOnly)

    def openClicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
                files.append(os.path.join(str(self.directory().absolutePath()),
                                          str(i.data())))
        self.selectedFiles = files
        self.hide()
        self.open_clicked = True

    def filesSelected(self):
        return self.selectedFiles
