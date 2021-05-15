from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer

from Database.database import data

class SetupModel(QObject):
    closeButtonPressed = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setupSaved = True
        self.d = data()
        
        r = self.d.getSetup()
        self.setup = [list(r1) for r1 in r] 

        self.setupKeys = r.keys()

    def onSaveButtonPressed(self):
        print('saving')

    def onCloseButtonPressed(self):
        # что-нибудь сохранить перед выходом
        self.closeButtonPressed.emit(self.setupSaved)


if __name__=='__main__':
    d = data()
    r = d.getSetup()
    k = r.keys()
    z = zip(r,k)
    setup = [list(r1) for r1 in r] 
    print()
    for position, name in zip(k, r):
        print(f'{position} = {name}')

    #for k,v in r:
    #    print(f'{k} = {v}')
