from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal, pyqtSlot,QAbstractListModel,QModelIndex

from Database.database import data

class ReceiptModel(QAbstractListModel):
    def __init__(self,enabledReceipts=0):
        super(ReceiptModel,self).__init__()
        
        self.enabledReceipts = enabledReceipts
        self.insertNewReceipt = True
        self.d = data()

        stp = self.d.getSetup()
        self.keyboardButtonSize = int(stp['KeyboardButtonSize'])

    def data(self, index: QModelIndex, role: int):
        if (role == Qt.DisplayRole):
            self.getReceipts()
            receiptName = self.receipts[index.row()]['Name']
            return receiptName

    def rowCount(self, parent: QModelIndex) -> int:
        self.getReceipts()
        return len(self.receipts)

    def getReceipt(self,name):
        return self.d.getReceipt(name)

    def saveReceipt(self,receipt):
        #print(f'save = {receipt["Name"]}')
        self.d.saveReceipt(receipt)
        self.insertNewReceipt = False

    def deleteReceipt(self,name):
        self.d.deleteReceipt(name)

    def getReceipts(self):
        
        if (self.enabledReceipts):
            self.receipts = self.d.getEnabledReceipts()
        else:
            self.receipts = self.d.getReceipts()


