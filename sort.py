import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from PySide2.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox, QComboBox
from PySide2.QtCore import Qt

class Sort(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.defaultbool = None

        self.FirstBox = createGroupBox().createBox(name="Primary")
        self.SecondaryBox = createGroupBox().createBox(name="Secondary")
        self.TertiaryBox = createGroupBox().createBox(name="Tertiary")

        self.SecondaryBox.setVisible(False)
        self.TertiaryBox.setVisible(False)

        self.grid = QGridLayout()
        self.grid.addWidget(self.FirstBox, 0, 0)
        self.grid.addWidget(self.SecondaryBox, 1, 0)
        self.grid.addWidget(self.TertiaryBox, 2, 0)
        self.grid.addLayout(self.createButton(), 0, 1)

        self.setWindowTitle("Sort")
        self.setLayout(self.grid)

        self.moreButton.clicked.connect(self.Boxvisible)
        

    def createButton(self):
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.moreButton = QPushButton("&More")

        self.buttonArea = QVBoxLayout()
        self.buttonArea.addWidget(self.okButton)
        self.buttonArea.addWidget(self.cancelButton)
        self.buttonArea.addWidget(self.moreButton)

        return self.buttonArea

    def Boxvisible(self):
        if (not self.defaultbool) | (self.defaultbool != True):
            self.SecondaryBox.setVisible(True)
            self.TertiaryBox.setVisible(True)
            self.defaultbool = True
            self.adjustSize()
        else:
            self.SecondaryBox.setVisible(False)
            self.TertiaryBox.setVisible(False)
            self.defaultbool = False
            self.adjustSize()
            
class createGroupBox(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createBox(self, name=None):
        self.groupBox = QGroupBox("{} Key".format(name))

        self.label1 = QLabel("Column : ")
        self.label2 = QLabel("Order : ")

        self.ColumnBox = QComboBox()
        self.ColumnBox.addItem("None")

        self.OrderBox = QComboBox()
        self.OrderBox.addItem("Ascending")
        self.OrderBox.addItem("Descending")

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.label1)
        self.topLayout.addWidget(self.ColumnBox)

        self.botLayout = QHBoxLayout()
        self.botLayout.addWidget(self.label2)
        self.botLayout.addWidget(self.OrderBox)

        self.Vbox = QVBoxLayout()
        self.Vbox.addLayout(self.topLayout)
        self.Vbox.addLayout(self.botLayout)
        self.groupBox.setLayout(self.Vbox)

        return self.groupBox


    
