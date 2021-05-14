from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer



class SetupModel(QObject):
    closeButtonPressed = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setupSaved = True

    def onSaveButtonPressed(self):
        print('saving')

    def onCloseButtonPressed(self):
        # что-нибудь сохранить перед выходом
        self.closeButtonPressed.emit(self.setupSaved)

