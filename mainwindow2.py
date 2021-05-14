import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
from findwindow import *
from gotocell import *
from sort import *
from imagewindow_ver2 import *
#from controlbox import *
#from spreadsheet import *

from PySide2.QtWidgets import QMainWindow, QPlainTextEdit, QAction, QApplication, QFileDialog, QMessageBox
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtCore import Qt, QFile, QFileInfo, QSettings, QTextStream, QPoint, QSize

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.textEdit = QPlainTextEdit()
        self.curFile = ""

        self.centralWidget = qtw.QWidget()
        self.mainWindow = self.createMainWindow()
        self.centralWidget.setLayout(self.mainWindow)

        self.setCentralWidget(self.centralWidget)
        #self.setFixedSize(1000, 550)
        
        self.createActions()
        self.createMenus()
        #self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.textEdit.document().contentsChanged.connect(self.documentWasModified)

        #self.setCurrentFile("")
        self.setUnifiedTitleAndToolBarOnMac(True)

        #self.menuBar = qtw.QLayout.menuBar()
        #self.statusBar = qtw.QMainWindow.statusBar()
        self.Qsettings = QSettings()

        #self.connectlist()

    def createMainWindow(self):

        self.graphics = GraphicsWindow()
        self.spreadsheet = self.graphics.scene_class.spreadsheet
        self.control = self.spreadsheet.control

        self.controlobj = self.control.controlBox

        self.control.nextButton.clicked.connect(self.spreadsheet.update_table)
        self.control.nextButton.clicked.connect(self.graphics.update_view)
        
        self.control.prevButton.clicked.connect(self.spreadsheet.prev_table)
        self.control.prevButton.clicked.connect(self.graphics.prev_view)

        self.righttop = QVBoxLayout()
        self.righttop.addLayout(self.controlobj)
        self.righttop.addWidget(self.spreadsheet.table)

        self.mainWin = QHBoxLayout()
        self.mainWin.addWidget(self.graphics)
        self.mainWin.addLayout(self.righttop)

        return self.mainWin
    
    def closeEvent(self, event):
        if self.maybeSave:
            self.writeSettings
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        if self.maybeSave:
            self.textEdit.clear()
            self.setCurrentFile("")

    def open(self):
        if self.maybeSave:
            fileName = QFileDialog.getOpenFileName(self)
            if not fileName.isEmpty():
                self.loadFile(fileName)

    def save(self):
        if self.curFile == "":
            return self.saveAs

        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName = QFileDialog.getSaveFileName(self)
        if fileName.isEmpty():
            return False
        
        return self.saveFile(fileName)

    def about(self):
        QMessageBox.about(self, "About Application\n", 
                                                "The <b>Application</b> example demonstrates how to\n"
                                                "write modern GUI applications using Qt, With a menu bar\n"
                                                "toolbars, and a status bar.")

    def documentWasModified(self):
        self.setWindowModified(self.textEdit.document().isModified())

    
    
    def createActions(self):
        self.Act = QAction(QIcon(":/images/new.png"), "&New", self)
        self.Act.setShortcuts(QKeySequence.New)
        self.Act.setStatusTip("Create a new file")
        self.Act.triggered.connect(self.newFile)

        self.openAct = QAction(QIcon(":/images/new.png"), "&Open", self)
        self.openAct.setShortcuts(QKeySequence.Open)
        self.openAct.setStatusTip("Open an exsting file")
        self.openAct.triggered.connect(self.open)

        self.saveAct = QAction("&Save", self)
        self.saveAct.setShortcuts(QKeySequence.Save)
        self.saveAct.setStatusTip("Save a file")
        self.saveAct.triggered.connect(self.save)

        self.saveasAct = QAction("&Save as", self)
        self.saveasAct.setShortcuts(QKeySequence.SaveAs)
        self.saveasAct.setStatusTip("Save as a file")
        self.saveasAct.triggered.connect(self.saveAs)

        self.aboutQtAct = QAction("About &Qt", self)
        self.aboutQtAct.setStatusTip("Show the Qt library's About box")
        self.aboutQtAct.triggered.connect(qApp.aboutQt)

        self.exitAct = QAction("&Exit", self)
        self.exitAct.setStatusTip("Exit")
        self.exitAct.triggered.connect(self.exit)

        #self.cutAct.setEnabled(False)
        #self.copyAct.setEnabled(False)
        #self.textEdit.copyAvailable[bool].connect(self.cutAct.setEnabled)
        #self.textEdit.copyAvailable[bool].connect(self.copyAct.setEnabled)

        self.findAct = QAction("&Find", self)
        self.findAct.triggered.connect(self.find)
        self.gotocellAct = QAction("&GoToCell", self)
        self.gotocellAct.triggered.connect(self.gotocell)
        self.sortAct = QAction("&Sort", self)
        self.sortAct.triggered.connect(self.sort)

        self.undoAct = QAction("&Undo", self)
        self.redoAct = QAction("&Redo", self)
        self.cutAct = QAction("&Cut", self)
        self.copyAct = QAction("&Copy", self)
        self.pasteAct = QAction("&Paste", self)
        self.aboutAct = QAction("&About", self)
        self.boldAct = QAction("&Bold", self)
        self.italicAct = QAction("&Italic", self)
        self.leftAlignAct = QAction("&LeftAlign", self)
        self.rightAlignAct = QAction("&Alignment", self)
        self.justifyAct = QAction("&Justify", self)
        self.centerAct = QAction("&Center", self)
        self.setLineSpacingAct = QAction("&setLine", self)
        self.setParagrahSpacingAct = QAction("&setPAragrah", self)


    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.Act)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addSeparator()

        self.dataMenu = self.menuBar().addMenu("&Data")
        self.dataMenu.addAction(self.findAct)
        self.dataMenu.addAction(self.gotocellAct)
        self.dataMenu.addAction(self.sortAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.formatMenu = self.editMenu.addMenu("&Fornat")
        self.formatMenu.addAction(self.boldAct)
        self.formatMenu.addAction(self.italicAct)
        self.formatMenu.addSeparator().setText("Alignment")
        self.formatMenu.addAction(self.leftAlignAct)
        self.formatMenu.addAction(self.rightAlignAct)
        self.formatMenu.addAction(self.justifyAct)
        self.formatMenu.addAction(self.centerAct)
        self.formatMenu.addSeparator()
        self.formatMenu.addAction(self.setLineSpacingAct)
        self.formatMenu.addAction(self.setParagrahSpacingAct)

    def readSettings(self):
        self.settings = QSettings("Trolltrch", "Application Example")
        self.pos = self.settings.value("pos", QPoint(200, 200))#.toPoint()
        self.size = self.settings.value("size", QSize(400, 400))#.toSize()
        self.resize(self.size)
        self.move(self.pos)

    def writeSettings(self):
        self.settings = QSettings("Trolltech", "Application Example")
        self.settings.setValue("pos", self.pos)
        self.setting.setValue("size", self.size)

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QMessageBox.warning(self, "Application",
                                                                  "The document has been modified.\n"
                                                                  "Do you want to save your changes?",
                                                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.cancel)
            
            if ret == QMessageBox.Save:
                return self.save
            elif ret == QMessageBox.Cancel:
                return False
        
        return True

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Application", "Cannot read file"
                                                                                        "{}:\n{}".format(fileName, file.errorString()))
            return False

        in_ = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(in_.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                                         "Cannot write file %1:\n%2.".arg(fileName)
                                                                                                           .arg(file.errorString()))
            return False

        self.out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.out = self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile.isEmpty():
            shownName = "untitled.txt"
        else:
            shownName = strippedName(curFile)

        setWindowTitle(tr("%1[*] - %2").arg(shownName).arg("Application"))

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def exit(self):
        pass

    '''
    def connectlist(self):

        self.copyAct.triggered.connect(self.spreadsheet.copy())
        self.pasteAct.triggered.connect(self.spreadsheet.paste())
        # self.
    '''

    def find(self):
        print("findをクリックしました")
        self.fw = FindDialog()
        self.fw.show()
        self.fw.activateWindow()

    def gotocell(self):
        self.gw = GoToCell()
        self.gw.show()
        self.gw.activateWindow()

    def sort(self):
        self.sw = Sort()
        self.sw.show()
        self.sw.activateWindow()





    

    


    


