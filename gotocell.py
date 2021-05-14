import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from PySide2.QtWidgets import QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import Qt, QRegExp
from PySide2.QtGui import QRegExpValidator

class GoToCell(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("&Cell Location : ")
        self.lineEdit = QLineEdit()
        self.LimitLineEdit() # 自作関数
        self.label.setBuddy(self.lineEdit)

        self.okButton = QPushButton("&OK")
        self.cancelButton = QPushButton("&Cancel")

        self.okButton.setDefault(True)
        self.okButton.setEnabled(False)
        self.ButtonSetting() # 自作関数


        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.lineEdit)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.okButton)
        self.bottomLayout.addWidget(self.cancelButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Go To Cell")

        self.lineEdit.textChanged.connect(self.On_LineEdit_textChanged)


    def LimitLineEdit(self):
        self.regExp = QRegExp("[A-Za-z][1-9][0-9]")
        self.lineEdit.setValidator(QRegExpValidator(self.regExp, self))

    def ButtonSetting(self):
        self.okButton.clicked.connect(self.accept()) # self.accept()はQDialog内関数
        self.cancelButton.clicked.connect(self.reject()) # self.reject()はQDialog内関数

    def On_LineEdit_textChanged(self):
        self.okButton.setEnabled(not self.lineEdit.text() == "")


    


    

