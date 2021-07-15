from Channel import ChannelView
from MainModel import MainModel
from Config import BUTTON_START_TEST
#from stylesheets import ButtonStartStyle,ButtonStopStyle,MenuButtonStyle
import stylesheets

from PyQt5.QtWidgets import QDialog,QWidget,QGridLayout,QProgressBar,QPushButton,QHBoxLayout
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,pyqtSlot

class MainInterface(QWidget):
    def __init__(self,model):
        super().__init__()
        self._model = model
        self.initUI()
        
    def initUI(self):
        self.showFullScreen()

        self.channels = []
        self.mainLayout = QGridLayout()

        self.menu = QHBoxLayout()


        self.setupButton = QPushButton(self._model.buttonSetupName)
        self.setupButton.setStyleSheet(stylesheets.SVC_Button) #MenuButtonStyle)
        self.manualButton = QPushButton(self._model.buttonManualName)
        self.manualButton.setStyleSheet(stylesheets.SVC_Button) #MenuButtonStyle)
        self.setButtonsVisible()

        self.menu.addWidget(self.setupButton)
        self.menu.addWidget(self.manualButton)

        self.mainLayout.addLayout(self.menu,0,0,1,4,Qt.AlignRight|Qt.AlignVCenter)

        for i in range(self._model.channelsQuantity):
            #print(i)
            ch = ChannelView(self._model.channelModels[i])
            self.channels.append(ch)           
            self.mainLayout.addWidget(self.channels[i],2,i,1,1,Qt.AlignVCenter)


        self.startTestButton = QPushButton(self._model.startTestButtonName)
        self.startTestButton.setObjectName("StartTestButton")
        self.startTestButton.setStyleSheet(stylesheets.ButtonStartStyle)
 
 
        self.mainLayout.addWidget(self.startTestButton,3,0,1,self._model.channelsQuantity)
        
        self.setLayout(self.mainLayout)

        self._model.startTestButtonNameChanged.connect(self.onStartTestButtonNameChanged)
        self._model.buttonsVisibleChanged.connect(self.setButtonsVisible)
        self.startTestButton.clicked.connect(lambda: self._model.startTestButtonPressed())
        self.setupButton.clicked.connect(lambda: self._model.openSetupDialogButtonPressed())
        self.manualButton.clicked.connect(lambda: self._model.openServiceDialogButtonPressed())
        
    @pyqtSlot(str)
    def onStartTestButtonNameChanged(self,value):
        self.startTestButton.setText(value)
        if (value == BUTTON_START_TEST):
            self.startTestButton.setStyleSheet(stylesheets.ButtonStartStyle)
        else:
            self.startTestButton.setStyleSheet(stylesheets.ButtonStopStyle)
    
    @pyqtSlot()
    def setButtonsVisible(self):
        self.setupButton.setVisible(self._model.buttonSetupVisible)
        self.manualButton.setVisible(self._model.buttonManualVisible)

    