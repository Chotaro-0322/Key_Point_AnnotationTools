import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from findwindow import *
from gotocell import *
from sort import *
from imagewindow import *
from controlbox import *

from PySide2.QtWidgets import QMainWindow, QPlainTextEdit, QAction, QApplication, QFileDialog, QMessageBox
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtCore import Qt, QFile, QFileInfo, QSettings, QTextStream, QPoint, QSize

class SpreadSheet(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = QTableWidget(rows, cols, self)