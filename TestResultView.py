import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget,QDialog,QPushButton,QVBoxLayout,QSpacerItem,QGridLayout,QFrame,QApplication,QLabel,QScrollBar
from TestResultModel import TestResultModel
from TestResultExport import TestResultExporter
import Config
import stylesheets
from VirtualKeyboard import VirtualKeyboard
from QLineEditVK import QLineEditVK
from datetime import datetime

class TestResultView(QDialog):
    
    def __init__(self, *args,**kwargs):
        #QWidget.__init__(self,*args,**kwargs)
        super().__init__()
        self.showFullScreen()
     
        self.view = QtWidgets.QTableView()
        
        
        self.model = TestResultModel()
        self.view.setModel(self.model)
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().sectionResizeMode(QHeaderView.Fixed)
        self.view.verticalHeader().setDefaultSectionSize(self.model.fontSize+20)
        self.view.resizeColumnsToContents()

        
        self.view.verticalScrollBar().setStyleSheet(stylesheets.TR_Vertical)
        self.view.horizontalScrollBar().setStyleSheet(stylesheets.TR_Horizontal)
        
        self.frame = QFrame()
        self.frame.setStyleSheet(stylesheets.BodyStyle)
        self.mainLayout = QGridLayout(self.frame) 
        
        

        self.labelExportResultQty = QLabel(Config.RES_EXPORT_RESULT)
        self.labelExportResultQty.setStyleSheet(stylesheets.SDS_Label)

        self.exportResultQty = QLineEditVK()
        self.exportResultQty.keyboard = VirtualKeyboard(self,int(self.model.setup['KeyboardButtonSize']),True) 
        self.exportResultQty.setStyleSheet(stylesheets.SDS_LineEdit)
        self.exportResultQty.name = 'ExportResultQty'
        self.exportResultQty.setText(self.model.exportResultQty)
        self.exportResultQty.setFixedWidth(Config.SETUP_DIALOG_LINE_EDIT_FIELD_WIDTH)
        
        self.exportButton = QPushButton(Config.RES_EXPORT_BUTTON)
        self.exportButton.setStyleSheet(stylesheets.SVC_Button)

        
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.horizontalHeader().setSectionsMovable(True)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.view.horizontalHeader().setFont(self.font)
        self.view.setFont(self.model.font)


        self.closeButton = QPushButton(Config.SETUP_DIALOG_CLOSE)
        self.closeButton.setStyleSheet(stylesheets.SVC_Button)

        self.spacer = QSpacerItem(10,50)
        self.spacer2 = QSpacerItem(10,100)
        self.mainLayout.addWidget(self.view,0,1,1,3)

        self.mainLayout.addItem(self.spacer,1,1,1,3)
        self.mainLayout.addWidget(self.labelExportResultQty,2,1)
        self.mainLayout.addWidget(self.exportResultQty,2,2)
        self.mainLayout.addWidget(self.exportButton,2,3)

        self.mainLayout.addItem(self.spacer2,3,1,1,3)
        self.mainLayout.addWidget(self.closeButton,4,3,1,1)

        self.setLayout(self.mainLayout)
        self.closeButton.clicked.connect(self.onCloseButtonPressed)
        self.exportButton.clicked.connect(self.onExportButtonPressed)
        self.exportResultQty.editDone.connect(self.exportResultQtyEdited)

        

    def exportResultQtyEdited(self):
        val = int(self.exportResultQty.text())
        if (val<0): val=0      
        self.exportResultQty.setText(str(val))
        self.model.exportResultQty = val

    def onCloseButtonPressed(self):
        self.close()

    def reportProgress(self, n):
        self.exportResultQty.setText(str(n))

    def onExportButtonPressed(self):
        #print(f"export")
        self.thread = QThread()
        self.xlsExporter = TestResultExporter(int(self.model.exportResultQty))
        self.xlsExporter.moveToThread(self.thread)

        self.thread.started.connect(self.xlsExporter.run)
        self.xlsExporter.finished.connect(self.thread.quit)
        self.xlsExporter.finished.connect(self.xlsExporter.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.xlsExporter.progress.connect(self.reportProgress)

        
        self.thread.start()

        self.exportButton.setEnabled(False)
        self.closeButton.setEnabled(False)
        self.thread.finished.connect(lambda: (self.exportButton.setEnabled(True), self.closeButton.setEnabled(True)))



        


if __name__=='__main__':
    app = QApplication(sys.argv)
    
    p = TestResultView()
    p.show()
    sys.exit(app.exec_())
