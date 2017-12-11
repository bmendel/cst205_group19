import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
							QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PIL import Image
import facebook_scrape
import filter

filter_list = {'None', 'Sepia', 'Negative', 'Grayscale'}
holiday_list = {'None','Thanksgiving', 'Christmas'}
profile = 'profile.png'

class NewWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Your New Profile Picture!')
		self.my_label = QLabel(self)
		self.my_image = QPixmap(profile)
		self.my_label.setPixmap(self.my_image)
		self.resize(self.my_image.width(), self.my_image.height())

class Window(QWidget):
	def __init__(self):
		super().__init__()

		main_layout = QVBoxLayout()
		self.my_label = QLabel('Facebook Filter Application', self)
		main_layout.addWidget(self.my_label)

		self.term_label = QLabel('Facebook URL: ', self)
		self.my_line_edit = QLineEdit(self)

		self.my_combo_box = QComboBox()
		self.my_combo_box.addItems(filter_list)
		self.other_combo_box = QComboBox()
		self.other_combo_box.addItems(holiday_list)
		
		self.response_label = QLabel(self)
		self.submit_btn = QPushButton('Filter', self)

		h_layout = QHBoxLayout()
		h_layout.addWidget(self.term_label)
		h_layout.addWidget(self.my_line_edit)

		v_layout = QVBoxLayout()
		v_layout.addWidget(self.submit_btn)
		v_layout.addWidget(self.response_label)

		main_layout.addLayout(h_layout)
		main_layout.addWidget(self.my_combo_box)
		main_layout.addWidget(self.other_combo_box)
		main_layout.addLayout(v_layout)

		self.new_win = NewWindow()

		self.submit_btn.clicked.connect(self.on_click)
		self.setLayout(main_layout)

		self.setWindowTitle('Facebook Profile Picture Editor')
		self.show()
		
	@pyqtSlot()
	def on_click(self):
		if not self.my_line_edit.text():
			return
		facebook_scrape.scrape_profile(self.my_line_edit.text(), profile)
		filter.bigger(profile)
		
		manipulation = self.my_combo_box.currentText()
		pic_filter = self.other_combo_box.currentText()
		line_edit_value = self.my_line_edit.text()
		
		if pic_filter != 'None':
			filter.add_filter(profile, pic_filter)
			
		if manipulation == 'Negative':
			filter.negative(profile)
		elif manipulation == 'Grayscale':
			filter.grayscale_create(profile)
		elif manipulation == 'Sepia':
			filter.sepia_tint(profile)

		self.new_win = NewWindow()
		self.new_win.show()
		#filter.smaller(profile)
	
app = QApplication(sys.argv)
main = Window()
main.resize(400, 100)
main.show()
sys.exit(app.exec_())
