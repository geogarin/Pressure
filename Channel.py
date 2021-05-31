import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QCheckBox, QFrame,QComboBox,QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout)
from PyQt5.QtCore import Qt,QPoint, QRect, QSize, pyqtSlot
import Config
from Model import ChannelModel
from CircularProgressBar import QRoundProgressBar
from SwitchButton import SwitchButton
from RoundedRect import RoundedRect

import stylesheets

class ChannelView(QWidget):
    def __init__(self,model):
        super().__init__()
        self._model = model
        self.group = QVBoxLayout(self)
        self.group.setSpacing(0)

        self.title = QLabel(self._model.channelName)
        
        self.title.setProperty('type',1)
        self.title.setStyleSheet(stylesheets.HeaderStyle)
        
        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)
        
        # Выбор теста >>
        self.testName = QComboBox()
        self.testName.setModel(self._model.testNameModel)
      
        #self.pal = self.testName.palette()
        #self.pal.setColor(QtGui.QPalette.Button, QtGui.QColor(97,197,255))
        #self.testName.setPalette(self.pal) 
        self.testName.setStyleSheet(stylesheets.QComboBoxReceipt)                    
        # Выбор теста <<

        # Тест прочности >>
        #self.testStrength = QCheckBox(Config.CHECKBOX_STRENGTH_TEST)
        #self.testStrength.setStyleSheet(stylesheets.QCheckBoxStyle2)
        self.testStrengthLabel = QLabel(Config.CHECKBOX_STRENGTH_TEST)
        self.testStrengthLabel.setObjectName('Label')
        self.testStrengthLabel.setStyleSheet(stylesheets.QLabelStyle3)
        self.testStrength = SwitchButton(None,'',Config.BUTTON_VALUE_ON,Config.BUTTON_VALUE_OFF,200,50,10,100)
        self.testStrength.setStyleSheet(stylesheets.SwitchButtonStyle)
        # Тест прочности <<

        # Тест герметичности >>
        #self.testSealed = QCheckBox(Config.CHECKBOX_SEALED_TEST)
        #self.testSealed.setStyleSheet(stylesheets.QCheckBoxStyle2)
        self.testSealedLabel = QLabel(Config.CHECKBOX_SEALED_TEST)
        self.testSealedLabel.setObjectName('Label')
        self.testSealedLabel.setStyleSheet(stylesheets.QLabelStyle3)
        self.testSealed = SwitchButton(None,'',Config.BUTTON_VALUE_ON,Config.BUTTON_VALUE_OFF,200,50,10,100)
        self.testSealed.setStyleSheet(stylesheets.SwitchButtonStyle)
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
        
        self.unitOfMeasureAbs = QLabel(ChannelModel.DISPLAY_UNIT_OF_MEASURE['ABS'])
        self.unitOfMeasureAbs.setStyleSheet(stylesheets.QLabelStyle)
        # единицы измерения <<
        
        # значения с датчиков >>
        self.measureDiff = QLineEdit('')
        self.measureDiff.setReadOnly(True)
        self.measureDiff.setStyleSheet(stylesheets.QLineEditStyle)

        self.measureAbs = QLineEdit('')
        self.measureAbs.setReadOnly(True)
        self.measureAbs.setStyleSheet(stylesheets.QLineEditStyle)
        # значения с датчиков <<

        # результат прочности >>
        self.resultStrength = RoundedRect()
        self.resultStrength.setValue(1)
        # результат прочности <<
        
        # таймер >>
        self.stepDuration = QRoundProgressBar()
        self.stepDuration.setFixedSize(200, 200)

        self.stepDuration.setDataPenWidth(0)
        self.stepDuration.setOutlinePenWidth(0)
        self.stepDuration.setDecimals(2)
        #self.stepDuration.setFormat('%v | %p %')
        self.stepDuration.setFormat('%v')
        # self.stepDuration.resetFormat()
        self.stepDuration.setNullPosition(90)
        self.stepDuration.setBarStyle(QRoundProgressBar.StyleDonut)
        self.stepDuration.setDataColors([(0., QtGui.QColor.fromRgb(255,0,0)), (0.5, QtGui.QColor.fromRgb(255,255,0)), (1., QtGui.QColor.fromRgb(0,255,0))])
        self.stepDuration.setMaximun(5)
        self.stepDuration.setMinimun(0)
        self.stepDuration.setRange(0, 5)
        self.stepDuration.setValue(0)
        # таймер <<

        # результат герметичности >>
        self.resultSealed = RoundedRect()
        self.resultSealed.setValue(-1)
        # результат герметичности <<

        self.res = QHBoxLayout()
        self.res.addWidget(self.resultStrength)
        self.res.addWidget(self.stepDuration)
        self.res.addWidget(self.resultSealed )


        curRow = 0
        curCol = 0
        self.mainLayout = QGridLayout(self.frame) 
        self.mainLayout.addWidget(self.testName,curRow,curCol,1,2) 
        curRow += 1
        #self.mainLayout.addWidget(self.testStrength,curRow,curCol,1,2)
        #curRow += 1
        #self.mainLayout.addWidget(self.testSealed,curRow,curCol,1,2)
        self.mainLayout.addWidget(self.testStrengthLabel,curRow,curCol,1,1,Qt.AlignCenter)
        self.mainLayout.addWidget(self.testSealedLabel,curRow,curCol+1,1,1,Qt.AlignCenter)
        curRow += 1
        self.mainLayout.addWidget(self.testStrength,curRow,curCol)
        self.mainLayout.addWidget(self.testSealed,curRow,curCol+1)
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
        #self.mainLayout.addWidget(self.stepDuration,curRow,curCol,1,2,Qt.AlignCenter) 
        self.mainLayout.addLayout(self.res,curRow,curCol,1,2,Qt.AlignCenter) 
        curRow += 1


        self.group.addWidget(self.title)    
        self.group.addWidget(self.frame)
        self.group.addStretch()
        
        self._model.absValueChanged.connect(self.onValueAbsChanged)
        self._model.difValueChanged.connect(self.onValueDifChanged)
        self._model.durationValueChanged.connect(self.onDurationValueChanged)

    @pyqtSlot(float)
    def onValueAbsChanged(self,value):       
        self.measureAbs.setText(str.format("{:.{}f}",value,Config.ABS_PRESSURE_ROUNDING_PRECISION))    

    @pyqtSlot(float)
    def onValueDifChanged(self,value):
        self.measureDiff.setText(str.format("{:.{}f}",value,Config.DIF_PRESSURE_ROUNDING_PRECISION))        

    @pyqtSlot(float)
    def onDurationValueChanged(self,value):
        self.stepDuration.setValue(value)

        
