import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout, QWidget, QMessageBox, QAction, QFileDialog)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QFont
from PyQt5.QtCore import pyqtSlot, Qt, QFile, QTextStream, QFileInfo, QSettings

class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.title = 'PyQt5 simple window with status bar'
		self.left = 10
		self.top = 10
		self.width = 800
		self.height = 600
		self.initUI()

	def initUI(self):

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.statusBar().showMessage('')

		self.app = App(self)
		self.setCentralWidget(self.app)

		# Set window background color
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), QColor(0, 230, 200, 255))
		self.setPalette(p)

		self.curFile = ''
		self.createMenu()

		self.show()

	def closeEvent(self, event):
		if self.app.maybeSave():
			#self.writeSettings()
			event.accept()
		else:
			event.ignore()	

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

		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)
		fileMenu.addAction(exitButton)

		cutButton.setEnabled(False)
		copyButton.setEnabled(False)
		self.app.textEdit.copyAvailable.connect(cutButton.setEnabled)
		self.app.textEdit.copyAvailable.connect(copyButton.setEnabled)

class App(QWidget):

	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		self.createHorizontalLayout()
		self.createGridLayout()

		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.hGroupBox)
		windowLayout.addWidget(self.gridGroupBox)

		self.setLayout(windowLayout)

	def createHorizontalLayout(self):

		self.hGroupBox = QGroupBox()

		layout = QHBoxLayout()

		button = QPushButton('PyQt button', self)
		button.setToolTip('This is an example button')
		button.clicked.connect(self.on_click_button)
		layout.addWidget(button)

		mb_button = QPushButton('MessageBox example', self)
		mb_button.clicked.connect(self.on_click_messagebox)
		layout.addWidget(mb_button)

		self.hGroupBox.setLayout(layout)

	def createGridLayout(self):

		self.gridGroupBox = QGroupBox()

		layout = QGridLayout()

		self.textbox = QLineEdit(self)
		self.textbox.resize(100,100)
		layout.addWidget(self.textbox,1,1)

		tb_button = QPushButton('Submit')
		tb_button.clicked.connect(self.on_click_submit)
		layout.addWidget(tb_button,1,2)

		self.createEditor()
		layout.addWidget(self.textEdit,2,1)

		self.gridGroupBox.setLayout(layout)

	def createEditor(self):
		self.textEdit = QTextEdit()
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
	def on_click_button(self):
		print('PyQt5 button click')

	def on_click_messagebox(self):
		buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you like PyQt5?", 
			QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

		if buttonReply == QMessageBox.Yes:
			print('Yes clicked.')
		if buttonReply == QMessageBox.No:
			print('No clicked.')
		if buttonReply == QMessageBox.Cancel:
			print('Cancel')

	def on_click_submit(self):
		textboxValue = self.textbox.text()
		print(textboxValue)
		self.textbox.setText("")

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())