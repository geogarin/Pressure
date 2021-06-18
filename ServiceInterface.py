from PyQt5.QtWidgets import QWidget,QDialog,QSizePolicy, QDialogButtonBox, QFormLayout, QLabel,QLineEdit, QGroupBox, QVBoxLayout,QGridLayout,QPushButton,QHBoxLayout,QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,pyqtSlot,pyqtSignal

from ServiceChannel import ServiceChannel


import Config
import stylesheets

class ServiceInterface(QDialog):
    def __init__(self,model):
        super().__init__()
        self.showFullScreen()
        
        
        self.channels = []
        self.mainLayout = QGridLayout()
        
        for i in range(model.channelsQuantity):
            ch = ServiceChannel(model.channelModels[i])
            ch._model.setMasterMode(True)
            self.channels.append(ch)           
            self.mainLayout.addWidget(self.channels[i],1,i,1,1,Qt.AlignTop)
    
        
        closeButton = QPushButton(Config.SETUP_DIALOG_CLOSE)
        closeButton.setStyleSheet(stylesheets.SVC_Button)
        
        self.mainLayout.addWidget(closeButton,3,0,1,model.channelsQuantity,Qt.AlignRight)
        self.setLayout(self.mainLayout)

        closeButton.clicked.connect(self.onCloseButtonPressed)

    def onCloseButtonPressed(self):
        for ch in self.channels:
            ch._model.setMasterMode(False)
        self.close()

        

        


        




