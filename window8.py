import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout, QWidget, QMessageBox, QAction, QFileDialog, QSplitter, QFrame, QDesktopWidget)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QFont
from PyQt5.QtCore import (pyqtSlot, Qt, QFile, QTextStream, QFileInfo, QSettings, 
QSize, QPoint)

class MainWindow(QMainWindow):

	def __init__(self):
		
		super().__init__()

		self.app = App(self)

		self.settings = None
		self.readSettings()

		self.title = 'Application Test'
		self.left = 10
		self.top = 10
		self.width = 1480
		self.height = 800
		self.initUI()

	def writeSettings(self):
		self.settings = QSettings("CDMCAR", "TestApplication")
		self.settings.beginGroup('MainWindow')
		self.settings.setValue('size', self.size())
		self.settings.setValue('pos', self.pos())
		self.settings.endGroup()
		self.settings.setValue('splitterSizes', self.app.splitter.saveState())

	def readSettings(self):
		self.settings = QSettings("CDMCAR", "TestApplication")
		self.settings.beginGroup('MainWindow')
		self.resize(self.settings.value('size', QSize(400, 400)))
		self.move(self.settings.value('pos', QPoint(200, 200)))
		self.settings.endGroup()
		#self.app.textEdit.setText(str(self.settings.fileName()))
		#self.settings.value('splitterSizes', self.app.splitter.restoreState())

	def initUI(self):

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.app = App(self)
		self.setCentralWidget(self.app)

		# Set window background color
		#self.setAutoFillBackground(True)
		#p = self.palette()
		#p.setColor(self.backgroundRole(), QColor(0, 230, 200, 255))
		#self.setPalette(p)

		self.curFile = ''
		self.createMenu()

		self.center()

		self.readSettings()

		self.settings = QSettings('CDMCAR', 'TestApplication')

		geometry = self.settings.value('geometry', "")

		self.restoreGeometry(geometry)
		self.app.splitter.restoreState(self.settings.value('splitterSizes'), QSize(200,200))

		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def closeEvent(self, event):
		geometry = self.saveGeometry()

		self.settings.setValue('geometry', geometry)

		super(MainWindow, self).closeEvent(event)

		if self.app.maybeSave():
			self.writeSettings()
			event.accept()
		else:
			event.ignore()

		if sys.exit():
			self.writeSettings()

	def newFile(self):
		if self.app.maybeSave():
			self.app.textEdit.clear()
			self.app.setCurrentFile('')

	def openFile(self):
		if self.app.maybeSave():
			fileName, _ = QFileDialog.getOpenFileName(self)
			if fileName:
				self.loadFile(fileName)

	def loadFile(self, fileName):
		file = QFile(fileName)
		if not file.open(QFile.ReadOnly | QFile.Text):
			QMessageBox.warning(self, "Application",
				"Cannot read file %s:\n%s." % (fileName, file.errorString()))
			return
		
		inf = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)
		self.app.textEdit.setPlainText(inf.readAll())
		QApplication.restoreOverrideCursor()

		self.app.setCurrentFile(fileName)
		self.statusBar().showMessage("File loaded", 2000)

	def openFiles(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", 
			"","All Files (*);;Python Files (*.py)", options=options)
		if files:
			print(files)
		 
	def saveFile(self):
		filename, _ = QFileDialog.getSaveFileName(self, 
			"Choose a file name", '.', "All Files (*);;HTML (*.html *.htm)")
		if not filename:
			return

		file = QFile(filename)
		if not file.open(QFile.WriteOnly | QFile.Text):
			QMessageBox.warning(self, "Application",
				"Cannot write file %s:\n%s." % (filename, file.errorString()))
			return

		out = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)
		out << self.app.textEdit.toPlainText()
		QApplication.restoreOverrideCursor()

		self.statusBar().showMessage("Saved '%s'" % filename, 2000)

	def saveAs(self):
		fileName, _ = QFileDialog.getSaveFileName(self)
		if fileName:
			return self.saveFile(fileName)

		return False

	def undoFile(self):
		document = self.app.textEdit.document()
		document.undo()

	def createMenu(self):
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('File')
		editMenu = mainMenu.addMenu('Edit')
		viewMenu = mainMenu.addMenu('View')
		searchMenu = mainMenu.addMenu('Search')
		toolsMenu = mainMenu.addMenu('Tools')
		helpMenu = mainMenu.addMenu('Help')
		 
		newButton = QAction('New', self)
		newButton.triggered.connect(self.newFile)
		fileMenu.addAction(newButton)

		openButton = QAction('Open', self)
		openButton.setShortcut('Ctrl+O')
		openButton.setStatusTip('Open file')
		openButton.triggered.connect(self.openFile)
		fileMenu.addAction(openButton)

		saveButton = QAction('Save', self)
		saveButton.setShortcut('Ctrl-S')
		saveButton.setStatusTip('Save file')
		saveButton.triggered.connect(self.saveFile)
		fileMenu.addAction(saveButton)

		saveAsButton = QAction('Save As..', self)
		saveAsButton.triggered.connect(self.saveAs)
		fileMenu.addAction(saveAsButton)

		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)
		fileMenu.addAction(exitButton)

		undoButton = QAction('Undo', self)
		undoButton.triggered.connect(self.undoFile)
		editMenu.addAction(undoButton)

		redoButton = QAction('Redo', self)
		editMenu.addAction(redoButton)

		cutButton = QAction('Cut', self)
		cutButton.triggered.connect(self.app.textEdit.cut)
		editMenu.addAction(cutButton)

		copyButton = QAction('Copy', self)
		copyButton.triggered.connect(self.app.textEdit.copy)
		editMenu.addAction(copyButton)

		pasteButton = QAction('Paste', self)
		pasteButton.triggered.connect(self.app.textEdit.paste)
		editMenu.addAction(pasteButton)

		editorView = QAction('Editor View', self)
		viewMenu.addAction(editorView)

		noteView = QAction('Notebook View', self)
		viewMenu.addAction(noteView)

		webView = QAction('Web View', self)
		viewMenu.addAction(webView)

		consoleView = QAction('Console View', self)
		viewMenu.addAction(consoleView)

		settings = QAction('Settings', self)
		toolsMenu.addAction(settings)

		cutButton.setEnabled(False)
		copyButton.setEnabled(False)
		self.app.textEdit.copyAvailable.connect(cutButton.setEnabled)
		self.app.textEdit.copyAvailable.connect(copyButton.setEnabled)

