from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal,QTimer, pyqtSlot

from ReceiptModel import ReceiptModel

from Database.database import data

class SetupModel(QObject):
    #closeButtonPressed = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setupSaved = True
        self.d = data()
        
        stp = self.d.getSetup()
        self.setupKeys = stp.keys()
        self.setup = {k:str(stp[k]) for k in self.setupKeys if k!='Entry'}

        self.receiptModel = ReceiptModel(enabledReceipts=0)
        
    @pyqtSlot(str,str)
    def onSave(self,name,value):
        print(f'saving {name}={value}')
        self.d.saveSetup(name,value)



    #def onCloseButtonPressed(self):
    #    # что-нибудь сохранить перед выходом
    #    self.closeButtonPressed.emit(self.setupSaved)


if __name__=='__main__':
    d = data()
    r = d.getSetup()
    k = r.keys()
    k2 = [i for i in k if i!='Entry']
    z = zip(r,k)
    print(f'keys={k2}')
    #setup = [list(r1) for r1 in r] 
    setup = {k1:str(r[k1]) for k1 in k if k1!='Entry'}
    print(f'{setup} ')
    for position, name in zip(k, r):
        print(f'{position} = {name}')

    #for k,v in r:
    #    print(f'{k} = {v}')
