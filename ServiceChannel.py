
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QDialog,QSizePolicy, QFrame,QComboBox,QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout,QSpacerItem)
from PyQt5.QtCore import Qt,pyqtSlot,QTimer
import Config
from PressureSensor import PressureSensor
from CircularProgressBar import QRoundProgressBar
from SwitchButton import SwitchButton
from RoundedRect import RoundedRect
import stylesheets

class ServiceChannel(QWidget):
    def __init__(self,model):
        super().__init__()
        self._model = model

        self.group = QVBoxLayout(self)
        self.group.setSpacing(0)

        self._model.initRoundingPrecision(2,2)
    
        self.title = QLabel(Config.SVC_SERVICE_NAME+' '+self._model.channelName)
        
        self.title.setProperty('type',1)
        self.title.setStyleSheet(stylesheets.HeaderStyle)
        
        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)
        
        # значения с датчиков >>
        self.measureDiff = QLineEdit('')
        self.measureDiff.setReadOnly(True)
        self.measureDiff.setStyleSheet(stylesheets.QLineEditStyle)

        self.measureAbs = QLineEdit('')
        self.measureAbs.setReadOnly(True)
        self.measureAbs.setStyleSheet(stylesheets.QLineEditStyle)
        # значения с датчиков <<

        self.labelValve1 = QLabel(Config.SVC_VALVE1_NAME)
        self.labelValve1.setObjectName('Label')
        self.labelValve1.setStyleSheet(stylesheets.QLabelStyle3)
        self.valve1 = SwitchButton(None,'',Config.SVC_VALVE_CLOSED,Config.SVC_VALVE_OPEN,200,50,10,100)       
        self.valve1.setStyleSheet(stylesheets.SwitchButtonStyle)

        self.labelValve2 = QLabel(Config.SVC_VALVE2_NAME)
        self.labelValve2.setObjectName('Label')
        self.labelValve2.setStyleSheet(stylesheets.QLabelStyle3)
        self.valve2 = SwitchButton(None,'',Config.SVC_VALVE_CLOSED,Config.SVC_VALVE_OPEN,200,50,10,100)
        self.valve2.setStyleSheet(stylesheets.SwitchButtonStyle)
        #self.valve2.setEnabled(False)
        
        self.labelValve3 = QLabel(Config.SVC_VALVE3_NAME)
        self.labelValve3.setObjectName('Label')
        self.labelValve3.setStyleSheet(stylesheets.QLabelStyle3)
        self.valve3 = SwitchButton(None,'',Config.SVC_VALVE_CLOSED,Config.SVC_VALVE_OPEN,200,50,10,100)
        self.valve3.setStyleSheet(stylesheets.SwitchButtonStyle)

        self.labelValve4 = QLabel(Config.SVC_VALVE4_NAME)
        self.labelValve4.setObjectName('Label')
        self.labelValve4.setStyleSheet(stylesheets.QLabelStyle3)
        self.valve4 = SwitchButton(None,'',Config.SVC_VALVE_CLOSED,Config.SVC_VALVE_OPEN,200,50,10,100)
        self.valve4.setStyleSheet(stylesheets.SwitchButtonStyle)
        for i in range(1,5):
            self.updateValves(i)


        self.zeroSensor = QPushButton(Config.SVC_ZERO_SENSOR)
        self.zeroSensor.setStyleSheet(stylesheets.SVC_Button)

        self.resetZeroSensor = QPushButton(Config.SVC_RESET_ZERO_SENSOR)
        self.resetZeroSensor.setStyleSheet(stylesheets.SVC_Button)

        self.spacer = QSpacerItem(10,200)


        
        
        


        """
        self.res = QHBoxLayout()
        self.res.addWidget(self.resultStrength)
        self.res.addWidget(self.stepDuration)
        self.res.addWidget(self.resultSealed )
        """

        curRow = 0
        curCol = 0
        self.mainLayout = QGridLayout(self.frame) 
        #self.mainLayout.addWidget(self.testName,curRow,curCol,1,2) 
        #curRow += 1
        """
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
        """
        self.mainLayout.addWidget(self.measureDiff,curRow,curCol)
        self.mainLayout.addWidget(self.measureAbs,curRow,curCol+1)
        curRow += 1

        self.mainLayout.addWidget(self.labelValve1,curRow,curCol)
        self.mainLayout.addWidget(self.labelValve4,curRow,curCol+1)
        curRow += 1

        self.mainLayout.addWidget(self.valve1,curRow,curCol)
        self.mainLayout.addWidget(self.valve4,curRow,curCol+1)
        curRow += 1

        self.mainLayout.addWidget(self.labelValve3,curRow,curCol)
        self.mainLayout.addWidget(self.labelValve2,curRow,curCol+1)
        curRow += 1

        self.mainLayout.addWidget(self.valve3,curRow,curCol)
        self.mainLayout.addWidget(self.valve2,curRow,curCol+1)
        curRow += 1

        self.mainLayout.addItem(self.spacer,curRow,curCol,1,2)
        curRow += 1

        self.mainLayout.addWidget(self.zeroSensor,curRow,curCol,1,2)
        curRow += 1

        self.mainLayout.addWidget(self.resetZeroSensor,curRow,curCol,1,2)
        curRow += 1

        """
        curRow += 1
        #self.mainLayout.addWidget(self.stepDuration,curRow,curCol,1,2,Qt.AlignCenter) 
        self.mainLayout.addLayout(self.res,curRow,curCol,1,2,Qt.AlignCenter) 
        curRow += 1
        """

        self.group.addWidget(self.title)    
        self.group.addWidget(self.frame)
        #self.group.addStretch()

        g=QtGui.QGuiApplication.primaryScreen().geometry()
        #print(g)       
        #self.setMinimumHeight(0.9*g.height())

        self.valve1.clicked.connect(lambda: self._model.inverseValve(1))
        self.valve2.clicked.connect(lambda: self._model.inverseValve(2))
        self.valve3.clicked.connect(lambda: self._model.inverseValve(3))
        self.valve4.clicked.connect(lambda: self._model.inverseValve(4))

        self.resetZeroSensor.clicked.connect(lambda: self._model.resetZeroSensors())
        self.zeroSensor.clicked.connect(lambda: self._model.zeroSensors())
        
        self._model.absValueChanged.connect(self.onValueAbsChanged)
        self._model.difValueChanged.connect(self.onValueDifChanged)
        self._model.valveStateChanged.connect(self.updateValves)

    @pyqtSlot(int)    
    def updateValves(self,value):
        if (value==1):
            self.valve1.setChecked(self._model.isOpenValve1)
        if (value==2):
            self.valve2.setChecked(self._model.isOpenValve2)
        if (value==3):
            self.valve3.setChecked(self._model.isOpenValve3)
        if (value==4):
            self.valve4.setChecked(self._model.isOpenValve4)

        self.valve2.setEnabled(self._model.isEnabledValve2)

    @pyqtSlot(str)
    def onValueAbsChanged(self,value):       
        self.measureAbs.setText(value)    

    @pyqtSlot(str)
    def onValueDifChanged(self,value):
        self.measureDiff.setText(value)        



        
