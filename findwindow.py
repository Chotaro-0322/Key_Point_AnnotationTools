import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from PySide2.QtWidgets import QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import Qt


class FindDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("Find &what : ")
        self.lineEdit = QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.caseCheckBox = QCheckBox("&Match & case")
        self.backwardCheckBox = QCheckBox("Search &backward")

        self.findButton = QPushButton("&find")
        self.findButton.setDefault(True)
        self.findButton.setEnabled(False)

        self.closeButton = QPushButton("&close")


        self.lineEdit.textChanged.connect(self.enableFindButton)
        self.findButton.clicked.connect(self.findClicked)
        self.closeButton.clicked.connect(self.close)

        self.topLeftLayout = QHBoxLayout()
        self.topLeftLayout.addWidget(self.label)
        self.topLeftLayout.addWidget(self.lineEdit)
        
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addLayout(self.topLeftLayout)
        self.leftLayout.addWidget(self.caseCheckBox)
        self.leftLayout.addWidget(self.backwardCheckBox)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.findButton)
        self.rightLayout.addWidget(self.closeButton)
        self.rightLayout.addStretch()

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.setLayout(self.mainLayout)


        self.setWindowTitle("Find")
        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


    def findClicked(self):
        self.cs = Qt.CaseSensitivity()
        if self.cs == self.caseCheckBox.isChecked():
            self.cs = Qt.CaseSensitivity
        else:
            self.cs = Qt.CaseInsensitive

        if self.backwardCheckBox.isChecked():
            self.findPrevious(self.text, self.cs)
        else:
            self.findNext(self.text, self.cs)
        
    def enableFindButton(self):
        self.text = self.lineEdit.text()
        print(self.text)
        self.findButton.setEnabled(not self.text == "")

            

