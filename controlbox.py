from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from PySide2.QtWidgets import QLabel, QPushButton, QGridLayout, QComboBox


class ControlBox(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.jointlabel = QLabel("Joint name")
        self.humannum = QLabel("Human number")
        self.mkhuman = QPushButton("Create(&Z)")
        self.rmhuman = QPushButton("Remove(&x)")
        self.joint_next = QPushButton("Next_joint(&A)")
        self.joint_prev = QPushButton("Pre_joint(&S)")
        self.nextButton = QPushButton("Next")
        self.prevButton = QPushButton("Prev")
        
        self.jointcombo = QComboBox()
        self.jointcombo.addItem("0.nose")
        self.jointcombo.addItem("1.neck")
        self.jointcombo.addItem("2.Right shoulder")
        self.jointcombo.addItem("3.Right elbow")
        self.jointcombo.addItem("4.Right hand")
        self.jointcombo.addItem("5.Left shoulder")
        self.jointcombo.addItem("6.Left elbow")
        self.jointcombo.addItem("7.Left hand")
        self.jointcombo.addItem("8.Right hip")
        self.jointcombo.addItem("9.Right knee")
        self.jointcombo.addItem("10.Right foot")
        self.jointcombo.addItem("11.Left hip")
        self.jointcombo.addItem("12.Left knee")
        self.jointcombo.addItem("13.Left foot")
        self.jointcombo.addItem("14.Right eye")
        self.jointcombo.addItem("15.Left eye")
        self.jointcombo.addItem("16.Right ear")
        self.jointcombo.addItem("17.Left ear")


        self.humancombo = QComboBox()
        self.humancombo.addItem("None")

        self.controlBox = self.createMainControl()

        self.mkhuman.clicked.connect(self.add_new_human)
        self.rmhuman.clicked.connect(self.rm_current_human)
        self.joint_next.clicked.connect(self.next_to_joint)
        self.joint_prev.clicked.connect(self.prev_to_joint)

    def createMainControl(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.jointlabel, 0, 0)
        self.grid.addWidget(self.jointcombo, 0, 1)
        self.grid.addWidget(self.joint_next, 0, 2)
        self.grid.addWidget(self.joint_prev, 0, 3)
        self.grid.addWidget(self.humannum, 1, 0)
        self.grid.addWidget(self.humancombo, 1, 1)
        self.grid.addWidget(self.mkhuman, 1, 2)
        self.grid.addWidget(self.rmhuman, 1, 3)
        self.grid.addWidget(self.prevButton, 3, 0, 1, 1)
        self.grid.addWidget(self.nextButton, 3, 1, 1, 1)

        return self.grid

    def add_new_human(self):
        if (self.humancombo.currentText() == 'None') | (self.humancombo.currentText() == ''):
            self.nonenum = self.humancombo.findText('None')
            self.humancombo.removeItem(self.nonenum)
            self.humancombo.addItem('1')
    
        else:
            currentNum = int(self.humancombo.currentText())
            # print(currentNum)
            nextNum = currentNum
            # print('next ', nextNum)
            if nextNum < 100:
                self.humancombo.setCurrentIndex(nextNum)

    def rm_current_human(self):
        nowText = self.humancombo.currentText()
        nowNum = self.humancombo.findText(nowText)
        if nowNum >= 1:
            self.humancombo.setCurrentIndex(nowNum - 1)

    def next_to_joint(self):
        #print('現在のコンボindex', self.jointcombo.currentIndex())
        next_combo = self.jointcombo.currentIndex() + 1
        #print('次のコンボ', next_combo)
        if next_combo < 18:
            self.jointcombo.setCurrentIndex(next_combo)

    def prev_to_joint(self):
        #print('現在のコンボindex', self.jointcombo.currentIndex())
        prev_combo = self.jointcombo.currentIndex() - 1
        #print('前のコンボ', prev_combo)
        if prev_combo >= 0:
            self.jointcombo.setCurrentIndex(prev_combo)

        
        

    



         

