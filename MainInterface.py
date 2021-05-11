from Channel import ChannelView
from MainModel import MainModel

from PyQt5.QtWidgets import QDialog,QWidget,QGridLayout,QProgressBar,QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot

class MainInterface(QWidget):
    def __init__(self,model):
        super().__init__()
        self._model = model
        self.initUI()

    def initUI(self):
        self.showFullScreen()

        self.channels = []
        self.mainLayout = QGridLayout()

        self.bu = QPushButton('Set')
        self.mainLayout.addWidget(self.bu,1,0,1,1)

        for i in range(self._model.channelsQuantity):
            #print(i)
            #self._model.channelModels[i] = ChannelModel(PINS_ABS[i],PINS_DIF[i])
            ch = ChannelView(self._model.channelModels[i])
            self.channels.append(ch)
            #self.mainLayout.addWidget(self.channels[i].group,2,i,1,1)
            #self.mainLayout.addLayout(self.channels[i].group,2,i,1,1)
            self.mainLayout.addWidget(self.channels[i],2,i,1,1)

        #self.progressBar = QProgressBar()
        #self.progressBar.setRange(0, 10000)
        #self.progressBar.setValue(5000) 

        self.font = QtGui.QFont("Times",75)
        self.startTestButton = QPushButton(self._model.startTestButtonName)
        self.startTestButton.setFont(self.font)


        self.mainLayout.addWidget(self.startTestButton,3,0,1,self._model.channelsQuantity)
        #self.mainLayout.addWidget(self.progressBar,5,0,1,channelsQty)
        
        self.setLayout(self.mainLayout)

        self._model.startTestButtonNameChanged.connect(self.onStartTestButtonNameChanged)
        self.startTestButton.clicked.connect(lambda: self._model.startTestButtonPressed())

    @pyqtSlot(str)
    def onStartTestButtonNameChanged(self,value):
        self.startTestButton.setText(value)