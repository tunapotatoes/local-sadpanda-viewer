#!/usr/bin/python2
from PySide import QtCore, QtGui
import weakref

"""
This shit is why I don't do Qt from hand.
"""


class C_QGallery(QtGui.QFrame):
    def __init__(self, parent=None, gallery=None, **kwargs):
        super(C_QGallery, self).__init__()
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
        self.image = QtGui.QLabel()
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
        self.setLayout(self.gridLayout_2)
        self._gallery = weakref.ref(gallery)
        self.openButton.clicked.connect(self.openFile)
        self.editButton.clicked.connect(self.gallery.customize)
        self.image.setPixmap(QtGui.QPixmap().fromImage(self.gallery.image))
        self.gallery.image = None
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

    def retranslateUi(self):
        # Not planning on translating shit so I'll probably just ax this later
        self.title.setText(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.editButton.setText(QtGui.QApplication.translate("Form", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.rating.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("Form", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.setProperty("class", QtGui.QApplication.translate("Form", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))

    def openFile(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(
            self.gallery.files[0]))

    def _setToolTip(self):
        if self.gallery.tags:
            tooltip = ", ".join(self.gallery.tags)
            tooltip = "<p>" + tooltip + "</p>"
        else:
            tooltip = "No tags found."
        self.setToolTip(tooltip)
