#!/usr/bin/python2
from PySide import QtCore, QtGui
import ui.misc
import weakref

"""
This shit is why I don't do Qt from hand.
"""


class C_QGallery(QtGui.QFrame):
    def __init__(self, parent=None, gallery=None, **kwargs):
        super(C_QGallery, self).__init__()
        self.parent = parent
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setWordWrap(True)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.image = ui.misc.C_QLabel()
        self.image.setObjectName("image")
        self.horizontalLayout_4.addWidget(self.image)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.editButton = QtGui.QPushButton()
        self.editButton.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy)
        self.editButton.setMinimumSize(QtCore.QSize(50, 23))
        self.editButton.setMaximumSize(QtCore.QSize(50, 23))
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_2.addWidget(self.editButton)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.rating = QtGui.QLabel()
        self.rating.setAlignment(QtCore.Qt.AlignCenter)
        self.rating.setObjectName("rating")
        self.horizontalLayout_3.addWidget(self.rating)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.openButton = QtGui.QPushButton()
        self.openButton.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openButton.sizePolicy().hasHeightForWidth())
        self.openButton.setSizePolicy(sizePolicy)
        self.openButton.setMinimumSize(QtCore.QSize(50, 23))
        self.openButton.setMaximumSize(QtCore.QSize(50, 23))
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.retranslateUi()
        # My manual stuff:
        #self.setContentsMargins(9, 9, 9, 9)
        self.gallery = gallery
        self.setLayout(self.gridLayout_2)
        self.openButton.clicked.connect(self.gallery.open_file)
        self.editButton.clicked.connect(self.gallery.customize)
        self.image.clicked.connect(self.gallery.open_file)
        self.update()
        self.setFixedSize(250, 400)
        #self.hide()

    def update(self):
        self.title.setText(self.gallery.title)
        self.rating.setText("Rating: %s" % self.gallery.rating)
        self._setToolTip()

    @property
    def gallery(self):
        return self._gallery()

    @gallery.setter
    def gallery(self, val):
        self._gallery = weakref.ref(val)

    def set_image(self):
        self.image.setPixmap(QtGui.QPixmap().fromImage(self.gallery.image))
        self.gallery.image = None

    def contextMenuEvent(self, *args, **kwargs):
        menu = QtGui.QMenu(self.parent)
        open_action = QtGui.QAction("Open", self)
        open_action.triggered.connect(self.gallery.open_file)
        menu.addAction(open_action)
        edit_action = QtGui.QAction("Edit", self)
        edit_action.triggered.connect(self.gallery.customize)
        menu.addAction(edit_action)
        view_in_folder_action = QtGui.QAction("View folder", self)
        view_in_folder_action.triggered.connect(self.gallery.open_folder)
        menu.addAction(view_in_folder_action)
        if self.gallery.gid:
            open_on_ex_action = QtGui.QAction("View on EX", self)
            open_on_ex_action.triggered.connect(self.gallery.open_on_ex)
            menu.addAction(open_on_ex_action)
        else:
            search_action = QtGui.QAction("Search for metadata", self)
            search_action.triggered.connect(self.gallery.get_metadata)
            menu.addAction(search_action)
        menu.popup(QtGui.QCursor.pos())

    def retranslateUi(self):
        # Not planning on translating shit so I'll probably just ax this later
        self.title.setText(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.editButton.setText(QtGui.QApplication.translate("Form", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.rating.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("Form", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.setProperty("class", QtGui.QApplication.translate("Form", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))

    def _setToolTip(self):
        if self.gallery.read_count == 1:
            tooltip = "Read %s time"
        else:
            tooltip = "Read %s times"
        tooltip = tooltip % self.gallery.read_count
        if self.gallery.last_read:
            tooltip += "<br/>Last read on %s" % self.gallery.local_last_read_time
        if self.gallery.tags:
            tooltip += "<br />Tags: " + ", ".join(self.gallery.tags)[:-2]
        tooltip = "<p>" + tooltip + "</p>"
        self.setToolTip(tooltip)
