

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect
import sys



class RoundedRect(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        print('init')
        self._w = 50/2
        self._h = 200/2
        self._r = 10
        self.value=0
        
        self.setMinimumWidth(int(2*self._w))
        self.setMinimumHeight(int(2*self._h))


    def setValue(self, val):
        print('set value')
        if self.value != val:    
            self.value = val
            self.update()

    

    def paintEvent(self, event):
        print('paint')
        if (self.value==0):
            bg_color = Qt.gray
        if (self.value==1):
            bg_color = Qt.green
        if (self.value==-1):
            bg_color = Qt.red
        
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QBrush(bg_color))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(0)
        
        painter.setPen(pen)
        
        painter.drawRoundedRect(QRect(-self._w, -self._h, 2*self._w, 2*self._h), self._r, self._r)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 350)
        MainWindow.setMinimumSize(QtCore.QSize(550, 350))
        MainWindow.setMaximumSize(QtCore.QSize(550, 350))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.sw = RoundedRect(self.centralwidget)
        #self.sw.setChecked(True)
        #self.sw.move(300,100)
        #self.sw.setValue(1)
        
        #self.sw.setValue(-1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    MainWindow = QtWidgets.QMainWindow()
    ui        = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec()