import sys
from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)

class MainWindow(qtw.Widgets):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.MaxRecentFile = 5

    # -------初期化---------------------------
    def writeSettings(self):
        pass

    def maybeSave(self):
        pass

    # -----------------------------------------
        

    def createMenus(self):
        self.fileMenu = qtw.QMainWindow.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)

        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.exitAction)


        self.editMenu = qtw.QMainWindow.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addAction(self.deleteAction)


        self.selectSubMenu = qtw.QMainWindow.menuBar().addMenu("&Select")
        self.selectSubMenu.addAction(self.selectRowAction)
        self.selectSubMenu.addAction(self.selectColumnAction)
        self.selectSubMenu.addAction(self.selectAllAction)


        self.editMenu.addSeparator()
        self.editMenu.addAction(self.findAction)
        self.editMenu.addAction(self.goToCellAction)


        self.toolMenu = qtw.QMainWindow.menuBar().addMenu("&Tools")
        self.toolMenu.addAction(self.recalculateAction)
        self.toolMenu.addAction(self.sortAction)


        self.optionMenu = qtw.QMainWindow.menuBar().addMenu("&Options")
        self.optionMenu.addAction(self.showGridAction)
        self.optionMenu.addAction(self.autoRecalcAction)

        qtw.QMainWindow.menuBar().addSeparator()


        self.helpMenu = qtw.QMainWindow.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)






    def createActions(self):
        self.newAction = qtc.QAction("&New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new file")
        self.newAction.triggered.coonect(self.newFile)

        self.newAction = qtc.QAction("&Open ...", self)
        self.newAction.setShortcut("Ctrl+O")
        self.newAction.setStatusTip("Open a file")
        self.newAction.triggered.coonect(self.openFile)

        self.newAction = qtc.QAction("&Save", self)
        self.newAction.setShortcut("Ctrl+S")
        self.newAction.setStatusTip("Save a file")
        self.newAction.triggered.coonect(self.saveFile)

        self.newAction = qtc.QAction("&Save $As ...", self)
        self.newAction.setStatusTip("Save as a file")
        self.newAction.triggered.coonect(self.saveAsFile)

        # 最近開いたファイルは後回し
        #for i in range(self.MaxRecentFile):

        self.selectAllAction = qtc.QAction("&All", self)
        self.selectAllAction.setShortcut("Ctrl+A")
        self.selectAllAction.setStatusTip("Select all the cells in the spreadsheet")
        self.selectAllAction.triggered.connect(qtw.QAbstractItemView.selectAll())

        self.showGridAction = qtc.QAction("&Show Grid", self)
        self.showGridAction.setCheckable(True)
        self.showGridAction.setChecked(qtw.QTableView.showGrid())
        self.showGridAction.setStatusTip("Show or hide the spreadsheet's grid")
        self.showGridAction.clicked.connect(qtw.QTableView.setShowGrid)

        self.aboutQtAction = qtc.QAction("&About &Qt", self)
        self.aboutQtAction.setStatusTip("Show the Qt library's About box")
        self.aboutQtAction.triggered.connect(qtw.QApplication.aboutQt())

    def createContextMenu(self):

        self.spreadsheet.addAction(self.cutAction)
        self.spreadsheet.addAction(self.copyAction)
        self.spreadsheet.addAction(self.pasteAction)
        self.spreadsheet.setContextMenuPolicy(qtc.Qt.ActionsContextMenu)

    
    def createToolBars(self):
        self.fileToolBar = qtc.addToolBar("&File")
        self.fileToolBar.addAction(self.newAction)
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.saveAction)

        self.editToolBar = qtc.addToolBar("&Edit")
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.findAction)
        self.addAction(self.goToCellAction)


    def createStatusBar(self):
        self.locationLabel = qtw.QLabel("W999")
        self.locationLabel.setAlignment(qtc.Qt.AlignHCenter)
        self.locationLabel.setMinimumSize(self.locationLabel.sizeHint())

        self.formulaLabel = qtw.QLabel
        self.formulaLabel.setIndent(3)

        qtw.QMainWindow.statusBar.addWidget(self.locationLabel)
        qtw.QMainWindow.statusBar.addWidget(self.formulaLabel, 1)

        self.spreadsheet.currentCellChanged.connect(self.updateStatusBar)
        self.spreadsheet.modified.connect(self.spreadsheetModified)

        self.updataStatusBar()

    
    def updateStatusBar(self):
        self.locationLabel.setText(self.spreadsheet.currentLocation())
        self.formulaLabel.setText(self.spreadsheet.currentFormula())


    def spreadsheetModified(self):
        qtw.Qwidget.setWindowModified(True)
        self.updateStatusBar()


    def newFile(self):
        if self.maybeSave:
            self.spreadsheet.clear()
            self.setCurrentFile("")


    def maybeSave(self):
        if modified:
            ret = qtw.QMessageBox.warning(self, "Spreadsheet", "The document has been modified.\nDo you want to save your changes?",
                                                                qtw.QMessageBox.Yes | qtw.QMessageBox.Escape,
                                                                qtw.QMessageBox.No,
                                                                qtw.QMessageBox.Cancel | qtw.QMessageBox.Escape)
            
            if ret == qtw.QMessageBox.Yes:
                return self.save

            elif ret == qtw.QMessageBox.Cancel:
                return False

            return True

    
    def open(self):
        if self.maybeSave:
            fileName = qtw.QFileDialog.getOpenFileName(self, "Open Spreadsheet", ".", "Spreadsheet files (*.sp)")

            if not fileName.isEmpty():
                self.loadFile(fileName)

    def loadFile(self, fileName):
        if not self.spreadsheet.readFile(fileName):
            qtw.QMainWindow.statusBar.showMessage("Loading canceled", 2000)
            return False

        self.setCurrentFile(fileName)
        qtw.QMainWindow.statusBar.showMessage("File loaded", 2000)
        return True

    def save(self):
        if self.curFile.isEmpty():
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveFile(self, fileName):
        if not self.spreadsheet.writeFile(fileName):
            qtw.QMainWindow.statusBar.showMessage("Saving canceld", 2000)
            return False

        self.setCurrentFile(fileName)
        qtw.QMainWindow.statusBar.showMessage("File saved", 2000)
        return True

    def saveAs(self):
        fileName = qtw.QFileDialog.getSaveName(self, "Save Spreadsheet", ".", "Spreadsheet file (*.sp)")

        if fileName.isEmpty():
            return False

        return self.saveFile(fileName)

    def closeEvent(self, event):
        if self.okToContinue:
            self.writeSettings
            event.accept()
        else:
            event.ignore()

    def setCurrentFile(self, fileName):
        curFile = fileName
        setWindowModified(False)

        if not curFile.isEmpty():
            shownName = strippedName(curFile)
            self.updateRecentFileActions
        else:
            shownName = "Untitled.txt"
        setWindowTitle(("%1[*] - %2").arg(shownName).arg("Spreadsheet"))


    def strippedName(self, fileName):
        return qtc.QFileInfo(fullFileName).fileName()

    def find(self):
        if not findDialog:
            findDialog = 




    











