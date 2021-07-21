from time import sleep
import Config 
from Model import ChannelModel
from SetupModel import SetupModel
from SetupInterface import SetupView
from ServiceInterface import ServiceInterface
from CommonControl import CommonControl

from Database.database import data
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer

class MainModel(QObject):
    startTestButtonNameChanged = pyqtSignal(str)
    setupDialogClosed = pyqtSignal()
    buttonsVisibleChanged = pyqtSignal()
    def __init__(self):
        super().__init__()
        CommonControl.closeInputPressure()
        self.db = data()
        channels = self.db.getChannels()

        self.channelsQuantity = len(channels)
        self.channelModels = []
        
        channelIndex = 1
        for channel in channels:
            #print(f"{channel['Name']},{channel['PinAbs']},{channel['PinDif']}") 
            self.channelModels.append(ChannelModel(channel['Name'],channel['PinAbs'],channel['PinDif'],channel['I2CAddress'],channelIndex))
            channelIndex += 1

        self.timer = QTimer()
        self.timer.timeout.connect(self.upd)

        self.testStarted = False
        self._startTestButtonName = Config.BUTTON_START_TEST
        self.buttonSetupName = Config.BUTTON_SETUP
        self.buttonSetupVisible = False
        self.buttonManualName = Config.BUTTON_MANUAL
        self.buttonManualVisible = False

        self.checkUsbTimer = QTimer()
        self.checkUsbTimer.timeout.connect(self.onCheckUsbTimer)
        self.checkUsbTimer.start(Config.USB_CHECK_PERIOD)
    
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

    def openServiceDialogButtonPressed(self):
        serviceInterface = ServiceInterface(self)
        serviceInterface.exec_()
        #print('after service')
        
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

    def onCheckUsbTimer(self):
        isSetup = self.db.isSetupFlashInstalled()
        isMaster = self.db.isMasterFlashInstalled()

        if (isSetup!=self.buttonSetupVisible) or (isMaster!=self.buttonManualVisible):
            self.buttonSetupVisible = isSetup
            self.buttonManualVisible = isMaster
            self.buttonsVisibleChanged.emit()




