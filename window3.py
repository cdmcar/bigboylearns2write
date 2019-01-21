import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

	def __init__(self):
		super().__init__()

		self.title = 'PyQt5 simple window with status bar'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.statusBar().showMessage('Message in statusbar.')

		button = QPushButton('PyQt button', self)
		button.setToolTip('This is an example button')
		button.move(100,70)
		button.clicked.connect(self.on_click)

	@pyqtSlot()
	def on_click(self):
		print('PyQt5 button click')

class Dialog(QDialog):

	def slot_method(self):
		print('Slot method called.')

	def __init__(self):
		super(Dialog, self).__init__()

		button = QPushButton("Click")
		button.clicked.connect(self.slot_method)

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(button)

		self.setLayout(mainLayout)
		self.setWindowTitle("Button Example")

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = App()
	display = Dialog()
	sys.exit(display.exec_())