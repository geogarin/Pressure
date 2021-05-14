from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer


class SetupModel(QObject):
    closeButtonPressed = pyqtSignal()
    def __init__(self):
        super().__init__()

    

    def onCloseButtonPressed(self):
        # что-нибудь сохранить перед выходом
        
        self.closeButtonPressed.emit()

