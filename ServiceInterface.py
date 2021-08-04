from PyQt5.QtWidgets import QWidget,QDialog,QSizePolicy, QDialogButtonBox, QFormLayout, QLabel,QLineEdit, QGroupBox, QVBoxLayout,QGridLayout,QPushButton,QHBoxLayout,QMessageBox
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
        
        
        self.channels = []
        self.mainLayout = QGridLayout()
        
        # установка напряжения >>
        self.labelSetVoltage = QLabel(Config.SVC_SET_VOLTAGE)
        self.labelSetVoltage.setStyleSheet(stylesheets.SDS_Label)

        self.setVoltage = QLineEditVK()
        self.setVoltage.keyboard = VirtualKeyboard(self,int(model.setup['KeyboardButtonSize']),True) 
        self.setVoltage.setStyleSheet(stylesheets.SDS_LineEdit)
        self.setVoltage.name = 'SetVoltage'
        self.setVoltage.setText('0')
        #self.setVoltage.setFixedWidth(Config.SETUP_DIALOG_LINE_EDIT_FIELD_WIDTH)
        # установка напряжения <<
        curRow = 2

        self.mainLayout.addWidget(self.labelSetVoltage,curRow,1)
        self.mainLayout.addWidget(self.setVoltage,curRow,2)        
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


        self.setVoltage.editDone.connect(self.onSetVoltage)

    def onSetVoltage(self):
        val = int(self.setVoltage.text())
        if (val<0): val=0 
        if (val>100): val=100     
        self.setVoltage.setText(str(val))
        #self._model.setVoltage()

    def onCloseButtonPressed(self):
        m = mcp4725()
        m.setNormalizedValue(0)
        for ch in self.channels:
            ch._model.setMasterMode(False)
        self.close()

        

        


        




