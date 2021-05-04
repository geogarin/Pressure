import Config 
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer

class MainModel(QObject):
    startTestButtonNameChanged = pyqtSignal(str)
    def __init__(self,channelsQty):
        super().__init__()
        self.channelsQuantity = channelsQty
        self.channelModels = [None] * channelsQty
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.upd)

        self.testStarted = False
        self._startTestButtonName = Config.BUTTON_START_TEST
    
    @property
    def startTestButtonName(self):
        return self._startTestButtonName

    @startTestButtonName.setter
    def startTestButtonName(self,value):
        self._startTestButtonName = value
        self.startTestButtonNameChanged.emit(value)

    def startTestButtonPressed(self):
        self.testStarted = not self.testStarted
        if self.testStarted:
            self.timer.start(100)
            self.startTestButtonName = Config.BUTTON_STOP_TEST
            #self.readSensor('ABS')
        else:
            self.timer.stop()
            self.startTestButtonName = Config.BUTTON_START_TEST
    
    def upd(self):
        for i in range(self.channelsQuantity):
            self.channelModels[i].readSensor('ABS')
            #self.channelModels[i].readSensor('DIF')