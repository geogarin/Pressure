from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget,QDialog,QPushButton,QVBoxLayout,QSpacerItem,QGridLayout,QFrame
from TestResultModel import TestResultModel
import Config
import stylesheets

class TestResultView(QDialog):
    def __init__(self, *args,**kwargs):
        #QWidget.__init__(self,*args,**kwargs)
        super().__init__()
        self.showFullScreen()
        self.view = QtWidgets.QTableView()
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.verticalHeader().setVisible(False)


        #self.mainLayout = QVBoxLayout()
        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)
        self.mainLayout = QGridLayout(self.frame) 
        
        self.mainLayout.addWidget(self.view,0,1)
        self.model = TestResultModel()
        self.view.setModel(self.model)

        
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.horizontalHeader().setSectionsMovable(True)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


        self.closeButton = QPushButton(Config.SETUP_DIALOG_CLOSE)
        self.closeButton.setStyleSheet(stylesheets.SVC_Button)

        self.spacer = QSpacerItem(10,200)
        self.mainLayout.addItem(self.spacer,1,1)
        self.mainLayout.addWidget(self.closeButton,2,1)

        self.setLayout(self.mainLayout)
        self.closeButton.clicked.connect(self.onCloseButtonPressed)

    def onCloseButtonPressed(self,setupSaved):
        self.close()
