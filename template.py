import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *

class Template(QWidget):

	def __init__(self, parent=None):
		super(QWidget, self).__init__(parent=None)

		self.title = 'Template'
		self.left = 0
		self.top = 0
		self.width = 1200
		self.height = 800

		self.setWindowTitle('self.title')
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.makeLayout()

	def makeLayout(self):

		self.frame1 = QFrame(self)

		self.makeGroupBox1 = QGroupBox(self.frame1)
		self.makeGroupBox2 = QGroupBox()
		self.makeGroupBox3 = QGroupBox()

		scrollArea = QScrollArea()
		scrollArea.setWidget(self.frame1)
		#self.makeGroupBox1.addWidget(scrollArea)

		hLayout = QHBoxLayout()
		vLayout = QVBoxLayout()
		
		self.gridLayout = QGridLayout(self.frame1)
		self.gridLayout2 = QGridLayout()

		self.frame1.setLayout(self.gridLayout)
		self.makeGroupBox2.setLayout(self.gridLayout2)

		self.items = []

		lbl = QLabel('Enter Grid x, y Values')
		self.gridLayout2.addWidget(lbl,0,0)

		xlbl = QLabel('X')
		self.xVal = QComboBox()
		self.comboNumber(self.xVal, '20')

		ylbl = QLabel('Y')
		self.yVal = QComboBox()
		self.comboNumber(self.yVal, '20')

		go = QPushButton('Make Grid')
		go.clicked.connect(lambda item: self.helpGrid(self.makeGrid()))
		
		self.gridLayout2.addWidget(xlbl,0,0)
		self.gridLayout2.addWidget(self.xVal,0,1)
		self.gridLayout2.addWidget(ylbl,0,2)
		self.gridLayout2.addWidget(self.yVal,0,3)
		self.gridLayout2.addWidget(go,0,4)

		frame2 = QFrame(self)
		frame2.setFrameShape(QFrame.StyledPanel)

		self.hSplitter = QSplitter(Qt.Horizontal, frame2)
		self.vSplitter = QSplitter(Qt.Vertical, frame2)

		label = QLabel()
		label.setText('Label')

		widgetButton = QPushButton()
		widgetButton.setText('Make Widgets')
		widgetButton.clicked.connect(self.widgetButtonClicked)
		self.gridLayout.addWidget(widgetButton,0,0)

		self.textInput = QLineEdit()
		self.textInput.setPlaceholderText('Input Text')
		self.textInput.setMaxLength(20)

		self.textInput = QLineEdit()
		self.textInput.setPlaceholderText('Input Text')
		self.textInput.setMaxLength(20)

		self.checkbox = QCheckBox()
		self.checkbox.setText('Checkbox')
		#self.checkbox.stateChanged.connect(self.checkState)

		self.checkbox = QCheckBox()
		self.checkbox.setText('Checkbox')
		#self.checkbox.stateChanged.connect(self.checkState)

		self.combobox = QComboBox()
		self.combobox.addItem('Item')
		self.combobox.activated.connect(self.widgetButtonClicked)
		self.gridLayout.addWidget(self.combobox)

		self.combobox2 = QComboBox()
		self.combobox2.addItem('Item')
		self.combobox2.activated.connect(self.cBoxActivated)
		self.gridLayout.addWidget(self.combobox2)

		#return frame1.setLayout(self.gridLayout)

		splitter = QSplitter()

		splitter.addWidget(self.frame1)
		splitter.addWidget(self.makeGroupBox2)
		hLayout.addWidget(splitter)
		vLayout.addLayout(hLayout)
		#self.makeGroupBox3.setLayout(hLayout)

		self.setLayout(vLayout)

	def comboNumber(self, name, number):
		num = number
		n = name
		items = []
		for i in range(int(num)+1):
			items.append(n.addItem('%d' % i))

		return items

	def makeGrid(self):

		xN = [val for val in range(int(self.xVal.currentText()))]
		yN = [val for val in range(int(self.yVal.currentText()))]
		cells = int(self.xVal.currentText()) * int(self.yVal.currentText())

		grid = [xN, yN]

		items = []
		list = []

		for j in xN:
			x = j
			for j in yN:
				y = j
				items.append([x, y])
				string = ('lbl' + '_' + str(x) + '_' + str(y))
				string = QLabel('%s, %s' % (x, y))
				list.append(string)

		return list

	def helpGrid(self, list=''):
		xN = [val for val in range(int(self.xVal.currentText()))]
		yN = [val for val in range(int(self.yVal.currentText()))]
		
		items = []
		grid = [xN, yN]

		for n in xN:
			x = n
			for o in yN:
				y = o
				items.append([x,y])
		for i in list:
			x = i.text()[0]
			y = i.text()[3]
			
			d = 0
			e = 0
			for j in x:
				d = j
				for k in y:
					e = k
					self.gridLayout2.addWidget(i,int(j)+1,int(k)+1)

		self.items = items
		print(self.items)
		return items

	def widgetButtonClicked(self):
		lblWidget = []
		self.cells = int(self.xVal.currentText()) * int(self.yVal.currentText())
		number = 0
		items = self.helpGrid()
		print(items)
		
		for c in range(self.cells):
			string = ('lblWidget_%s' % str(c))
			string = QLabel('Widget At ' + str(self.items[c]))
			lblWidget.append(string)
			string2 = ('combobox_%s' % str(c))
			string2 = QComboBox()
			string2.setObjectName('comboWidget_%' + str(c))
			comboWidget.append(string2)
			string3 = ('btnWidget_%s' % str(c))
			string3 = ('btnWidget_' + str(self.items[c]))
			btnWidget.append(string3)
		
		for i in lblWidget:
			self.gridLayout.addWidget(i,number,1)
			number += 1
		number2 = 1
		for i in comboWidget:
			self.gridLayout.addWidget(i, number2, 1)
			number2 += 1
		number3 = 2
		for i in btnWidget:
			self.gridLayout.addWidget(i, number3, 1)

	def cBoxActivated(self):
		pass


if __name__ == '__main__':

	application = QApplication(sys.argv)
	win = Template()
	win.show()
	sys.exit(application.exec_())