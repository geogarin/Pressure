from PyQt5.QtWidgets import QSlider, QWidget,QDialog, QFrame, QLabel,QLineEdit, QGroupBox, QVBoxLayout,QGridLayout,QPushButton,QHBoxLayout,QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,pyqtSlot,pyqtSignal

from ServiceChannel import ServiceChannel
from VirtualKeyboard import VirtualKeyboard
from QLineEditVK import QLineEditVK
from Dac import mcp4725


import Config
import stylesheets

class ServiceInterface(QDialog):
    def __init__(self,model):
        super().__init__()
        self.showFullScreen()
        
        
        
        
        # установка напряжения >>
        self.widg = QWidget()

        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)


        self.voltage = QLineEdit('')
        self.voltage.setReadOnly(True)
        self.voltage.setStyleSheet(stylesheets.QVoltageStyle)
        self.voltage.setAlignment(Qt.AlignCenter)
        self.voltage.setText('0')

        self.voltageSlider = QSlider(Qt.Horizontal)
        self.voltageSlider.setRange(0,100)
        self.voltageSlider.setValue(0)
        self.voltageSlider.setFixedWidth(500)
        self.voltageSlider.setStyleSheet(stylesheets.QVoltageSlider)

        self.group = QVBoxLayout(self.widg)
        self.group.setSpacing(0)

        self.title = QLabel(Config.SVC_SET_VOLTAGE)
        self.title.setProperty('type',1)
        self.title.setStyleSheet(stylesheets.HeaderStyle)
        
        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)
        self.group.addWidget(self.title)    
        self.group.addWidget(self.frame)
        self.widg.mainLayout = QGridLayout(self.frame)

        curRow = 1
        self.widg.mainLayout.addWidget(self.voltage,curRow,0,Qt.AlignHCenter)
        curRow += 1
        self.widg.mainLayout.addWidget(self.voltageSlider,curRow,0,Qt.AlignHCenter) 
        self.model = model 
        self.model.setInputVoltage(0)      
        # установка напряжения <<

        self.channels = []
        self.mainLayout = QGridLayout()

        curRow = 1
        self.mainLayout.addWidget(self.widg,curRow,0,1,model.channelsQuantity)
        curRow += 1

        

        for i in range(model.channelsQuantity):
            ch = ServiceChannel(model.channelModels[i])
            ch._model.setMasterMode(True)
            self.channels.append(ch)           
            self.mainLayout.addWidget(self.channels[i],curRow,i,1,1,Qt.AlignTop)
        curRow += 2
        
        closeButton = QPushButton(Config.SETUP_DIALOG_CLOSE)
        closeButton.setStyleSheet(stylesheets.SVC_Button)
        #curRow += 1
        
        self.mainLayout.addWidget(closeButton,curRow,0,1,model.channelsQuantity,Qt.AlignRight)
        self.setLayout(self.mainLayout)

        closeButton.clicked.connect(self.onCloseButtonPressed)


        self.voltageSlider.valueChanged.connect(self.onSetVoltage)

    def onSetVoltage(self,value):    
        self.voltage.setText(str(value))
        self.model.setInputVoltage(value)
        #print(f'val={value}')
    
    def onCloseButtonPressed(self):
        self.model.setInputVoltage(0)
        
        for ch in self.channels:
            ch._model.setMasterMode(False)
        self.close()

        

        


        




