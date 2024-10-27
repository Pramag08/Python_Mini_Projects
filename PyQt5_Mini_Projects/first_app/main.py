# import Modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

from random import choice
# main app objects
app=QApplication([])
main_window=QWidget()
main_window.setWindowTitle('My First App')
main_window.setGeometry(100,100,600,400)

# c reate all widgets needed for the app
title_text=QLabel("Random Keywords")

text1=QLabel("?")
text2=QLabel("?")
text3=QLabel("?")

button1=QPushButton("click me")
button2=QPushButton("click me")
button3=QPushButton("click me")

mywords=["Python","Java","C++","C#","Ruby","PHP","JavaScript","HTML","CSS","SQL","Swift","Kotlin","R","Go","Perl","Scala","Lua","Rust","TypeScript","Dart","Haskell","Groovy","Julia","Erlang","Clojure","F#","COBOL","Fortran","Ada","Lisp","Scheme","Prolog","Smalltalk","Tcl","Bash","PowerShell","ActionScript","Objective-C","Visual Basic","Delphi","Assembly"]

# all design here
master_layout=QVBoxLayout()

row1=QHBoxLayout()
row2=QHBoxLayout()
row3=QHBoxLayout()

# set final layout to the Main window
row1.addWidget(title_text,alignment=Qt.AlignCenter)

row2.addWidget(text1,alignment=Qt.AlignCenter)
row2.addWidget(text2,alignment=Qt.AlignCenter)
row2.addWidget(text3,alignment=Qt.AlignCenter)

row3.addWidget(button1)
row3.addWidget(button2)
row3.addWidget(button3)

master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)

main_window.setLayout(master_layout)

# create events
def random_word1():
    word=choice(mywords)
    text1.setText(word)
def random_word2():
    word=choice(mywords)
    text2.setText(word)
def random_word3():
    word=choice(mywords)
    text3.setText(word)

    
 
# events
button1.clicked.connect(random_word1)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)

# show and execute our app
main_window.show()
app.exec_()