from SetupModel import SetupModel

from PyQt5.QtWidgets import QDialog, QGroupBox, QVBoxLayout,QWidget,QGridLayout,QProgressBar,QPushButton,QHBoxLayout
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,pyqtSlot

import Config

class SetupView(QDialog):
    def __init__(self,model):
        super().__init__()
        self.showFullScreen()
        self._model = model

        self.setWindowTitle(Config.SETUP_DIALOG_NAME)
        self.mainLayout = QVBoxLayout()
        # Общие настройки >>
        self.groupCommon = QGroupBox(Config.SETUP_DIALOG_COMMON)

        # Общие настройки <<

        # Рецепты >>
        self.groupReceipts = QGroupBox(Config.SETUP_DIALOG_RECEIPTS)
        # Рецепты <<

        # Кнопки нижнего ряда >>
        self.buttonsLayout = QHBoxLayout()
        self.closeButton = QPushButton(Config.SETUP_DIALOG_CLOSE)
        # Кнопки нижнего ряда <<


        self.buttonsLayout.addWidget(self.closeButton,1,Qt.AlignRight)

        self.mainLayout.addWidget(self.groupCommon)
        self.mainLayout.addWidget(self.groupReceipts)
        self.mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(self.mainLayout)


        self.closeButton.clicked.connect(lambda: self._model.onCloseButtonPressed())
        self._model.closeButtonPressed.connect(self.onCloseButtonPressed)

    @pyqtSlot()
    def onCloseButtonPressed(self):
        self.close()

