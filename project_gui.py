###########################################################
# Filename: project_gui.py
# Author: Eli Manzo
# Course: CST 205
# Last Updated: 12/10/17
#
# The main GUI for the application
###########################################################

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
							QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PIL import Image
import facebook_scrape
import filter

filter_list = ['None', 'Sepia', 'Negative', 'Grayscale']
template_list = ['None','Thanksgiving', 'Christmas']
profile = 'profile.png'

# Represents a window with the newly modified profile picture
class NewWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Your New Profile Picture!')
		self.my_label = QLabel(self)
		self.my_image = QPixmap(profile)
		self.my_label.setPixmap(self.my_image)
		self.resize(self.my_image.width(), self.my_image.height())

# Represents the main window where the user picks modifications
class Window(QWidget):
	def __init__(self):
		super().__init__()
		
		# Creates the main layout, with a label for the application
		main_layout = QVBoxLayout()
		self.my_label = QLabel('Facebook Filter Application', self)
		main_layout.addWidget(self.my_label)

		# Creates a layout for adding a facebook url
		self.url_layout = QHBoxLayout()
		self.url_label = QLabel('Facebook URL: ', self)
		self.url_line_edit = QLineEdit(self)
		self.url_layout.addWidget(self.url_label)
		self.url_layout.addWidget(self.url_line_edit)

		# Creates a layout to apply a filter
		self.filter_layout = QHBoxLayout()
		self.filter_combo_box = QComboBox()
		self.filter_combo_box.addItems(filter_list)
		self.filter_label = QLabel('Filter: ', self)
		self.filter_layout.addWidget(self.filter_label)
		self.filter_layout.addWidget(self.filter_combo_box)
		
		# Creates a layout to apply a template
		self.template_layout = QHBoxLayout()
		self.template_combo_box = QComboBox()
		self.template_combo_box.addItems(template_list)
		self.template_label = QLabel('Template: ', self)
		self.template_layout.addWidget(self.template_label)
		self.template_layout.addWidget(self.template_combo_box)
		
		# Creates a button that applies filters and layouts to the profile pic
		self.submit_btn = QPushButton('Make your profile picture!', self)
		self.submit_btn.clicked.connect(self.on_click)

		# Adds all layouts and widgets to the main layout
		main_layout.addLayout(self.url_layout)
		main_layout.addLayout(self.filter_layout)
		main_layout.addLayout(self.template_layout)
		main_layout.addWidget(self.submit_btn)

		# Displays the main application window
		self.setLayout(main_layout)
		self.setWindowTitle('Facebook Profile Picture Editor')
		self.show()
		
	# Applies filters and templates to webscraped profile picture
	@pyqtSlot()
	def on_click(self):
		# Gets information about the type of template and filter needed,
		# as well as the profile url
		pic_url = self.url_line_edit.text()
		pic_filter = self.filter_combo_box.currentText()
		pic_template = self.template_combo_box.currentText()
		
		# If a url is in the line edit field, scrape a profile picture
		if not pic_url:
			return
		facebook_scrape.scrape_profile(pic_url, profile)
		filter.bigger(profile)
		
		# Adds template to profile picture
		if pic_template != 'None':
			filter.add_template(profile, pic_template)
		
		# Adds filter to profile picture
		if pic_filter == 'Negative':
			filter.negative(profile)
		elif pic_filter == 'Grayscale':
			filter.grayscale_create(profile)
		elif pic_filter == 'Sepia':
			filter.sepia_tint(profile)

		# Displays newly modified profile picture in a new window
		self.new_win = NewWindow()
		self.new_win.show()
	
app = QApplication(sys.argv)
main = Window()
main.resize(400, 100)
main.show()
sys.exit(app.exec_())
