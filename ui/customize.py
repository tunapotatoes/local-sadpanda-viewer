# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customize.ui'
#
# Created: Sun Feb 15 02:57:01 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(300, 327)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(300, 327))
        Dialog.setMaximumSize(QtCore.QSize(300, 327))
        Dialog.setStyleSheet("")
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainFrame = QtGui.QFrame(Dialog)
        self.mainFrame.setStyleSheet("#mainFrame {\n"
"background: #4f535b;\n"
"border: 1px solid black;\n"
"}\n"
"\n"
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
"")
        self.mainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.mainFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editFrame = QtGui.QFrame(self.mainFrame)
        self.editFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.editFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.editFrame.setObjectName("editFrame")
        self.gridLayout = QtGui.QGridLayout(self.editFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtGui.QLabel(self.editFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtGui.QLabel(self.editFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
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
        self.customTitle = QtGui.QLineEdit(self.editFrame)
        self.customTitle.setText("")
        self.customTitle.setObjectName("customTitle")
        self.verticalLayout_6.addWidget(self.customTitle)
        self.gridLayout.addLayout(self.verticalLayout_6, 1, 0, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_7 = QtGui.QLabel(self.editFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
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
        self.customTags = QtGui.QLineEdit(self.editFrame)
        self.customTags.setText("")
        self.customTags.setObjectName("customTags")
        self.verticalLayout_7.addWidget(self.customTags)
        self.gridLayout.addLayout(self.verticalLayout_7, 2, 0, 1, 1)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtGui.QLabel(self.editFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setStyleSheet("\n"
"QFrame.sidebarFrame QLabel {\n"
"\n"
"font-weight: normal;\n"
"\n"
"}\n"
"")
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.customRating = QtGui.QLineEdit(self.editFrame)
        self.customRating.setText("")
        self.customRating.setObjectName("customRating")
        self.verticalLayout_9.addWidget(self.customRating)
        self.gridLayout.addLayout(self.verticalLayout_9, 3, 0, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtGui.QLabel(self.editFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setStyleSheet("\n"
"QFrame.sidebarFrame QLabel {\n"
"\n"
"font-weight: normal;\n"
"\n"
"}\n"
"")
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.exhentaiURL = QtGui.QLineEdit(self.editFrame)
        self.exhentaiURL.setText("")
        self.exhentaiURL.setObjectName("exhentaiURL")
        self.verticalLayout_8.addWidget(self.exhentaiURL)
        self.gridLayout.addLayout(self.verticalLayout_8, 4, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.editFrame)
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
        self.submitButton = QtGui.QPushButton(self.editFrame)
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
        self.gridLayout.addLayout(self.horizontalLayout_7, 5, 0, 1, 1)
        self.horizontalLayout.addWidget(self.editFrame)
        self.verticalLayout.addWidget(self.mainFrame)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.customTitle, QtCore.SIGNAL("returnPressed()"), self.submitButton.click)
        QtCore.QObject.connect(self.customTags, QtCore.SIGNAL("returnPressed()"), self.submitButton.click)
        QtCore.QObject.connect(self.exhentaiURL, QtCore.SIGNAL("returnPressed()"), self.submitButton.click)
        QtCore.QObject.connect(self.customRating, QtCore.SIGNAL("returnPressed()"), self.submitButton.click)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Customize", None, QtGui.QApplication.UnicodeUTF8))
        self.editFrame.setProperty("class", QtGui.QApplication.translate("Dialog", "sidebarFrame", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Customize", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Custom Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setProperty("class", QtGui.QApplication.translate("Dialog", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Custom Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setProperty("class", QtGui.QApplication.translate("Dialog", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Custom Rating", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setProperty("class", QtGui.QApplication.translate("Dialog", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "ExHentai URL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setProperty("class", QtGui.QApplication.translate("Dialog", "smallText", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.submitButton.setText(QtGui.QApplication.translate("Dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))

