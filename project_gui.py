import sys
import math
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PIL import Image
from io import BytesIO


def none():
    image_id = "profile"
    # source image
    s_image = Image.open(f'images/{image_id}.jpg')
    # destination image
    width, height = s_image.size
    canvas = Image.new("RGB", (width,height), "white")
    target_x = 0
    for source_x in range(s_image.width):
        target_y = 0
        for source_y in range(s_image.height):
            color = s_image.getpixel((source_x, source_y)) # get pixels from the source
            canvas.putpixel((target_x, target_y), color) # put pixels onto target
            target_y += 1
        target_x +=1
    canvas.save("temp.jpg")

def smaller():
    image_id = "profile"
    # source image
    s_image = Image.open(f'images/{image_id}.jpg')
    # destination image
    width, height = s_image.size
    canvas = Image.new("RGB", (math.ceil(width/2),math.ceil(height/2)), "white")
    target_x = 0
    for source_x in range(0, s_image.width, 2):
        target_y = 0
        for source_y in range(0, s_image.height, 2):
            color = s_image.getpixel((source_x, source_y))
            canvas.putpixel((target_x, target_y), color)
            target_y += 1
        target_x += 1
    canvas.save("temp.jpg")

def negative():
    image_id = "profile"
    s_image = Image.open(f'images/{image_id}.jpg')
    new_list = []
    for p in s_image.getdata():
        temp = (255-p[0], 255-p[1], 255-p[2])
        new_list.append(temp)
    s_image.putdata(new_list)
    s_image.save("temp.jpg")

def grayscale(picture):

    new_list = []

    for p in picture.getdata():
        new_red = int(p[0] * 0.299)
        new_green = int(p[1] * 0.587)
        new_blue = int(p[2] * 0.114)
        luminance = new_red + new_green + new_blue
        temp = (luminance, luminance, luminance)
        new_list.append(temp)

    return new_list

def grayscale_create():
    image_id = "profile"
    s_image = Image.open(f'images/{image_id}.jpg')
    new_list = []
    for p in s_image.getdata():
        new_red = int(p[0] * 0.299)
        new_green = int(p[1] * 0.587)
        new_blue = int(p[2] * 0.114)
        luminance = new_red + new_green + new_blue
        temp = (luminance, luminance, luminance)
        new_list.append(temp)
    s_image.putdata(new_list)
    s_image.save("temp.jpg")

def sepia_tint():
    image_id = "profile"
    s_image = Image.open(f'images/{image_id}.jpg')

    width, height = s_image.size
    mode = s_image.mode
    temp_list = []
    pic_data = grayscale(s_image)

    for p in pic_data:
    # tint shadows
        if p[0] < 63:
            red_val = int(p[0] * 1.1)
            green_val = p[1]
            blue_val = int(p[2] * 0.9)

        # tint midtones
        if p[0] > 62 and p[0] < 192:
            red_val = int(p[0] * 1.15)
            green_val = p[1]
            blue_val = int(p[2] * 0.85)

        # tint highlights
        if p[0] > 191:
            red_val = int(p[0] * 1.08)
            if red_val > 255:
                red_val = 255
            green_val = p[1]
            blue_val = int(p[2] * 0.5)
        temp_list.append((red_val, green_val, blue_val))
    s_image.putdata(temp_list)
    s_image.save("temp.jpg")

filter_list = { "none","sepia", "negative", "grayscale", "thumbnail"}
holiday_list = {"none","thanksgiving", "christmas", "halloween", "valentine"}

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Temp Image')
        self.my_label = QLabel(self)
        self.my_image = QPixmap("temp.jpg")
        self.my_label.setPixmap(self.my_image)
        self.resize(self.my_image.width(), self.my_image.height())
class Window(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.my_label = QLabel("Image Filter Application!", self)
        self.term_label = QLabel("URL: ", self)

        main_layout.addWidget(self.my_label)


        self.my_line_edit = QLineEdit(self)

        self.response_label = QLabel(self)

        self.my_combo_box = QComboBox()
        self.my_combo_box.addItems(filter_list)
        self.other_combo_box = QComboBox()
        self.other_combo_box.addItems(holiday_list)
        self.submit_btn = QPushButton("Filter", self)

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

        self.setWindowTitle("CST205 Project!")
        self.show()


    @pyqtSlot()

    def on_click(self):
        manipulation = self.my_combo_box.currentText()
        pic_filter = self.other_combo_box.currentText()
        url_link = self.my_line_edit.text()
        response = requests.get(f"{url_link}")
        bytes = BytesIO(response.content)
        image = Image.open(bytes)
        image.save("images/profile.jpg")
        self.response_label.setText("My Profile Pic")
        if manipulation == "negative":
            negative()
        elif manipulation == "grayscale":
            grayscale_create()
        elif manipulation == "thumbnail":
            smaller()
        elif manipulation == "sepia":
            sepia_tint()
        else:
            none()

        self.new_win = NewWindow()
        self.new_win.show()

app = QApplication(sys.argv)
main = Window()
main.resize(400, 100)
main.show()
sys.exit(app.exec_())
