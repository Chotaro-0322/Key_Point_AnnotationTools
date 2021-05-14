from mainwindow2 import *
from findwindow import *
from gotocell import *
from sort import *
from controlbox import *
#from spreadsheet import *

import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)

app = qtw.QApplication(sys.argv)
mw = MainWindow()

mw.show()
sys.exit(app.exec_())

