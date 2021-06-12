from time import sleep
import Config 
from Model import ChannelModel
from SetupModel import SetupModel
from SetupInterface import SetupView

from Database.database import data
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer

class MainModel(QObject):
    startTestButtonNameChanged = pyqtSignal(str)
    setupDialogClosed = pyqtSignal()
    def __init__(self):
        super().__init__()
        d = data()
        channels = d.getChannels()

        self.channelsQuantity = len(channels)
        self.channelModels = []
        
        
        for channel in channels:
            #print(f"{channel['Name']},{channel['PinAbs']},{channel['PinDif']}") 
            self.channelModels.append(ChannelModel(channel['Name'],channel['PinAbs'],channel['PinDif']))

        self.timer = QTimer()
        self.timer.timeout.connect(self.upd)

        self.testStarted = False
        self._startTestButtonName = Config.BUTTON_START_TEST
        self.buttonSetupName = Config.BUTTON_SETUP
        self.buttonManualName = Config.BUTTON_MANUAL
    
    @property
    def startTestButtonName(self):
        return self._startTestButtonName

    @startTestButtonName.setter
    def startTestButtonName(self,value):
        self._startTestButtonName = value
        self.startTestButtonNameChanged.emit(value)

    def startTestButtonPressed(self):
        self.testStarted = not self.testStarted
        self.startDurationTimer(self.testStarted)
        if self.testStarted:
            self.initSensorValuesList()

            self.timer.start(Config.SENSORS_REQUEST_PERIOD)
            self.startTestButtonName = Config.BUTTON_STOP_TEST
        else:
            self.timer.stop()
            self.startTestButtonName = Config.BUTTON_START_TEST
    
    def openSetupDialogButtonPressed(self):
        setupModel = SetupModel()
        setupDialog = SetupView(setupModel)
        setupDialog.exec_()

        self.updateChannelsModel()
        
    def startDurationTimer(self,start):
        for i in range(self.channelsQuantity):
            self.channelModels[i].startDurationTimer(start)

    def initSensorValuesList(self):
        for i in range(self.channelsQuantity):
            self.channelModels[i].initSensorValues()
        
        
    def upd(self):
        for i in range(self.channelsQuantity):
            self.channelModels[i].readSensor('ABS')
            self.channelModels[i].readSensor('DIF')

    def updateChannelsModel(self):       
        for i in range(self.channelsQuantity):
            self.channelModels[i].updateModel()

