import subprocess
from SetupModel import SetupModel

from PyQt5.QtWidgets import QDialog, QDialogButtonBox,QLineEdit, QGroupBox, QVBoxLayout,QWidget,QGridLayout,QProgressBar,QPushButton,QHBoxLayout,QMessageBox,QSpinBox
from PyQt5 import QtGui
from PyQt5.QtCore import QElapsedTimer, Qt,pyqtSlot

from VirtualKeyboard import VirtualKeyboard

import Config
import stylesheets

class MatchBoxLineEdit(QLineEdit):
    def __init__(self,parent):
        super().__init__()
        self.mainWindowObj = parent
        #self.setFocusPolicy(Qt.ClickFocus)

    def focusInEvent(self, e):
        print(f'focus in {e.reason()}')
        if (e.reason()==Qt.MouseFocusReason):
            self.mainWindowObj.virtualKeyboardWidget.currentTextBox = self
            self.mainWindowObj.virtualKeyboardWidget.show()
        super(MatchBoxLineEdit, self).focusInEvent(e)


class SetupView(QDialog):
    def __init__(self,model):
        super().__init__()
        self.showFullScreen()
        self.virtualKeyboardWidget = VirtualKeyboard(self)
        self._model = model

        self.setWindowTitle(Config.SETUP_DIALOG_NAME)
        self.mainLayout = QVBoxLayout()
        # Общие настройки >>
        self.groupCommon = QGroupBox(Config.SETUP_DIALOG_COMMON)
        self.groupCommon.setStyleSheet(stylesheets.SDS_GroupBox)

        self.spinBoxHBox = QHBoxLayout()
        le = QLineEdit('ssss')
        self.spinBox = MatchBoxLineEdit(self) #QSpinBox()
        #self.spinBox.setValue(50)
        #self.spinBox.setText('50')
        #self.spinBox.setStyleSheet(stylesheets.SDS_SpinBox)
        self.spinBoxHBox.addWidget(le)
        self.spinBoxHBox.addWidget(self.spinBox)
        #QDialogButtonBox.C

        curRow = 0
        self.gridLayCommon = QGridLayout()
        self.gridLayCommon.addLayout(self.spinBoxHBox,curRow,0)
        


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

    @pyqtSlot(bool)
    def onCloseButtonPressed(self,setupSaved):
        if (not setupSaved):
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(Config.SETUP_DIALOG_SAVE_CHANGED)
            msgBox.setWindowTitle(Config.SETUP_DIALOG_NAME)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Yes:
                self._model.onSaveButtonPressed()         
        self.close()

