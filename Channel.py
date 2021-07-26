
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QCheckBox, QFrame,QComboBox,QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout)
from PyQt5.QtCore import Qt,pyqtSlot
import Config
from PressureSensor import PressureSensor
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
        self.testName.setStyleSheet(stylesheets.QComboBoxReceipt)                    
        # Выбор теста <<

        # Тест прочности >>
        self.testStrengthLabel = QLabel(Config.CHECKBOX_STRENGTH_TEST)
        self.testStrengthLabel.setObjectName('Label')
        self.testStrengthLabel.setStyleSheet(stylesheets.QLabelStyle3)
        self.testStrength = SwitchButton(None,'',Config.BUTTON_VALUE_ON,Config.BUTTON_VALUE_OFF,200,50,10,100)
        self.testStrength.setStyleSheet(stylesheets.SwitchButtonStyle)
        self.testStrength.setChecked(self._model.testStrengthOff)
        # Тест прочности <<

        # Тест герметичности >>
        self.testSealedLabel = QLabel(Config.CHECKBOX_SEALED_TEST)
        self.testSealedLabel.setObjectName('Label')
        self.testSealedLabel.setStyleSheet(stylesheets.QLabelStyle3)
        self.testSealed = SwitchButton(None,'',Config.BUTTON_VALUE_ON,Config.BUTTON_VALUE_OFF,200,50,10,100)
        self.testSealed.setStyleSheet(stylesheets.SwitchButtonStyle)
        self.testSealed.setChecked(self._model.testSealedOff)
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
        self.unitOfMeasureDiff = QLabel(PressureSensor.DISPLAY_UNIT_OF_MEASURE['DIF'])
        self.unitOfMeasureDiff.setStyleSheet(stylesheets.QLabelStyle)
        
        self.unitOfMeasureAbs = QLabel(PressureSensor.DISPLAY_UNIT_OF_MEASURE['ABS'])
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
        self.resultStrength.setValue(self._model.resultStrength)
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
        #self.stepDuration.setMaximun(self._model.maxDurationValue)
        self.stepDuration.setMinimun(0)
        #self.stepDuration.setRange(0, self._model.maxDurationValue)
        self.stepDuration.setValue(0)
        # таймер <<

        # результат герметичности >>
        self.resultSealed = RoundedRect()
        self.resultSealed.setValue(self._model.resultSealed)
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
        self.mainLayout.addWidget(self.unitOfMeasureAbs,curRow,curCol)
        self.mainLayout.addWidget(self.unitOfMeasureDiff,curRow,curCol+1)               
        curRow += 1
        self.mainLayout.addWidget(self.measureAbs,curRow,curCol)
        self.mainLayout.addWidget(self.measureDiff,curRow,curCol+1)
        curRow += 1
        #self.mainLayout.addWidget(self.stepDuration,curRow,curCol,1,2,Qt.AlignCenter) 
        self.mainLayout.addLayout(self.res,curRow,curCol,1,2,Qt.AlignCenter) 
        curRow += 1


        self.group.addWidget(self.title)    
        self.group.addWidget(self.frame)
        #self.group.addStretch()

        self.testStrength.clicked.connect(lambda: self._model.inverseTestStrength())
        self.testSealed.clicked.connect(lambda: self._model.inverseTestSealed())

        self._model.resultStrengthChanged.connect(self.onResultStrengthChanged)
        self._model.resultSealedChanged.connect(self.onResultSealedChanged)
       
        self._model.absValueChanged.connect(self.onValueAbsChanged)
        self._model.difValueChanged.connect(self.onValueDifChanged)
        self._model.durationValueChanged.connect(self.onDurationValueChanged)

        self._model.testLabelChanged.connect(self.onTestLabelChanged)
        self._model.stepLabelChanged.connect(self.onStepLabelChanged)

        self._model.durationChanged.connect(self.onDurationChanged)

        self.testName.currentIndexChanged.connect(self.onTestChanged)
        self.onTestChanged(0)

    def onTestChanged(self,i):
        self._model.testNameChanged(self.testName.currentText())

    @pyqtSlot(str)
    def onValueAbsChanged(self,value):       
        self.measureAbs.setText(value)    

    @pyqtSlot(str)
    def onValueDifChanged(self,value):
        self.measureDiff.setText(value)        

    @pyqtSlot(float)
    def onDurationValueChanged(self,value):
        self.stepDuration.setValue(value)

    @pyqtSlot(str)
    def onTestLabelChanged(self,value):
        self.testStage.setText(value)
    
    @pyqtSlot(str)
    def onStepLabelChanged(self,value):
        self.testStep.setText(value)
    
    @pyqtSlot(float)
    def onDurationChanged(self,value):
        self.stepDuration.setRange(0, value)

    @pyqtSlot(int)
    def onResultStrengthChanged(self,value):
        self.resultStrength.setValue(value)

    @pyqtSlot(int)
    def onResultSealedChanged(self,value):
        self.resultSealed.setValue(value)



        
