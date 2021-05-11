import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QFrame, QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout)
from PyQt5.QtCore import Qt,QPoint, QRect, QSize, pyqtSlot
import Config
from Model import ChannelModel

import stylesheets

class ChannelView(QWidget):
    def __init__(self,model):
        super().__init__()
        self._model = model

        #self.group = QGroupBox(self._model.channelName)
        self.group = QVBoxLayout(self)
        self.group.setSpacing(0)

        self.title = QLabel(self._model.channelName)
        self.title.setStyleSheet(stylesheets.QLabelStyle)

        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.QFrameStyle)
        #self.group.setCheckable(False)
        
        #self.mainLayout.setGeometry(QRect(QPoint(0,0),QSize(200,100)))
        #self.group.setStyleSheet(stylesheets.QGroupBoxStyle)

        self.measureFont = QtGui.QFont("Times",35)

        # единицы измерения >>
        self.unitOfMeasureDiff = QLabel(ChannelModel.DISPLAY_UNIT_OF_MEASURE['DIF'])
        #self.unitOfMeasureDiff.setFrameStyle(QLabel.Box)
        #self.unitOfMeasureDiff.setReadOnly(True)
        self.unitOfMeasureDiff.setFont(self.measureFont)

        self.unitOfMeasureAbs = QLabel(ChannelModel.DISPLAY_UNIT_OF_MEASURE['ABS'])
        #self.unitOfMeasureAbs.setFrameStyle(QLabel.Box)
        #self.unitOfMeasureAbs.setReadOnly(True)
        self.unitOfMeasureAbs.setFont(self.measureFont)

        self.unitOfMeasureLay = QHBoxLayout()
        self.unitOfMeasureLay.addWidget(self.unitOfMeasureDiff)
        #self.unitOfMeasureLay.addStretch(1)
        self.unitOfMeasureLay.addWidget(self.unitOfMeasureAbs)
        # единицы измерения <<
        

        # значения с датчиков >>
        self.measureDiff = QLineEdit('')
        self.measureDiff.setReadOnly(True)
        self.measureDiff.setFont(self.measureFont)

        self.measureAbs = QLineEdit('')
        self.measureAbs.setReadOnly(True)
        self.measureAbs.setFont(self.measureFont)
        # значения с датчиков <<
        
        #self.measureLay = QHBoxLayout()
        #self.measureLay.addWidget(self.measureDiff)
        #self.measureLay.addStretch(1)
        #self.measureLay.addWidget(self.measureAbs)


        #self.button = QPushButton(self._model.butName)
        #self.button.setFont(self.measureFont)


        
        #self.lay = QHBoxLayout()
        
        #self.lay.addWidget(self.measureAbs)
        #self.lay.addWidget(self.measureLay)

        self.mainLayout = QGridLayout(self.frame)
           
        self.mainLayout.addWidget(self.unitOfMeasureDiff,0,0,Qt.AlignTop)
        self.mainLayout.addWidget(self.unitOfMeasureAbs,0,1,Qt.AlignTop)
        self.mainLayout.addWidget(self.measureDiff,1,0,Qt.AlignTop)
        self.mainLayout.addWidget(self.measureAbs,1,1,Qt.AlignTop)
        
        
        #self.lay = QVBoxLayout()
        #self.lay.addStretch(1)
        #self.mainLayout.addLayout(self.lay,2,0)
        

        #self.group.setLayout(self.mainLayout)
        self.group.addWidget(self.title)    
        self.group.addWidget(self.frame)
        self.group.addStretch()
        #self.group.addLayout(self.mainLayout)
        
        
        
        

        self._model.absValueChanged.connect(self.onValueAbsChanged)
        self._model.difValueChanged.connect(self.onValueDifChanged)


        self._model.butNameChanged.connect(self.onButtonNameChanged)
        #self.button.clicked.connect(lambda: self._model.buttonPressed())

    @pyqtSlot(float)
    def onValueAbsChanged(self,value):       
        self.measureAbs.setText(str.format("{:.{}f}",value,Config.ABS_PRESSURE_ROUNDING_PRECISION))    

    @pyqtSlot(float)
    def onValueDifChanged(self,value):
        self.measureDiff.setText(str.format("{:.{}f}",value,Config.DIF_PRESSURE_ROUNDING_PRECISION))        


    @pyqtSlot(str)
    def onButtonNameChanged(self,value):
        self.button.setText(value)
        
