# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Feb 23 23:00:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from ui.misc import C_QTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 845)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("#MainWindow {\n"
"background: #34353b;\n"
"border: none;\n"
"}\n"
"\n"
"#centralwidget {\n"
"background: #34353b;\n"
"border: none;\n"
"\n"
"}#scrollAreaWidgetContents {\n"
"background: #34353b;\n"
"border: none;\n"
"}")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sidebarFrame = QtGui.QFrame(self.centralwidget)
        self.sidebarFrame.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebarFrame.sizePolicy().hasHeightForWidth())
        self.sidebarFrame.setSizePolicy(sizePolicy)
        self.sidebarFrame.setMinimumSize(QtCore.QSize(150, 0))
        self.sidebarFrame.setMaximumSize(QtCore.QSize(250, 16777215))
        self.sidebarFrame.setAutoFillBackground(False)
        self.sidebarFrame.setStyleSheet("#sidebarFrame {\n"
"background: #4f535b;\n"
"border: 1px solid black;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"     width: 18px;\n"
"     height: 18px;\n"
" }\n"
"\n"
"QFrame.sidebarFrame {\n"
"\n"
"background: #43464e;\n"
"border: 1px solid #34353b;\n"
"border-radius: 9px;\n"
"\n"
"}\n"
"\n"
"QFrame.sidebarFrame QLabel {\n"
"color: #F1F1F1;\n"
"font-weight: bold;\n"
"background: #43464e\n"
"}\n"
"\n"
"QFrame.sidebarFrame QTextEdit {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"font-size: 8pt;\n"
"color: #F1F1F1;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QTextEdit:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QPushButton {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"color: #f1f1f1;\n"
"font-size: 8pt;\n"
"height: 23px;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QPushButton:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QLineEdit {\n"
"background: #34353b;\n"
"color: #F1F1F1;\n"
"border: 1px solid black;\n"
"font-size: 8pt;\n"
"height: 21px;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QLineEdit:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"\n"
"\n"
"QFrame.sidebarFrame QPushButton:hover {\n"
"background: #43464e;\n"
"}\n"
"QFrame.sidebarFrame QCheckBox {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"color: #f1f1f1;\n"
"font-size: 8pt;\n"
"\n"
"height: 21px;\n"
"}\n"
"QFrame.sidebarFrame QComboBox {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"font-size: 8pt;\n"
"height: 21px;\n"
"color: #F1F1F1;\n"
"\n"
"padding: 1px 0px 0px 3px\n"
"\n"
"}\n"
"QFrame.sidebarFrame QComboBox:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"    QComboBox:editable {\n"
"     color: red;\n"
"    }\n"
"\n"
"QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}\n"
"QComboBox QListView {\n"
"        color: #F1F1F1;\n"
"        background-color: #4f535b;\n"
"\n"
"    }\n"
"\n"
"\n"
"QProgressBar:horizontal {\n"
"border: 1px solid black;\n"
"background: #4f535b;\n"
"}\n"
"\n"
"QProgressBar::chunk:horizontal {\n"
"background: #34353b\n"
"}")
        self.sidebarFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.sidebarFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.sidebarFrame.setObjectName("sidebarFrame")
        self.gridLayout_3 = QtGui.QGridLayout(self.sidebarFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_4 = QtGui.QFrame(self.sidebarFrame)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtGui.QLabel(self.frame_4)
        self.label_6.setStyleSheet("\n"
"QFrame.sidebarFrame QLabel {\n"
"\n"
"font-weight: normal;\n"
"\n"
"}\n"
"")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.memberId = QtGui.QLineEdit(self.frame_4)
        self.memberId.setText("")
        self.memberId.setObjectName("memberId")
        self.verticalLayout_6.addWidget(self.memberId)
        self.gridLayout_4.addLayout(self.verticalLayout_6, 1, 0, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_7 = QtGui.QLabel(self.frame_4)
        self.label_7.setStyleSheet("\n"
"QFrame.sidebarFrame QLabel {\n"
"\n"
"font-weight: normal;\n"
"\n"
"}\n"
"")
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.passHash = QtGui.QLineEdit(self.frame_4)
        self.passHash.setText("")
        self.passHash.setObjectName("passHash")
        self.verticalLayout_7.addWidget(self.passHash)
        self.gridLayout_4.addLayout(self.verticalLayout_7, 2, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setMinimumSize(QtCore.QSize(50, 23))
        self.cancelButton.setMaximumSize(QtCore.QSize(16777215, 23))
        self.cancelButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_7.addWidget(self.cancelButton)
        self.submitButton = QtGui.QPushButton(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setMinimumSize(QtCore.QSize(50, 23))
        self.submitButton.setMaximumSize(QtCore.QSize(16777215, 23))
        self.submitButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.submitButton.setObjectName("submitButton")
        self.horizontalLayout_7.addWidget(self.submitButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_8 = QtGui.QLabel(self.frame_4)
        self.label_8.setStyleSheet("\n"
"QFrame.sidebarFrame QLabel {\n"
"\n"
"font-weight: normal;\n"
"\n"
"}\n"
"")
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.directories = C_QTextEdit(self.frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directories.sizePolicy().hasHeightForWidth())
        self.directories.setSizePolicy(sizePolicy)
        self.directories.setMaximumSize(QtCore.QSize(16777215, 50))
        self.directories.setObjectName("directories")
        self.verticalLayout_5.addWidget(self.directories)
        self.gridLayout_4.addLayout(self.verticalLayout_5, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame_4)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_4, 4, 0, 1, 1)
        self.frame_5 = QtGui.QFrame(self.sidebarFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 100000))
        self.frame_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_5 = QtGui.QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pageBox = QtGui.QComboBox(self.frame_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageBox.sizePolicy().hasHeightForWidth())
        self.pageBox.setSizePolicy(sizePolicy)
        self.pageBox.setMaximumSize(QtCore.QSize(16777215, 16777210))
        self.pageBox.setEditable(False)
        self.pageBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.pageBox.setIconSize(QtCore.QSize(0, 0))
        self.pageBox.setFrame(True)
        self.pageBox.setObjectName("pageBox")
        self.pageBox.addItem("")
        self.pageBox.addItem("")
        self.pageBox.addItem("")
        self.pageBox.addItem("")
        self.pageBox.addItem("")
        self.gridLayout_5.addWidget(self.pageBox, 1, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.frame_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 1, 1, 1)
        self.pageLabel = QtGui.QLabel(self.frame_5)
        self.pageLabel.setObjectName("pageLabel")
        self.gridLayout_5.addWidget(self.pageLabel, 1, 3, 1, 1)
        self.label_10 = QtGui.QLabel(self.frame_5)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 5)
        self.navButton = QtGui.QPushButton(self.frame_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navButton.sizePolicy().hasHeightForWidth())
        self.navButton.setSizePolicy(sizePolicy)
        self.navButton.setMinimumSize(QtCore.QSize(50, 23))
        self.navButton.setMaximumSize(QtCore.QSize(16777215, 23))
        self.navButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.navButton.setObjectName("navButton")
        self.gridLayout_5.addWidget(self.navButton, 1, 5, 1, 1)
        self.gridLayout_3.addWidget(self.frame_5, 1, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(self.sidebarFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.refBox = QtGui.QCheckBox(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refBox.sizePolicy().hasHeightForWidth())
        self.refBox.setSizePolicy(sizePolicy)
        self.refBox.setObjectName("refBox")
        self.verticalLayout_2.addWidget(self.refBox)
        self.metaBox = QtGui.QCheckBox(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.metaBox.sizePolicy().hasHeightForWidth())
        self.metaBox.setSizePolicy(sizePolicy)
        self.metaBox.setChecked(False)
        self.metaBox.setObjectName("metaBox")
        self.verticalLayout_2.addWidget(self.metaBox)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.refreshButton = QtGui.QPushButton(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setMinimumSize(QtCore.QSize(50, 23))
        self.refreshButton.setMaximumSize(QtCore.QSize(16777215, 23))
        self.refreshButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_4.addWidget(self.refreshButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout_3.addWidget(self.frame_3, 3, 0, 1, 1)
        self.statusFrame = QtGui.QFrame(self.sidebarFrame)
        self.statusFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.statusFrame.setFrameShadow(QtGui.QFrame.Plain)
        self.statusFrame.setObjectName("statusFrame")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.statusFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtGui.QLabel(self.statusFrame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.progressBar = QtGui.QProgressBar(self.statusFrame)
        self.progressBar.setMinimum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.gridLayout_3.addWidget(self.statusFrame, 6, 0, 1, 1)
        self.frame = QtGui.QFrame(self.sidebarFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchLine = QtGui.QLineEdit(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLine.sizePolicy().hasHeightForWidth())
        self.searchLine.setSizePolicy(sizePolicy)
        self.searchLine.setObjectName("searchLine")
        self.horizontalLayout.addWidget(self.searchLine)
        self.searchButton = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(50, 23))
        self.searchButton.setMaximumSize(QtCore.QSize(16777215, 23))
        self.searchButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.searchButton.setAutoDefault(False)
        self.searchButton.setDefault(False)
        self.searchButton.setFlat(False)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.sidebarFrame, 0, 0, 1, 1)
        self.scrollFrame = QtGui.QFrame(self.centralwidget)
        self.scrollFrame.setStyleSheet("#scrollFrame {\n"
"background: #4f535b;\n"
"border: 1px solid black;\n"
"}\n"
"")
        self.scrollFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.scrollFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.scrollFrame.setObjectName("scrollFrame")
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtGui.QScrollArea(self.scrollFrame)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setMaximumSize(QtCore.QSize(16777209, 16777215))
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setStyleSheet("#scrollArea {\n"
"background: #4f535b;\n"
"border: none\n"
"}\n"
"\n"
"QScrollBar:vertical {               \n"
"        border: 1px solid black;\n"
"        background: #4f535b;\n"
"        width:10px;    \n"
"        margin: 0px 0px 0px 0px;\n"
"    }\n"
"    QScrollBar::handle:vertical {\n"
"        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop: 0  #34353b, stop: 0.5 #34353b, stop:1 #34353b);\n"
"        min-height: 0px;\n"
"    \n"
"    }\n"
"    QScrollBar::add-line:vertical {\n"
"        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop: 0  #34353b, stop: 0.5 #34353b, stop:1 #34353b);\n"
"            height: px;\n"
"        subcontrol-position: bottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"    QScrollBar::sub-line:vertical {\n"
"        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop: 0  #34353b, stop: 0.5 #34353b, stop:1 #34353b);\n"
"        height: 0px;\n"
"        subcontrol-position: top;\n"
"    }\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{\n"
"     background: none;\n"
"}\n"
"\n"
"\n"
"\n"
"QToolTip {\n"
"color: #F1F1F1;\n"
"border: 1px solid black;\n"
"background: #34353b;\n"
"min-height: 19;\n"
"}\n"
"\n"
"QFrame.sidebarFrame {\n"
"\n"
"background: #43464e;\n"
"border: 1px solid #34353b;\n"
"border-radius: 9px;\n"
"\n"
"}\n"
"\n"
"QFrame.sidebarFrame QLabel {\n"
"color: #F1F1F1;\n"
"font-weight: bold;\n"
"background: #43464e\n"
"}\n"
"\n"
"QFrame.sidebarFrame QTextEdit {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"font-size: 8pt;\n"
"color: #F1F1F1;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QTextEdit:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QPushButton {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"color: #f1f1f1;\n"
"font-size: 8pt;\n"
"height: 23px;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QPushButton:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QLineEdit {\n"
"background: #34353b;\n"
"color: #F1F1F1;\n"
"border: 1px solid black;\n"
"font-size: 8pt;\n"
"height: 21px;\n"
"}\n"
"\n"
"QFrame.sidebarFrame QLineEdit:hover {\n"
"background: #43464e;\n"
"}\n"
"\n"
"\n"
"\n"
"QFrame.sidebarFrame QPushButton:hover {\n"
"background: #43464e;\n"
"}\n"
"QFrame.sidebarFrame QCheckBox {\n"
"background: #34353b;\n"
"border: 1px solid black;\n"
"color: #f1f1f1;\n"
"font-size: 8pt;\n"
"height: 21px;\n"
"}\n"
"\n"
"QProgressBar:horizontal {\n"
"border: 1px solid black;\n"
"background: #4f535b;\n"
"}\n"
"\n"
"QProgressBar::chunk:horizontal {\n"
"background: #34353b\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 814, 807))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.scrollFrame, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.searchLine, QtCore.SIGNAL("returnPressed()"), self.searchButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.searchLine, self.searchButton)
        MainWindow.setTabOrder(self.searchButton, self.refBox)
        MainWindow.setTabOrder(self.refBox, self.metaBox)
        MainWindow.setTabOrder(self.metaBox, self.refreshButton)
        MainWindow.setTabOrder(self.refreshButton, self.memberId)
        MainWindow.setTabOrder(self.memberId, self.passHash)
        MainWindow.setTabOrder(self.passHash, self.directories)
        MainWindow.setTabOrder(self.directories, self.cancelButton)
        MainWindow.setTabOrder(self.cancelButton, self.submitButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SadPanda Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_4.setProperty("class", QtGui.QApplication.translate("MainWindow", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Member ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setProperty("class", QtGui.QApplication.translate("MainWindow", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Password Hash", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setProperty("class", QtGui.QApplication.translate("MainWindow", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.submitButton.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Folders  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setProperty("class", QtGui.QApplication.translate("MainWindow", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.directories.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_5.setProperty("class", QtGui.QApplication.translate("MainWindow", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.pageBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.pageBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.pageBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.pageBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.pageBox.setItemText(4, QtGui.QApplication.translate("MainWindow", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Page", None, QtGui.QApplication.UnicodeUTF8))
        self.pageLabel.setText(QtGui.QApplication.translate("MainWindow", "of N", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Navigation", None, QtGui.QApplication.UnicodeUTF8))
        self.navButton.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_3.setProperty("class", QtGui.QApplication.translate("MainWindow", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Gallery Options", None, QtGui.QApplication.UnicodeUTF8))
        self.refBox.setText(QtGui.QApplication.translate("MainWindow", "Search directories for galleries", None, QtGui.QApplication.UnicodeUTF8))
        self.metaBox.setText(QtGui.QApplication.translate("MainWindow", "Get metadata for new galleries", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.statusFrame.setProperty("class", QtGui.QApplication.translate("MainWindow", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.frame.setProperty("class", QtGui.QApplication.translate("MainWindow", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("MainWindow", "Submit", None, QtGui.QApplication.UnicodeUTF8))

