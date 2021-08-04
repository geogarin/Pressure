from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,QObject,pyqtSignal, pyqtSlot,QAbstractTableModel,QModelIndex
from Database.database import data
from datetime import datetime
from TestResultExport import TestResultExporter
import Config

class TestResultModel(QAbstractTableModel):
    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self,parent)

        d = data()
        self.tableData = d.getTestResults()
   
        stp = d.getSetup()
        self.setupKeys = stp.keys()
        self.setup = {k:str(stp[k]) for k in self.setupKeys if k!='Entry'}

        self.fontSize = 22
        self.font = QtGui.QFont(QtGui.QFont("Times",self.fontSize))

        self.exportResultQty = '1'
        self.resExporter = TestResultExporter(0)
        
    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.tableData)

    def columnCount(self, parent: QModelIndex) -> int:
        return len(self.tableData[0])-1

    def data(self, index: QModelIndex, role: int):
        
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole:            
            return self.formatTestResultData(self.tableData[row],column)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == QtCore.Qt.DisplayRole:
            if orientation==QtCore.Qt.Horizontal:           
                return Config.RES_COLUMN_NAMES[section]
        if role == QtCore.Qt.FontRole:
            return self.font
        
        if role!=QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        

if __name__=="__main__":
    d=data()
    r=d.getTestResults()

    print(f'fields={len(r[0])}')
    print(f'{r[7][1]}')
    ddd = r[7][1]

    dt = datetime.strptime(ddd,'%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%y %H:%M:%S')
    print(f'{dt}')

    dt=datetime.now()
    s=dt.strftime('%d_%m_%Y_%H_%M')
    print(s)


