#!/usr/bin/env python

import os
from PySide import QtCore, QtGui
import qtawesome as qta


class CQLockButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        super(CQLockButton, self).__init__(parent)
        self.locks = {}

    def set_lock(self, requester):
        self.locks[str(requester)] = True
        self.setEnabled(any([self.locks[l] for l in self.locks]))

    def remove_lock(self, requester):
        self.locks[str(requester)] = False
        self.setEnabled(not any([self.locks[l] for l in self.locks]))


class CQCompleter(QtGui.QCompleter):

    def pathFromIndex(self, index):
        path = super(CQCompleter, self).pathFromIndex(index)
        path_list = str((self.widget().text())).split(" ")
        if len(path_list):
            path = "%s %s" % (" ".join(path_list[:-1]), path)
        return path.lstrip()

    def splitPath(self, path):
        return [str(path.split(" ")[-1])]


class CQOverlayIcon(QtGui.QToolButton):
    SIZE = 100

    def __init__(self, parent=None):
        super(CQOverlayIcon, self).__init__(parent)
        self.parent = parent
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet(
            """
            QToolButton {
            border: 0px;
            background: transparent;
            color: #F1F1F1;
            font-size: 20pt;
            }
            """)
        self.parent = parent
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setIconSize(QtCore.QSize(self.SIZE, self.SIZE))
        self.size_to_parent()
        self.hide()
        self.parent.resized.connect(self.reposition)

    def size_to_parent(self):
        self.resize(self.parent.height(), 150)

    def mousePressEvent(self, event):
        event.accept()

    def reposition(self):
        raise NotImplementedError

class QControlButton(CQOverlayIcon):

    def __init__(self, parent=None, forwards=True):
        super(QControlButton, self).__init__(parent)
        # icon_type = "forward" if forwards else "backward"
        # icon = "fa.%s" % icon_type
        # options = {"color": "#F1F1F1"}
        # self.icon = qta.icon(["fa.square-o", icon], options=[options, options])
        icon_type = "right" if forwards else "left"
        icon = qta.icon("fa.chevron-circle-%s" % icon_type, color="#F1F1F1")

        self.setIcon(icon)

        



class CQSpinner(CQOverlayIcon):

    def __init__(self, parent=None):
        super(CQSpinner, self).__init__(parent)
        self.default_icon = qta.icon("fa.refresh", color="#F1F1F1", animation=qta.Spin(self))
        self.warning_icon = qta.icon("fa.warning", color="#F1F1F1")

    def reposition(self):
        self.size_to_parent()
        self.move(self.parent.width() / 2 - self.width() / 2,
                  self.parent.height() / 2 - self.height() / 2)

    def set_initial_loading(self):
        self.show()
        self.setIcon(self.default_icon)
        self.setText("Please wait while we load your galleries")

    def set_searching_galleries(self):
        self.show()
        self.setIcon(self.default_icon)
        self.setText("Please wait while we search for galleries")

    def set_no_galleries(self):
        self.show()
        self.setIcon(self.warning_icon)
        self.setText("Sorry, no galleries were found.")




class CQStar(QtGui.QLabel):
    COLOR = "#F1F1F1"
    SIZE = 25
    PXMSIZE = (SIZE, SIZE)
    MAX_NUMBER = 5

    def __init__(self, parent, number):
        super(CQStar, self).__init__()
        self.parent = parent
        self.setCursor(QtCore.Qt.PointingHandCursor)
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


class CQGalleryImage(QtGui.QLabel):
    clicked = QtCore.Signal()

    def __init__(self):
        super(CQGalleryImage, self).__init__()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setStyleSheet("border: 1px solid black;")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        else:
            super(CQGalleryImage, self).mousePressEvent(event)

class CQScrollArea(QtGui.QScrollArea):
    resized = QtCore.Signal()

    def keyPressEvent(self, event):
        key = event.key()
        scrollbar = self.verticalScrollBar()
        if key == QtCore.Qt.Key_Home:
            scrollbar.setValue(scrollbar.minimum())
        elif key == QtCore.Qt.Key_End:
            scrollbar.setValue(scrollbar.maximum())
        else:
            super(CQScrollArea, self).keyPressEvent(event)

    def resizeEvent(self, event):
        super(CQScrollArea, self).resizeEvent(event)
        event.accept()
        self.resized.emit()


class CQTextEdit(QtGui.QTextEdit):
    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(CQTextEdit, self).__init__(parent)
        self.setToolTip("Right click for file browser")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.clicked.emit()
        else:
            super(CQTextEdit, self).mousePressEvent(event)


class CQFileDialog(QtGui.QFileDialog):
    def __init__(self, parent=None):
        super(CQFileDialog, self).__init__(parent)
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
