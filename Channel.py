import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QCheckBox, QFrame,QComboBox,QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout)
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
        
        self.title.setProperty('type',1)
        self.title.setStyleSheet(stylesheets.HeaderStyle)
        
        #self.title.style().unpolish(self.title)
        #self.title.style().polish(self.title)
        


        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)
        
        self.measureFont = QtGui.QFont("Times",35)
        
        
        

        # Выбор теста >>
        self.testName = QComboBox()
        self.testName.addItems(["Ubuntu", "Mandriva",
                        "Fedora", "Arch", "Gentoo"])
       # self.testName.setFont(self.measureFont)  

        #self.pal = self.testName.palette()
        #self.pal.setColor(QtGui.QPalette.Button, QtGui.QColor(97,197,255))
        #self.testName.setPalette(self.pal) 
        self.testName.setStyleSheet(stylesheets.QComboBoxReceipt)                    
        # Выбор теста <<

        # Тест прочности >>
        self.testStrength = QCheckBox(Config.CHECKBOX_STRENGTH_TEST)
        self.testStrength.setStyleSheet(stylesheets.QCheckBoxStyle2)
        #self.testStrength.setFont(self.measureFont)
        #self.testStrength.toggled(True)
        # Тест прочности <<

        # Тест герметичности >>
        self.testSealed = QCheckBox(Config.CHECKBOX_SEALED_TEST)
        self.testSealed.setStyleSheet(stylesheets.QCheckBoxStyle2)
        #self.testSealed.setFont(self.measureFont)
        #self.testSealed.toggled(True)
        # Тест герметичности <<

        # Название теста >>
        self.testStage = QLabel()
        self.testStage.setStyleSheet(stylesheets.QLabelStyle2)
        # Название теста <<

        # Название этапа >>
        self.testStep = QLabel()
        self.testStep.setStyleSheet(stylesheets.QLabelStyle2)
        # Название этапа <<

        # единицы измерения >>
        self.unitOfMeasureDiff = QLabel(ChannelModel.DISPLAY_UNIT_OF_MEASURE['DIF'])
        self.unitOfMeasureDiff.setStyleSheet(stylesheets.QLabelStyle)
        #self.unitOfMeasureDiff.setFont(self.measureFont)

        self.unitOfMeasureAbs = QLabel(ChannelModel.DISPLAY_UNIT_OF_MEASURE['ABS'])
        self.unitOfMeasureAbs.setStyleSheet(stylesheets.QLabelStyle)
        #self.unitOfMeasureAbs.setFont(self.measureFont)

        #self.unitOfMeasureLay = QHBoxLayout()
        #self.unitOfMeasureLay.addWidget(self.unitOfMeasureDiff)
        #self.unitOfMeasureLay.addWidget(self.unitOfMeasureAbs)
        # единицы измерения <<
        

        # значения с датчиков >>
        self.measureDiff = QLineEdit('')
        self.measureDiff.setReadOnly(True)
        self.measureDiff.setStyleSheet(stylesheets.QLineEditStyle)
        #self.measureDiff.setFont(self.measureFont)

        self.measureAbs = QLineEdit('')
        self.measureAbs.setReadOnly(True)
        self.measureAbs.setStyleSheet(stylesheets.QLineEditStyle)
        #self.measureAbs.setFont(self.measureFont)
        # значения с датчиков <<
        curRow = 0
        curCol = 0
        self.mainLayout = QGridLayout(self.frame) 
        self.mainLayout.addWidget(self.testName,curRow,curCol,1,2) 
        curRow += 1
        self.mainLayout.addWidget(self.testStrength,curRow,curCol,1,2)
        curRow += 1
        self.mainLayout.addWidget(self.testSealed,curRow,curCol,1,2)
        curRow += 1
        self.mainLayout.addWidget(self.testStage,curRow,curCol,1,2)
        curRow += 1
        self.mainLayout.addWidget(self.testStep,curRow,curCol,1,2)
        curRow += 1
        self.mainLayout.addWidget(self.unitOfMeasureDiff,curRow,curCol)
        self.mainLayout.addWidget(self.unitOfMeasureAbs,curRow,curCol+1)
        curRow += 1
        self.mainLayout.addWidget(self.measureDiff,curRow,curCol)
        self.mainLayout.addWidget(self.measureAbs,curRow,curCol+1)
        curRow += 1


        self.group.addWidget(self.title)    
        self.group.addWidget(self.frame)
        self.group.addStretch()
        
        
        
        
        

        self._model.absValueChanged.connect(self.onValueAbsChanged)
        self._model.difValueChanged.connect(self.onValueDifChanged)


        #self._model.butNameChanged.connect(self.onButtonNameChanged)
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
        
