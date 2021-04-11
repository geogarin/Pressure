import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QObject,pyqtSignal,pyqtSlot,QTimer
from PyQt5.QtWidgets import QApplication,QMainWindow,QGroupBox,QPushButton,QLineEdit,QVBoxLayout,QGridLayout,QDialog,QLabel

class Model(QObject):
    amountChanged = pyqtSignal(int)
    butNameChanged = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self._amount = 0
        self.enb = False
        self._butName = 'Start'
        self.timer = QTimer()
        self.timer.timeout.connect(self.upd)
        #self.timer.start(300)

    @property
    def butName(self):
        return self._butName

    @butName.setter
    def butName(self,value):
        self._butName = value
        self.butNameChanged.emit(value)

    def buttonPressed(self):
        self.enb = not self.enb
        if self.enb:
            self.timer.start(300)
            self.butName = 'Stop'

        else:
            self.timer.stop()
            self.butName = 'Start'

    def upd(self):
        #print(f'upd {self.amount}')
        self.amount += 1
    
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self,value):
        self._amount = value
        self.amountChanged.emit(value)


class MainView(QMainWindow): # QDialog
    def __init__(self,model):
        super(MainView,self).__init__()
        self._model = model
        

         
        #self.group = QGroupBox('Qwerty')
        #self.group.setCheckable(False)
        centralWidget = QtWidgets.QWidget(self)
        
        self.resize(560,300)

        #self.lineEdit = QLineEdit('')
        lay = QVBoxLayout(centralWidget)



        self.lineEdit = QLineEdit('',centralWidget)
        self.button = QPushButton(self._model.butName,centralWidget)
        lay.addWidget(self.lineEdit)
        lay.addWidget(self.button)

        

        #label = QLabel("This is a PyQt5 window!")
        #self.setCentralWidget(label)
        self.setCentralWidget(centralWidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0,0,560,100))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionQuit = QtWidgets.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.menuFile.setTitle("File")
        self.menuHelp.setTitle("Help")
        self.actionQuit.setText("Quit")
        self.actionAbout.setText("About")  

        toolbar = QtWidgets.QToolBar("My main toolbar")
        toolbar.setIconSize(QtCore.QSize(32,32))
        self.addToolBar(toolbar) 
        button_action = QtWidgets.QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator() 
        button_action2 = QtWidgets.QAction("Your button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QtWidgets.QCheckBox())




        self._model.amountChanged.connect(self.onAmountChanged)
        self._model.butNameChanged.connect(self.onButtonNameChanged)
        self.button.clicked.connect(lambda: self._model.buttonPressed())


    def onMyToolBarButtonClick(self):
        print('click')

    @pyqtSlot(int)
    def onAmountChanged(self,value):
        self.lineEdit.setText(str(value))

    @pyqtSlot(str)
    def onButtonNameChanged(self,value):
        self.button.setText(value)
        


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        #self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
