import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QCheckBox, QFormLayout, QFrame,QComboBox, QListView,QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout,QApplication,QMessageBox)
from PyQt5.QtCore import QModelIndex, QObject, Qt,QPoint, QRect, QSize, pyqtSignal, pyqtSlot,QSignalMapper
import Config
from ReceiptModel import ReceiptModel
from QLineEditVK import QLineEditVK
from VirtualKeyboard import VirtualKeyboard

import stylesheets

class ReceiptView(QWidget):
    listSelectionChanged = pyqtSignal(QModelIndex)
    def __init__(self,parent = None,receiptModel=None):

        super(QWidget,self).__init__(parent)

        self.fieldsQty = 9

        self.fieldNames = ['Name','ConnectionDuration','InflatingDuration','StabilizationDuration','StrengthTestPressure','StrengthTestDuration','SealedTestPressure',
                          'SealedTestDeltaThreshold','SealedTestDuration','Enabled']
        self.labelTexts = [
            Config.RC_NAME,
            Config.RC_CONNECTION_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE+' ('+ str(Config.RC_CONNECTION_DURATION_MIN) +'-'+ str(Config.RC_CONNECTION_DURATION_MAX) +')',
            Config.RC_INFLATING_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE+' ('+ str(Config.RC_INFLATING_DURATION_MIN) +'-'+ str(Config.RC_INFLATING_DURATION_MAX) +')',
            Config.RC_STABILIZATION_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE+' ('+ str(Config.RC_STABILIZATION_DURATION_MIN) +'-'+ str(Config.RC_STABILIZATION_DURATION_MAX) +')',
            Config.RC_STRENGTH_TEST_PRESSURE+', '+Config.RC_STRENGTH_TEST_PRESSURE_UNIT_OF_MEASURE+' ('+ str(Config.RC_STRENGTH_TEST_PRESSURE_MIN) +'-'+ str(Config.RC_STRENGTH_TEST_PRESSURE_MAX) +')',
            Config.RC_STRENGTH_TEST_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE+' ('+ str(Config.RC_STRENGTH_TEST_DURATION_MIN) +'-'+ str(Config.RC_STRENGTH_TEST_DURATION_MAX) +')',
            Config.RC_SEALED_TEST_PRESSURE+', '+Config.RC_SEALED_TEST_PRESSURE_UNIT_OF_MEASURE+' ('+ str(Config.RC_SEALED_TEST_PRESSURE_MIN) +'-'+ str(Config.RC_SEALED_TEST_PRESSURE_MAX) +')',
            Config.RC_SEALED_TEST_DELTA_THRESHOLD+', '+Config.RC_SEALED_TEST_PRESSURE_UNIT_OF_MEASURE+' ('+ str(Config.RC_SEALED_TEST_DELTA_THRESHOLD_MIN) +'-'+ str(Config.RC_SEALED_TEST_DELTA_THRESHOLD_MAX) +')',
            Config.RC_SEALED_TEST_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE+' ('+ str(Config.RC_SEALED_TEST_DURATION_MIN) +'-'+ str(Config.RC_SEALED_TEST_DURATION_MAX) +')',
            Config.RC_ENABLED]

        self.fieldRanges = [
            (),
            (Config.RC_CONNECTION_DURATION_MIN,Config.RC_CONNECTION_DURATION_MAX),
            (Config.RC_INFLATING_DURATION_MIN,Config.RC_INFLATING_DURATION_MAX),
            (Config.RC_STABILIZATION_DURATION_MIN,Config.RC_STABILIZATION_DURATION_MAX),
            (Config.RC_STRENGTH_TEST_PRESSURE_MIN,Config.RC_STRENGTH_TEST_PRESSURE_MAX),
            (Config.RC_STRENGTH_TEST_DURATION_MIN,Config.RC_STRENGTH_TEST_DURATION_MAX),
            (Config.RC_SEALED_TEST_PRESSURE_MIN,Config.RC_SEALED_TEST_PRESSURE_MAX),
            (Config.RC_SEALED_TEST_DELTA_THRESHOLD_MIN,Config.RC_SEALED_TEST_DELTA_THRESHOLD_MAX),
            (Config.RC_SEALED_TEST_DURATION_MIN,Config.RC_SEALED_TEST_DURATION_MAX),
            ()
        ]
                 
        self.receiptList = QListView()
        self.receiptList.setMaximumWidth(Config.RC_LIST_WIDTH)
        self.receiptList.setStyleSheet(stylesheets.SDS_ListView)
        self.receiptList.setModel(receiptModel)
        self.receiptListSelectionModel = self.receiptList.selectionModel() 
        

        self.signalMapper = QSignalMapper(self) 
        self.signalMapper.mapped[int].connect(self.validateFieldValue)      

        self.receiptName = QLineEditVK()
        self.receiptName.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,False)
        self.receiptName.setStyleSheet(stylesheets.SDS_LineEdit)
        self.receiptName.editDone.connect(self.signalMapper.map)
        self.signalMapper.setMapping(self.receiptName,self.fieldNames[0])    
        self.receiptNameLabel = QLabel(self.labelTexts[0]) 
        self.receiptNameLabel.setStyleSheet(stylesheets.SDS_Label)


        self.receiptEditForm = QFormLayout()
        self.receiptEditForm.addRow(self.receiptNameLabel,self.receiptName)
        self.field = [None]*self.fieldsQty
        self.label = [None]*self.fieldsQty
        #self.vk = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        for i in range(1,self.fieldsQty):
            self.field[i] = QLineEditVK()
            self.field[i].keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
            #self.field[i].keyboard = self.vk
            self.field[i].range = self.fieldRanges[i]
            self.field[i].setStyleSheet(stylesheets.SDS_LineEdit)
            self.field[i].editDone.connect(self.signalMapper.map)
            self.signalMapper.setMapping(self.field[i],i)
            
            self.label[i] = QLabel(self.labelTexts[i])
            self.label[i].setStyleSheet(stylesheets.SDS_Label)
            self.receiptEditForm.addRow(self.label[i],self.field[i])

        self.receiptEnabled = QCheckBox()
        self.receiptEnabled.setStyleSheet(stylesheets.SDS_CheckBox)
        self.receiptEnabledLabel = QLabel(self.labelTexts[9])
        self.receiptEnabledLabel.setStyleSheet(stylesheets.SDS_Label)

        self.buttonNew = QPushButton(Config.RC_NEW)
        self.buttonNew.setStyleSheet(stylesheets.SDS_Button)
        self.buttonSave = QPushButton(Config.RC_SAVE)
        self.buttonSave.setStyleSheet(stylesheets.SDS_Button)
        self.buttonDelete = QPushButton(Config.RC_DELETE)
        self.buttonDelete.setStyleSheet(stylesheets.SDS_Button)
        hBox = QHBoxLayout()
        hBox.addWidget(self.buttonNew)
        hBox.addStretch()
        hBox.addWidget(self.buttonSave)
        hBox.addStretch()
        hBox.addWidget(self.buttonDelete)
        
        self.receiptEditForm.addRow(self.receiptEnabledLabel,self.receiptEnabled)
        self.receiptEditForm.addRow(hBox)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.receiptList,0,0)
        self.mainLayout.addItem(self.receiptEditForm,0,1)

        self.setLayout(self.mainLayout)

        self.receiptListSelectionModel.selectionChanged.connect(self.onReceiptSelected)
        self.buttonNew.clicked.connect(self.onButtonNewClicked)
        self.buttonSave.clicked.connect(self.onButtonSaveClicked)
        self.buttonDelete.clicked.connect(self.onButtonDeleteClicked)
        
        self.receiptList.setCurrentIndex(receiptModel.index(0,0) )
        self.onReceiptSelected(receiptModel.index(0,0))

        self.show()

    def onButtonNewClicked(self):       
        self.receiptList.model().insertNewReceipt = True
        self.receiptName.setText('')
        for i in range(1,self.fieldsQty):
            self.field[i].setText('')
            self.validateFieldValue(i)
        self.receiptEnabled.setChecked(False)

    def onButtonSaveClicked(self):
        recName = self.receiptName.text()
        if recName!='':
            retVal = QMessageBox.Yes
            rcpt = None
            if (self.receiptList.model().insertNewReceipt):
                rcpt = self.receiptList.model().getReceipt(recName)
            
            if not(rcpt is None):
                msgBox = QMessageBox(self)
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(Config.RC_DIALOG_RECEIPT_EXISTS)
                msgBox.setWindowTitle(Config.RC_DIALOG_NAME)
                msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                retVat = msgBox.exec()
            
            if retVal == QMessageBox.Yes:
                receipt = {}
                receipt['Name'] = recName

                for i in range(1,self.fieldsQty):
                    self.validateFieldValue(i)
                    if self.field[i].text()!='':
                        receipt[self.fieldNames[i]] = int(self.field[i].text())
                    else:
                        receipt[self.fieldNames[i]] = 0 

                receipt['Enabled'] = 1 if self.receiptEnabled.isChecked() else 0

                self.receiptList.model().saveReceipt(receipt)
                self.receiptList.model().layoutChanged.emit()
        
    def validateFieldValue(self,idx):
        if (idx in range(1,self.fieldsQty)):
            if self.field[idx].text()!='':
                val = int(self.field[idx].text())
                if val<self.field[idx].range[0]:
                    val = self.field[idx].range[0]
                if val>self.field[idx].range[1]:
                    val = self.field[idx].range[1]
            else:
                val = self.field[idx].range[0]
            self.field[idx].setText(str(val))

    def onButtonDeleteClicked(self):
        self.receiptList.model().deleteReceipt(self.receiptName.text())
        self.receiptList.model().layoutChanged.emit()
        self.receiptList.clearSelection()
        self.onButtonNewClicked()

    def onReceiptSelected(self,index):
        idx = self.receiptListSelectionModel.selection().indexes()        
        if idx:
            item = idx[0]
            self.receiptList.model().insertNewReceipt = False
            #print(f'selected = {item.data()}  row={item.row()}')
            rcpt = self.receiptList.model().getReceipt(item.data())
            self.receiptName.setText(rcpt['Name'])
            for i in range(1,self.fieldsQty):
                if not (rcpt[self.fieldNames[i]] is None):
                    self.field[i].setText(str(rcpt[self.fieldNames[i]]))    
            self.receiptEnabled.setChecked(rcpt['Enabled']==1)
            


if __name__ == '__main__':

    
    app = QApplication(sys.argv)
    rm = ReceiptModel(enabledReceipts=0)
    rv = ReceiptView(receiptModel=rm)
    #rv.receiptList.setModel(rm)
    
    rv.setGeometry(100, 100, 700, 700)
    

    sys.exit(app.exec_())

    
