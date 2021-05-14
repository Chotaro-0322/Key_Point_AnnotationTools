from PySide2.QtGui import QImage, QPixmap, QBrush, QColor
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide2.QtCore import QRectF, Qt

from spreadsheet import *

import cv2
import glob


class GraphicsWindow(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        print('you in the GraphicsWindow')

        self.count = 0

        self.scene_class = Graphics_scene()
        self.setScene(self.scene_class)

        self.update_view()

        self.table = self.scene_class.spreadsheet.table
        self.table.cellClicked.connect(self.cellClicked)


    def update_view(self):
        if self.count < self.scene_class.Imagelimit:
            #print(self.count)
            self.count_UP()
            self.Show_Image()
        

    def prev_view(self):
        if self.count > 1:
            self.count_DOWN()
            self.Show_Image()
        
    def Show_Image(self):
        print('show_Image')
        self.imgpass = './IMAGE/{}.jpg'.format(self.count)
        self.Image = QImage(self.imgpass)

        color = QColor()
        color.setRgb(0, 0, 255, a=255)
        joint_list = self.take_joint()
        if joint_list:
            #print('joint_listは存在する', joint_list)
            for joint in joint_list:
                if joint != '':
                    jointx, jointy = joint.split(',')
                    jointx, jointy = int(float(jointx)), int(float(jointy))
                    for x in range(jointx-4, jointx +5):
                        self.Image.setPixelColor(x, jointy-1, color)
                        self.Image.setPixelColor(x, jointy, color)
                        self.Image.setPixelColor(x, jointy+1, color)
                        for y in range(jointy - 4, jointy + 5):
                            self.Image.setPixelColor(jointx-1, y, color)
                            self.Image.setPixelColor(jointx, y, color)
                            self.Image.setPixelColor(jointx+1, y, color)
                else:
                    continue
        else:
            pass
        self.image_item = QGraphicsPixmapItem(QPixmap(self.Image))

        self.scene().clear()
        self.scene().addItem(self.image_item)

        self.height, self.width, _  = (cv2.imread(self.imgpass)).shape
        self.setFixedSize(self.width, self.height)
        #print('width, height', self.width, self.height)

        return self


    def count_UP(self):
        self.count += 1

    def count_DOWN(self):
        self.count -= 1

    def take_joint(self):
        #print('take_joint')
        joint_list = []
        print('next_csv is ', self.scene_class.spreadsheet.next_csv)
        for row in range(100):
            for column in range(18):
                #print('text is ', self.scene_class.spreadsheet.table.item(row, column).text())
                try:
                    joint_list.append(self.scene_class.spreadsheet.table.item(row, column).text())
                except AttributeError:
                    joint_list.append('')
        # print(joint_list)
        return joint_list

    def mouseReleaseEvent(self, event):
        print('view の中でクリックを検知しました')
        print(type(event))
        self.scene_class.mouseReleaseEvent(event)
        self.Show_Image()


    def cellClicked(self):
        print('cell is clicked')
        self.tableRow, self.tableColumn = self.table.currentRow(), self.table.currentColumn()
        print('row, column', self.tableRow, self.tableColumn)
        self.scene_class.spreadsheet.control.humancombo.setCurrentIndex(self.tableRow)
        self.scene_class.spreadsheet.control.jointcombo.setCurrentIndex(self.tableColumn)

        self.Show_Image()

        coord = self.table.currentItem().text()
        print('coord is ', coord)
        color = QColor()
        color.setRgb(255, 0, 0, a=255)
        if coord:
            jointx, jointy = coord.split(',')
            jointx, jointy = int(jointx), int(jointy)
            for x in range(jointx-6, jointx +7):
                self.Image.setPixelColor(x, jointy-1, color)
                self.Image.setPixelColor(x, jointy, color)
                self.Image.setPixelColor(x, jointy+1, color)
                for y in range(jointy - 6, jointy + 7):
                    self.Image.setPixelColor(jointx-1, y, color)
                    self.Image.setPixelColor(jointx, y, color)
                    self.Image.setPixelColor(jointx+1, y, color)

        self.image_item = QGraphicsPixmapItem(QPixmap(self.Image))
        self.scene().addItem(self.image_item)

        


class Graphics_scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Imagelist = glob.glob('IMAGE/*.jpg')
        self.Imagelimit = len(self.Imagelist)
        print(self.Imagelist)
        self.spreadsheet = SpreadSheet(100, 18, self.Imagelimit)
        # print('self.spreadsheetに入った後')
        
        
    def mouseReleaseEvent(self, event):
        x, y, = self.getMousePos(event)
        self.spreadsheet.joint_mouseEvent(x, y)
        print(type(event))
        print(x, y)

    def getMousePos(self, event):
        #x = event.scenePos().x()
        #y = event.scenePos().y()
        x = event.pos().x()
        y = event.pos().y()
        return x, y



if __name__ == '__main__':
    import sys
    app = qtw.QApplication(sys.argv)
    w = GraphicsWindow()
    w.update_view()
    #w.update_view()
    w.show()
    sys.exit(app.exec_())
