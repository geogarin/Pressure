from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QObject,pyqtSignal, pyqtSlot,QAbstractTableModel,QModelIndex
from Database.database import data
from datetime import datetime

class TestResultModel(QAbstractTableModel):
    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self,parent)

        d = data()
        self.tableData = d.getTestResults()
        """
        self.columnNames=("Date",
            "Channel",
            TestName,
            ProductVolume,
            StrengthTestEnabled,
            StrengthTestPassed,
            StrengthTestResult,
            StrengthTestDuration,
            StrengthTestPlanPressure,
            StrengthTestFactPressure,
            SealedTestEnabled,
            SealedTestPassed,
            SealedTestResult,
            SealedTestDuration,
            SealedTestPlanPressure,
            SealedTestFactPressure,
            SealedTestMaxDeltaThreshold,
            SealedTestFactDeltaThreshold,
            SealedTestMaxAllowedLeak,
            SealedTestVolumeOfLeak,
            SealedTestCrossSecAreaLeak,
            SealedTestLeakDiameter)
        """
    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.tableData)

    def columnCount(self, parent: QModelIndex) -> int:
        return len(self.tableData[0])-1

    def data(self, index: QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            res = self.tableData[row][column+1]
            if column==0:
                res = datetime.strptime(res,'%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%y %H:%M:%S')
            return res
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role!=QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation==QtCore.Qt.Horizontal:
            return QtCore.QVariant('My Column Name') 
        

if __name__=="__main__":
    d=data()
    r=d.getTestResults()

    print(f'fields={len(r[0])}')
    print(f'{r[7][1]}')
    ddd = r[7][1]

    dt = datetime.strptime(ddd,'%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%y %H:%M:%S')

    print(f'{dt}')


