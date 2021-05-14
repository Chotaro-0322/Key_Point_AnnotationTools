import sys
import os
import csv
import glob

from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg, QtCharts)

from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QMessageBox, QApplication
from PySide2.QtCore import QFile, QIODevice, QTextStream, QDataStream
from PySide2.QtGui import QGuiApplication

from controlbox import *


class SpreadSheet(QTableWidget):
    def __init__(self, rows, cols, Imagelimit,  parent=None):
        super().__init__(parent)

        self.control = ControlBox()

        #print('Spread sheet is active')
        self.rows = rows
        self.cols = cols
        self.Image_limit = Imagelimit
        self.table = QTableWidget(self.rows, self.cols, self)

        self.count = 0

        self.jointname = ['0. nose', '1.neck', '2.Right shoulder', "3.Right elbow", "4.Right hand", "5.Left shoulder", "6.Left elbow",
                                    "7.Left hand", "8.Right hip", "9.Right knee", "10.Right foot", "11.Left hip", "12.Left knee", "13.Left foot",
                                    "14.Right eye", "15.Left eye", "16.Right ear", "17.Left ear"]

        self.update_table()

    def update_table(self):
        if self.count < self.Image_limit:
            if not self.count == 0:
                self.Save_table()
            self.count_UP()
            self.Show_table()

    def prev_table(self):
        if self.count > 1:
            if not self.count == 0:
                self.Save_table()
            self.count_DOWN()
            self.Show_table()

    def Show_table(self):

        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        for c, joint in enumerate(self.jointname):
            self.table.setHorizontalHeaderItem(c, QTableWidgetItem(joint))

        self.next_csv = './Joint_csv/{}.csv'.format(self.count)
        human_num = [] # ???csv?????????????????????????????????????

        if not os.path.exists(self.next_csv):
            print('You dont have next_csv')
            with open(self.next_csv, 'w') as f:
                writer = csv.writer(f)
        else:
            print('csv is activate', self.next_csv)
            with open(self.next_csv) as f_read:
                reader = csv.reader(f_read)
                reader_list = [row for row in reader]
                for rindex, row in enumerate(reader_list):
                    #print('reader_list is ', rindex, row, '\n')
                    if row:
                        human_num.append(rindex) # csv???????????????????????????
                    for cindex, column in enumerate(row):
                        self.table.setItem(rindex, cindex, QTableWidgetItem(column))

        print('human_num is', human_num)
        self.control.humancombo.clear()
        if human_num:
            for i in human_num:
                self.control.humancombo.addItem(str(i + 1))
        else:
            print('else of human_num')
            self.control.humancombo.addItem('1')
        
        return self

    def Save_table(self):
        print('spreadsheet is saved')
        self.pre_csv = './Joint_csv/{}.csv'.format(self.count)
        print('save to', self.pre_csv)
        with open(self.pre_csv, 'w') as f_out:
            writer = csv.writer(f_out, lineterminator = '\n')
            for row in range(self.rows):
                row_data = []
                for column in range(self.cols):
                    try:
                        item = self.table.item(row, column).text()
                        #print('item is', item)
                        row_data.append(item)
                    except AttributeError:
                        row_data.append('')
                #print('row_data is ', row_data)
                writer.writerow(row_data)
        return self


    def count_UP(self):
        self.count += 1
        self.table.clear()

    def count_DOWN(self):
        self.count -= 1
        self.table.clear()


    def joint_mouseEvent(self, x, y):
        #print('You enter the joint_mouseEvent / mouse coord is ', x, y)
        self.coord = str(x) + ',' + str(y)
        #print(self.coord)
        self.joint_row = self.control.jointcombo.currentIndex()
        self.joint_column = int(self.control.humancombo.currentText()) - 1
        #print(self.joint_row)
        #print(self.joint_column)
        #print('Youre going to insert coord  ', self.joint_row, self.joint_column)
        self.table.setItem(self.joint_column, self.joint_row , QTableWidgetItem(self.coord))


if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    w = SpreadSheet()
    w.update_table()
    w.show()
    sys.exit(app.exec_())
