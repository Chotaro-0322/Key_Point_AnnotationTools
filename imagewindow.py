from PySide2.QtGui import QImage, QPixmap, QBrush
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide2.QtCore import QRectF, Qt

import cv2
import glob

class GraphicsArea(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Imagelist = glob.glob('IMAGE/*.jpg')
        #print('読み込まれた画像のリストは', self.Imagelist)
        
        self.image_item = QGraphicsPixmapItem(QPixmap(QImage(self.Imagelist[0])))
        self.height, self.width, _  = (cv2.imread(self.Imagelist[0])).shape
        self.current = self.Imagelist[0]
        self.addItem(self.image_item)
        self.setBackgroundBrush(QBrush(Qt.black))

    def mousePressEvent(self, event):
        x, y, = self.getMousePos(event)
        print(x, y)

    def getMousePos(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        return x, y

    def nextImage(self):
        #print("nextImageに入りました")
        #self.clear()
        print('self.currentは', self.current)
        self.current_imagenum = self.Imagelist.index(self.current)
        print('今見ている画像の番号は', self.current_imagenum)

        self.next_image = self.Imagelist[self.current_imagenum + 1]
        print('次の画像は', self.next_image)
        
        self.current = self.next_image
        print('self.currentは', self.current)

        self.next_item = QGraphicsPixmapItem(QPixmap(QImage(self.next_image)))
        #print(self.next_item)
        self.height, self.width, _  = (cv2.imread(self.next_image)).shape
        #print(self.height)

        self.addItem(self.next_item)
        self.setBackgroundBrush(QBrush(Qt.black))
        #print('nextimage内のselfは', self)

        return self



class GraphicsWindow(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        scene = GraphicsArea(self)
        print('sceneは',scene)
        self.setFixedSize(scene.width+5, scene.height+5)

        self.setScene(scene)
        self.show()

    def next_update(self):
        print('次の画像へ移動します')
        scene = GraphicsArea(self).nextImage()
        print(scene)
        self.setFixedSize(scene.width+5, scene.height+5)

        self.setScene(scene)
        self.show()
