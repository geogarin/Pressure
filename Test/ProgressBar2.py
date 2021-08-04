from CircularProgressBar import QRoundProgressBar
import sys
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QVBoxLayout
from time import sleep


class TstWidget(QWidget):
    def __init__(self):
        super(type(self), self).__init__()

        self.bar = QRoundProgressBar()
        self.bar.setFixedSize(500, 500)

        self.bar.setDataPenWidth(0)
        self.bar.setOutlinePenWidth(0)
        self.bar.setDecimals(2)
        #self.bar.setFormat('%v | %p %')
        self.bar.setFormat('%v')

        # self.bar.resetFormat()
        self.bar.setNullPosition(90)
        self.bar.setBarStyle(QRoundProgressBar.StyleDonut)
        self.bar.setDataColors([(0., QtGui.QColor.fromRgb(255,0,0)), (0.5, QtGui.QColor.fromRgb(255,255,0)), (1., QtGui.QColor.fromRgb(0,255,0))])
        self.bar.setMaximun(5)
        self.bar.setMinimun(0)
        self.bar.setRange(0, 5)
        self.bar.setValue(0)
        #self.bar.setDonutThicknessRatio(.25)
        #self.bar.setDataPenWidth=0
        #self.bar.setOutlinePenWidth=0.01

        button =  QPushButton("Start", self)

        button.clicked.connect(self.on_start)

        lay =  QVBoxLayout()
        lay.addWidget(button)
        lay.addWidget(self.bar)
        self.setLayout(lay)

        self.myLongTask = TaskThread()
        self.myLongTask.notifyProgress.connect(self.on_progress)

    def on_start(self):
        self.myLongTask.start()

    def on_progress(self, i):
        self.bar.setValue(i)


class TaskThread(QtCore.QThread):
   notifyProgress = QtCore.pyqtSignal(float)

   def run(self):
       for i in range(101):
           j = 5/100*i
           self.notifyProgress.emit(j)
           sleep(0.1)


def main():

    app = QApplication(sys.argv)
    ex = TstWidget()
    ex.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()