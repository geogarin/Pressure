
from SetupModel import SetupModel

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel,QLineEdit, QGroupBox, QVBoxLayout,QGridLayout,QPushButton,QHBoxLayout,QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,pyqtSlot

from VirtualKeyboard import VirtualKeyboard
from QLineEditVK import QLineEditVK

import Config
import stylesheets

class SetupView(QDialog):
    def __init__(self,model):
        super().__init__()
        self._model = model
        

        self.virtualKeyboardWidget = VirtualKeyboard(self,int(self._model.setup['KeyboardButtonSize']),True)
        
        self.showFullScreen()
        self.setWindowTitle(Config.SETUP_DIALOG_NAME)
        self.mainLayout = QVBoxLayout()
        # Общие настройки >>
        self.groupCommon = QGroupBox(Config.SETUP_DIALOG_COMMON)
        self.groupCommon.setStyleSheet(stylesheets.SDS_GroupBox)

        self.formL = QFormLayout()
        self.labelFilterDepth = QLabel(Config.SD_FILTER_DEPTH)
        self.labelFilterDepth.setStyleSheet(stylesheets.SDS_Label)

        self.filterDepthValue = QLineEditVK()
        self.filterDepthValue.keyboard = VirtualKeyboard(self,1.5*int(self._model.setup['KeyboardButtonSize']),True) 
        self.filterDepthValue.setStyleSheet(stylesheets.SDS_LineEdit)
        self.filterDepthValue.name = 'FilterDepth'
        self.filterDepthValue.setText(self._model.setup[self.filterDepthValue.name])
        self.filterDepthValue.setFixedWidth(Config.SETUP_DIALOG_LINE_EDIT_FIELD_WIDTH)

        self.formL.addRow(self.labelFilterDepth,self.filterDepthValue)

        self.formR = QFormLayout()
        self.labelKbButtonSize = QLabel(Config.SD_KEYBOARD_BUTTON_SIZE)
        self.labelKbButtonSize.setStyleSheet(stylesheets.SDS_Label)

        self.kbButtonSizeValue = QLineEditVK()
        self.kbButtonSizeValue.keyboard = VirtualKeyboard(self,int(self._model.setup['KeyboardButtonSize']),True)
        self.kbButtonSizeValue.name = 'KeyboardButtonSize' 
        self.kbButtonSizeValue.setText(self._model.setup[self.kbButtonSizeValue.name])
        self.kbButtonSizeValue.setStyleSheet(stylesheets.SDS_LineEdit)
        self.kbButtonSizeValue.setFixedWidth(Config.SETUP_DIALOG_LINE_EDIT_FIELD_WIDTH)

        self.formR.addRow(self.labelKbButtonSize,self.kbButtonSizeValue)
        
        curRow = 0
        self.gridLayCommon = QGridLayout()
        self.gridLayCommon.addLayout(self.formL,curRow,0)
        self.gridLayCommon.addLayout(self.formR,curRow,1)
        
        self.groupCommon.setLayout(self.gridLayCommon)

        """        
        SAMPLES_QUANTITY = 50
        ABS_PRESSURE_ROUNDING_PRECISION = 2
        DIF_PRESSURE_ROUNDING_PRECISION = 2
        """

        # Общие настройки <<

        # Рецепты >>
        self.groupReceipts = QGroupBox(Config.SETUP_DIALOG_RECEIPTS)
        self.groupReceipts.setStyleSheet(stylesheets.SDS_GroupBox)
        # Рецепты <<

        # Кнопки нижнего ряда >>
        self.buttonsLayout = QHBoxLayout()

        self.saveButton = QPushButton(Config.SETUP_DIALOG_SAVE)
        self.saveButton.setStyleSheet(stylesheets.SDS_Button)

        self.closeButton = QPushButton(Config.SETUP_DIALOG_CLOSE)
        self.closeButton.setStyleSheet(stylesheets.SDS_Button)

        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.saveButton,0,Qt.AlignRight)
        self.buttonsLayout.addWidget(self.closeButton,0,Qt.AlignRight)
        # Кнопки нижнего ряда <<


        

        self.mainLayout.addWidget(self.groupCommon)
        self.mainLayout.addWidget(self.groupReceipts)
        self.mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(self.mainLayout)

        self.saveButton.clicked.connect(lambda: self._model.onSaveButtonPressed())
        self.closeButton.clicked.connect(lambda: self._model.onCloseButtonPressed())
        self._model.closeButtonPressed.connect(self.onCloseButtonPressed)

    
        self.filterDepthValue.editDone.connect(self.filterDepthValueEdited)
        self.kbButtonSizeValue.editDone.connect(self.kbButtonSizeValueEdited)


    @pyqtSlot()
    def filterDepthValueEdited(self):
        val = int(self.filterDepthValue.text())
        if (val<0): val=0
        if (val>Config.MAX_SAMPLES_QUANTITY): val=Config.MAX_SAMPLES_QUANTITY
        self.filterDepthValue.setText(str(val))
        self._model.onSave(self.filterDepthValue.name,val)

    @pyqtSlot()
    def kbButtonSizeValueEdited(self):
        val = int(self.kbButtonSizeValue.text())
        if (val<Config.MIN_KB_BUTTON_SIZE): val=Config.MIN_KB_BUTTON_SIZE
        if (val>Config.MAX_KB_BUTTON_SIZE): val=Config.MAX_KB_BUTTON_SIZE
        self.kbButtonSizeValue.setText(str(val))
        self._model.onSave(self.kbButtonSizeValue.name,val)
        
    @pyqtSlot(bool)
    def onCloseButtonPressed(self,setupSaved):
        if (not setupSaved):
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(Config.SETUP_DIALOG_SAVE_CHANGED)
            msgBox.setWindowTitle(Config.SETUP_DIALOG_NAME)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            returnValue = msgBox.exec()
            #if returnValue == QMessageBox.Yes:
            #    self._model.onSaveButtonPressed()         
        self.close()



