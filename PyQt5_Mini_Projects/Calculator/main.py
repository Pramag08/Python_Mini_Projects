from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QWidget,QVBoxLayout,QLineEdit,QHBoxLayout
from PyQt5.QtGui import QFont


# module Qfont is used to set the font of the text

class Calculator:
    def __init__(self):
        self.app=QApplication([])
        self.main_window=QWidget()
        self.main_window.setWindowTitle('Calculator')
        self.main_window.setGeometry(100,100,400,500)

        self.text_box=QLineEdit()
        self.text_box.setFont(QFont('Helvatica',32))
        self.text_box.setAlignment(Qt.AlignRight)
        self.grid=QGridLayout()
        self.function=QHBoxLayout()

        self.clear=QPushButton('C')
        self.delete=QPushButton('<')
        self.clear.setStyleSheet("QPushButton {background-color: #D4A017 ; color: black; font-size: 20px; font-weight: bold; font: 15pt Comic Sans MS; padding:10px;}")
        self.delete.setStyleSheet("QPushButton {background-color: #D4A017 ; color: black; font-size: 20px; font-weight: bold; font: 15pt Comic Sans MS; padding:10px;}")

        self.row1=self.function.addWidget(self.clear)
        self.row2=self.function.addWidget(self.delete)

        grid_no=4
        L=[[7,8,9,'/'],[4,5,6,'*'],[1,2,3,'-'],[0,'.','+','=']]

        for i in range(grid_no):
            for j in range(grid_no):
                self.button=QPushButton(str(L[i][j]))
                self.button.clicked.connect(self.button_click)
                self.button.setStyleSheet("QPushButton {background-color: #D4A017 ; color: black; font-size: 20px; font-weight: bold; font: 15pt Comic Sans MS; padding:10px;}")
                self.grid.addWidget(self.button,i,j)
        self.master_layout=QVBoxLayout()
        self.master_layout.addWidget(self.text_box)
        self.master_layout.addLayout(self.grid)
        self.master_layout.addLayout(self.function)
        self.master_layout.setContentsMargins(25,25,25,25)


        self.clear.clicked.connect(self.button_click)
        self.delete.clicked.connect(self.button_click)

        self.main_window.setLayout(self.master_layout)
        self.main_window.setStyleSheet("QWidget { background-color: skyblue; }")

        self.main_window.show()
        self.app.exec_()

    def button_click(self):
        button=self.app.sender()
        text=button.text()

        if text=='=':
            symbol=self.text_box.text()
            try:
                res=eval(symbol)
                self.text_box.setText(str(res))
            except Exception as e:
                self.text_box.setText('Error')
        elif text=='C':
            self.text_box.clear()
        elif text=='<':
            # self.text_box.backspace()
            current_value=self.text_box.text()
            self.text_box.setText(current_value[:-1])
        else:
            current_value=self.text_box.text()
            new_value=current_value+text
            self.text_box.setText(new_value)
cal=Calculator()