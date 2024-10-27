import os
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QListWidget, QComboBox,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image,ImageEnhance,ImageFilter

app=QApplication([])
main_window=QWidget()
main_window.setWindowTitle('PhotoQt')
main_window.resize(900,700)

# all app widgets and objects
btn_folder=QPushButton('Open Folder')
file_list=QListWidget() 

btn_left=QPushButton('Left')
btn_right=QPushButton('Right')
mirror=QPushButton('Mirror')
sharpness=QPushButton('Sharpen')
gray=QPushButton('B/W')
saturation=QPushButton('Color')
contrast=QPushButton('Contrast')
blur=QPushButton('Blur')

filter_list=QComboBox()
filter_list.addItem('Original')
filter_list.addItem('Left')
filter_list.addItem('Right')
filter_list.addItem('Mirror')
filter_list.addItem('Sharpen')
filter_list.addItem('B/W')
filter_list.addItem('Color')
filter_list.addItem('Contrast')
filter_list.addItem('Blur')


picture_box=QLabel('Image will appear here')

# App designs
master_layout=QHBoxLayout()

col1=QVBoxLayout()
col2=QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_list)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)

master_layout.addLayout(col1,20)
master_layout.addLayout(col2,80)

main_window.setLayout(master_layout)

# functions
working_dir=''


# filter files based on extensions
def filter(files,extensions):
    result=[]
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                result.append(file)
    return result

# choose current directory
def getWorkingDir():
    global working_dir
    working_dir=QFileDialog.getExistingDirectory()
    extensions=['.jpg','.png','.jpeg','.svg']
    file_names=filter(os.listdir(working_dir),extensions)
    file_list.clear()
    for file in file_names:
        file_list.addItem(file)

class Editor:
    def __init__(self):
        self.image=None
        self.original=None
        self.file_name=None
        self.save_folder='Edited'

    def load_image(self,file_name):
        self.file_name=file_name
        full_path=os.path.join(working_dir,self.file_name)
        self.image=Image.open(full_path)
        self.original=self.image.copy()

    def save_image(self):
        path=os.path.join(working_dir,self.save_folder)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.makedirs(path)
        full_path=os.path.join(path,self.file_name)
        self.image.save(full_path)

    def show_image(self,path):
        picture_box.hide()
        pixmap=QPixmap(path)
        w,h=picture_box.width(),picture_box.height()
        pixmap=pixmap.scaled(w,h,Qt.KeepAspectRatio)
        picture_box.setPixmap(pixmap)
        picture_box.show()

    def grey(self):
        self.image=self.image.convert("L")
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def left(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def right(self):
        self.image=self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def mirror(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)
    
    def sharpen(self):
        self.image=self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def blur(self):
        self.image=self.image.filter(ImageFilter.BLUR)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def color(self):
        self.image=ImageEnhance.Color(self.image).enhance(1.2)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def contrast(self):
        self.image=ImageEnhance.Contrast(self.image).enhance(1.2)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

    def apply_filter(self,filter_name):
        if filter_name=='Original':
            self.image=self.original.copy()
        elif filter_name=='Left':
            self.image=self.original.transpose(Image.ROTATE_90)
        elif filter_name=='Right':
            self.image=self.original.transpose(Image.ROTATE_270)
        elif filter_name=='Mirror':
            self.image=self.original.transpose(Image.FLIP_LEFT_RIGHT)
        elif filter_name=='Sharpen':
            self.image=self.original.filter(ImageFilter.SHARPEN)
        elif filter_name=='B/W':
            self.image=self.original.convert("L")
        elif filter_name=='Color':
            self.image=ImageEnhance.Color(self.original).enhance(1.2)
        elif filter_name=='Contrast':
            self.image=ImageEnhance.Contrast(self.original).enhance(1.2)
        elif filter_name=='Blur':
            self.image=self.original.filter(ImageFilter.BLUR)
        self.save_image()
        image_path=os.path.join(working_dir,self.save_folder,self.file_name)
        self.show_image(image_path)

def handle_filter():
    if file_list.currentRow()>=0:
        filter_name=filter_list.currentText()
        main.apply_filter(filter_name)

def display_image():
    if file_list.currentRow()>=0:
        file_name=file_list.currentItem().text()
        main.load_image(file_name)
        main.show_image(os.path.join(working_dir,main.file_name))

main=Editor()

btn_folder.clicked.connect(getWorkingDir)
file_list.currentRowChanged.connect(display_image)
filter_list.currentTextChanged.connect(handle_filter)

gray.clicked.connect(main.grey)
btn_left.clicked.connect(main.left)
btn_right.clicked.connect(main.right)
mirror.clicked.connect(main.mirror)
sharpness.clicked.connect(main.sharpen)
blur.clicked.connect(main.blur)
saturation.clicked.connect(main.color)
contrast.clicked.connect(main.contrast)

main_window.show()
app.exec_()

