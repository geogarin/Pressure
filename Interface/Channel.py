import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout)
from PyQt5.QtCore import pyqtSlot
import Config

import stylesheets

class ChannelView(QWidget):
    def __init__(self,name,model):
        super().__init__()
        self._model = model

        self.group = QGroupBox(name)
        self.group.setCheckable(False)
        #self.group.setStyleSheet(stylesheets.QGroupBoxStyle)

        self.measureFont = QtGui.QFont("Times",35)

        
        self.measureAbs = QLineEdit('')
        self.measureAbs.setReadOnly(True)
        self.measureAbs.setFont(self.measureFont)
        

        self.measureDiff = QLineEdit('')
        self.measureDiff.setReadOnly(True)
        self.measureDiff.setFont(self.measureFont)

        self.measureLay = QHBoxLayout()
        self.measureLay.addWidget(self.measureAbs)
        self.measureLay.addStretch(1)
        self.measureLay.addWidget(self.measureDiff)


        self.button = QPushButton(self._model.butName)
        self.button.setFont(self.measureFont)


        self.lay = QVBoxLayout()
        
        #self.lay.addWidget(self.measureAbs)
        #self.lay.addWidget(self.measureLay)

        self.mainLayout = QGridLayout()



        self.lay.addWidget(self.button)
        self.lay.addStretch(1)
        #self.group.setLayout(self.lay)

        self.mainLayout.addLayout(self.measureLay,0,0,3,1)
        self.mainLayout.addLayout(self.lay,3,0)
        #self.mainLayout.addWidget(self.button,1,0)
   
        self.group.setLayout(self.mainLayout)
        #self.setLayout(self.lay)

        self._model.absValueChanged.connect(self.onValueAbsChanged)
        self._model.difValueChanged.connect(self.onValueDifChanged)


        self._model.butNameChanged.connect(self.onButtonNameChanged)
        self.button.clicked.connect(lambda: self._model.buttonPressed())

    @pyqtSlot(float)
    def onValueAbsChanged(self,value):
        #self.measureAbs.setText(str(value))
        #self.measureAbs.setText("{:.2f}".format(value))
        self.measureAbs.setText(str.format("{:.{}f}",value,Config.ABS_PRESSURE_ROUNDING_PRECISION))    

    @pyqtSlot(float)
    def onValueDifChanged(self,value):
        #self.measureDiff.setText(str(value))
        self.measureDiff.setText(str.format("{:.{}f}",value,Config.DIF_PRESSURE_ROUNDING_PRECISION))        


    @pyqtSlot(str)
    def onButtonNameChanged(self,value):
        self.button.setText(value)
        
