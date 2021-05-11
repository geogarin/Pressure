from PyQt5.QtWidgets import QGroupBox,QPushButton,QDial,QSlider,QVBoxLayout,QCheckBox
from PyQt5.QtCore import Qt,QTimer
import random
import stylesheets


class Channel():
    def __init__(self,name):
        
        self.group = QGroupBox(name)
        self.group.setCheckable(False)
        self.group.setStyleSheet(stylesheets.QGroupBoxStyle)

        self.button = QPushButton("N")
        #self.button.setFixedHeight(200)
        #self.button.setFixedWidth(200)
        self.button.setStyleSheet(stylesheets.QPushButtonReceipt)

        self.button2 = QPushButton("Hello")
        self.button2.setStyleSheet(stylesheets.QPushButton3)

        self.checkBox = QCheckBox('qqq')
        
        self.checkBox.setStyleSheet(stylesheets.QCheckBoxStyle)

        
        #self.dial = QDial(self.group)
        #self.dial.setValue(random.randint(0,100))
        #self.dial.setNotchesVisible(True)

        self.slider = QSlider(Qt.Horizontal, self.group)
        self.slider.setValue(random.randint(0,100))

        lay = QVBoxLayout()
        lay.addWidget(self.button)
        lay.addWidget(self.button2)
        lay.addWidget(self.checkBox)
        #lay.addWidget(self.dial)
        lay.addWidget(self.slider)

        self.dx1=1
        self.dx2=1
        self.timer = QTimer()
        self.timer.timeout.connect(self.processTimer)
        self.timer.start(random.randint(20,70))
        
        self.group.setLayout(lay)

    def getGroup(self)->QGroupBox:
        return self.group

    def processTimer(self):
        n = self.slider.value()
        ma = self.slider.maximum()
        mi = self.slider.minimum()
        #print(f'n={n}, ma={ma}, mi={mi}')
        if n >= ma: self.dx1=-1
        if n<=mi: self.dx1=1
        self.slider.setValue(n+self.dx1)

"""
        n = self.dial.value()
        ma = self.dial.maximum()
        mi = self.dial.minimum()
        if n >= ma: self.dx2=-1
        if n<=mi: self.dx2=1
        self.dial.setValue(n+self.dx2)
"""



    