class App(QWidget):

	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		#self.createHorizontalLayout()
		self.createGridLayout()

		windowLayout = QVBoxLayout()
		#windowLayout.addStretch(1)
		#windowLayout.addWidget(self.hGroupBox)
		windowLayout.addWidget(self.gridGroupBox)

		self.setLayout(windowLayout)

	def createHorizontalLayout(self):

		'''self.hGroupBox = QGroupBox()

		layout = QHBoxLayout()
		layout.addStretch(1)

		button = QPushButton('PyQt button', self)
		button.setToolTip('This is an example button')
		button.clicked.connect(self.on_click_button)
		layout.addWidget(button)

		mb_button = QPushButton('MessageBox example', self)
		mb_button.clicked.connect(self.on_click_messagebox)
		layout.addWidget(mb_button)

		self.hGroupBox.setLayout(layout)'''

	def createGridLayout(self):

		self.gridGroupBox = QGroupBox()

		layout = QHBoxLayout(self)

		#self.textbox = QLineEdit(self)
		#self.textbox.resize(100,100)
		#layout.addWidget(self.textbox,1,1)

		#tb_button = QPushButton('Submit')
		#tb_button.clicked.connect(self.on_click_submit)

		self.splitter = QSplitter(Qt.Horizontal, self)

		self.vsplitter = QSplitter(Qt.Vertical, self)

		frame = QFrame(self)
		#frame.setFrameShape(QFrame.StyledPanel)

		topleft = QFrame(frame)
		topleft.setFrameShape(QFrame.StyledPanel)

		topright = QFrame(frame)
		topright.setFrameShape(QFrame.StyledPanel)

		bottomleft = QFrame(frame)
		bottomleft.setFrameShape(QFrame.StyledPanel)

		bottomright = QFrame(frame)
		bottomright.setFrameShape(QFrame.StyledPanel)

		#self.textDisplay = QTextEdit()
		#self.textDisplay.setReadOnly(True)

		self.createEditor()
		
		self.splitter.addWidget(topleft)
		self.splitter.addWidget(self.textEdit)
		
		self.splitter.addWidget(self.vsplitter)
		self.vsplitter.addWidget(bottomleft)
		self.vsplitter.addWidget(bottomright)

		self.splitter.setSizes([100,300,200,200])

		layout.addWidget(self.splitter)

		self.gridGroupBox.setLayout(layout)



	def createEditor(self):
		self.textEdit = QTextEdit(self)
		self.textEdit.setAcceptRichText(True)
		# AutoNone, AutoBulletList, AutoAll
		self.textEdit.setAutoFormatting(QTextEdit.AutoAll)
		# NoWrap, WidgetWidth, FixedPixelWidth, FixedColumnWidth
		self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
		#self.textEdit.setTabStopDistance(64)
		self.textEdit.setReadOnly(False)
		self.textEdit.setUndoRedoEnabled(True)

		#self.textEdit.setDocument()

		#self.textEdit.clear()
		#self.textEdit.copy()
		#self.textEdit.cut()
		#self.textEdit.paste()
		#self.textEdit.redo()
		#self.textEdit.undo()
		#self.textEdit.find()
		#self.textEdit.selectAll()
		#self.textEdit.setCurrentFont()
		#self.textEdit.setFontFamily()
		#self.textEdit.setFontItalic()
		#self.textEdit.setFontWeight()
		#self.textEdit.setFontPointSize()
		#self.textEdit.setFontUnderline()
		#self.textEdit.setText()
		#self.textEdit.setTextBackgroundColor()
		#self.textEdit.setTextColor()
		#self.textEdit.setAlignment()

		# Signals
		# cursorPositionChanged(), selectionChanged(), textChanged(),
		# currentCharFormatChanged(), copyAvailable(), redoAvailable(), undoAvailable()

	def documentWasModified(self):
		self.setWindowModified(self.textEdit.document().isModified())

	def maybeSave(self):
		if self.textEdit.document().isModified():
			ret = QMessageBox.warning(self, "Application",
				"The document had been modified. \nDo you want to save your changes?",
				QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

			if ret == QMessageBox.Save:
				return self.save()

			if ret == QMessageBox.Cancel:
				return False

		return True

	def setCurrentFile(self, fileName):
		self.curFile = fileName
		self.textEdit.document().setModified(False)
		self.setWindowModified(False)

		if self.curFile:
			shownName = self.strippedName(self.curFile)
		else:
			shownName = 'untitled.txt'

		self.setWindowTitle("%s[*] - Application" % shownName)

	def strippedName(self, fullFileName):
		return QFileInfo(fullFileName).fileName()

	@pyqtSlot()
	def on_click_submit(self):
		textboxValue = self.textbox.text()
		print(textboxValue)
		self.textbox.setText("")

if __name__ == '__main__':

	application = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(application.exec_())