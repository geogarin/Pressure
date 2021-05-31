import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QCheckBox, QFormLayout, QFrame,QComboBox, QListView,QWidget,QGroupBox,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QGridLayout,QApplication,QMessageBox)
from PyQt5.QtCore import QModelIndex, Qt,QPoint, QRect, QSize, pyqtSignal, pyqtSlot
import Config
from ReceiptModel import ReceiptModel
from QLineEditVK import QLineEditVK
from VirtualKeyboard import VirtualKeyboard

import stylesheets

class ReceiptView(QWidget):
    listSelectionChanged = pyqtSignal(QModelIndex)
    hideKeyboard = pyqtSignal()
    def __init__(self,parent = None,receiptModel=None):

        super(QWidget,self).__init__(parent)
         
        self.receiptList = QListView()
        self.receiptList.setMaximumWidth(Config.RC_LIST_WIDTH)
        self.receiptList.setStyleSheet(stylesheets.SDS_ListView)
        self.receiptList.setModel(receiptModel)
        self.receiptListSelectionModel = self.receiptList.selectionModel()        

        self.receiptName = QLineEditVK()
        self.receiptName.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,False)
        self.receiptName.setStyleSheet(stylesheets.SDS_LineEdit)
        self.receiptNameLabel = QLabel(Config.RC_NAME) 
        self.receiptNameLabel.setStyleSheet(stylesheets.SDS_Label)

        self.connection = QLineEditVK()
        self.connection.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.connection.setStyleSheet(stylesheets.SDS_LineEdit)
        self.connectionLabel = QLabel(Config.RC_CONNECTION_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE)
        self.connectionLabel.setStyleSheet(stylesheets.SDS_Label)

        self.inflating = QLineEditVK()
        self.inflating.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.inflating.setStyleSheet(stylesheets.SDS_LineEdit)
        self.inflatingLabel = QLabel(Config.RC_INFLATING_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE)
        self.inflatingLabel.setStyleSheet(stylesheets.SDS_Label)

        self.stabilization = QLineEditVK()
        self.stabilization.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.stabilization.setStyleSheet(stylesheets.SDS_LineEdit)
        self.stabilizationLabel = QLabel(Config.RC_STABILIZATION_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE)
        self.stabilizationLabel.setStyleSheet(stylesheets.SDS_Label)

        self.strengthPressure = QLineEditVK()
        self.strengthPressure.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.strengthPressure.setStyleSheet(stylesheets.SDS_LineEdit)
        self.strengthPressureLabel = QLabel(Config.RC_STRENGTH_TEST_PRESSURE+', '+Config.RC_STRENGTH_TEST_PRESSURE_UNIT_OF_MEASURE)
        self.strengthPressureLabel.setStyleSheet(stylesheets.SDS_Label)

        self.strengthDuration = QLineEditVK()
        self.strengthDuration.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.strengthDuration.setStyleSheet(stylesheets.SDS_LineEdit)
        self.strengthDurationLabel = QLabel(Config.RC_STRENGTH_TEST_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE)
        self.strengthDurationLabel.setStyleSheet(stylesheets.SDS_Label)

        self.sealedPressure = QLineEditVK()
        self.sealedPressure.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.sealedPressure.setStyleSheet(stylesheets.SDS_LineEdit)
        self.sealedPressureLabel = QLabel(Config.RC_SEALED_TEST_PRESSURE+', '+Config.RC_SEALED_TEST_PRESSURE_UNIT_OF_MEASURE)
        self.sealedPressureLabel.setStyleSheet(stylesheets.SDS_Label)

        self.sealedDuration = QLineEditVK()
        self.sealedDuration.keyboard = VirtualKeyboard(self,self.receiptList.model().keyboardButtonSize,True)
        self.sealedDuration.setStyleSheet(stylesheets.SDS_LineEdit)
        self.sealedDurationLabel = QLabel(Config.RC_SEALED_TEST_DURATION+', '+Config.RC_DURATION_UNIT_OF_MEASURE)
        self.sealedDurationLabel.setStyleSheet(stylesheets.SDS_Label)

        self.receiptEnabled = QCheckBox()
        self.receiptEnabled.setStyleSheet(stylesheets.SDS_CheckBox)
        self.receiptEnabledLabel = QLabel(Config.RC_ENABLED)
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
        


        self.receiptEditForm = QFormLayout()
        self.receiptEditForm.addRow(self.receiptNameLabel,self.receiptName)
        self.receiptEditForm.addRow(self.connectionLabel,self.connection)
        self.receiptEditForm.addRow(self.inflatingLabel,self.inflating)
        self.receiptEditForm.addRow(self.stabilizationLabel,self.stabilization)
        self.receiptEditForm.addRow(self.strengthPressureLabel,self.strengthPressure)
        self.receiptEditForm.addRow(self.strengthDurationLabel,self.strengthDuration)
        self.receiptEditForm.addRow(self.sealedPressureLabel,self.sealedPressure)
        self.receiptEditForm.addRow(self.sealedDurationLabel,self.sealedDuration)
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
        
        self.show()

    def onButtonNewClicked(self):
        self.hideKeyboard.emit()
        self.receiptList.model().insertNewReceipt = True
        self.receiptName.setText('')
        self.receiptEnabled.setChecked(False)

    def onButtonSaveClicked(self):
        self.hideKeyboard.emit()
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

                
                if self.connection.text()!='':
                    receipt['ConnectionDuration'] = float(self.connection.text())
                else:
                    receipt['ConnectionDuration'] = 0

                if self.inflating.text()!='':
                    receipt['InflatingDuration'] = float(self.inflating.text())
                else: 
                    receipt['InflatingDuration'] = 0

                if self.stabilization.text()!='':
                    receipt['StabilizationDuration'] = float(self.stabilization.text())
                else:
                    receipt['StabilizationDuration'] = 0

                if self.strengthPressure.text()!='':
                    receipt['StrengthTestPressure'] = int(self.strengthPressure.text())
                else:
                    receipt['StrengthTestPressure'] = 0

                if  self.strengthDuration.text()!='':   
                    receipt['StrengthTestDuration'] = float(self.strengthDuration.text())
                else:
                    receipt['StrengthTestDuration'] = 0

                if self.sealedPressure.text()!='':
                    receipt['SealedTestPressure'] = int(self.sealedPressure.text())
                else:
                    receipt['SealedTestPressure'] = 0

                if self.sealedDuration.text()!='':
                    receipt['SealedTestDuration'] = float(self.sealedDuration.text())
                else:
                    receipt['SealedTestDuration'] = 0

                receipt['Enabled'] = 1 if self.receiptEnabled.isChecked() else 0

                self.receiptList.model().saveReceipt(receipt)
                self.receiptList.model().layoutChanged.emit()

    def onButtonDeleteClicked(self):
        self.hideKeyboard.emit()
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
            if not (rcpt['ConnectionDuration'] is None):
                self.connection.setText(str(rcpt['ConnectionDuration']))

            if not( rcpt['InflatingDuration']is None):    
                self.inflating.setText(str(rcpt['InflatingDuration']))

            if not(rcpt['StabilizationDuration'] is None):
                self.stabilization.setText(str(rcpt['StabilizationDuration']))

            if not(rcpt['StrengthTestPressure'] is None):
                self.strengthPressure.setText(str(rcpt['StrengthTestPressure']))

            if not(rcpt['StrengthTestDuration'] is None):
                self.strengthDuration.setText(str(rcpt['StrengthTestDuration']))

            if not(rcpt['SealedTestPressure'] is None):
                self.sealedPressure.setText(str(rcpt['SealedTestPressure']))

            if not(rcpt['SealedTestDuration'] is None):
                self.sealedDuration.setText(str(rcpt['SealedTestDuration']))
            self.receiptEnabled.setChecked(rcpt['Enabled']==1)
            


if __name__ == '__main__':

    app = QApplication(sys.argv)
    rm = ReceiptModel(enabledReceipts=0)
    rv = ReceiptView(receiptModel=rm)
    #rv.receiptList.setModel(rm)
    
    rv.setGeometry(100, 100, 700, 700)
    

    sys.exit(app.exec_())

    
