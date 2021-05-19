from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect
import sys

class MySwitch(QtWidgets.QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        print('init')
        self.setCheckable(True)
        self.setMinimumWidth(200)
        self.setMinimumHeight(80)

    def paintEvent(self, event):
        label = "Выкл" if self.isChecked() else "Вкл"
        bg_color = Qt.red if self.isChecked() else Qt.green

        radius = 10
        height = 40
        width = 100
        w2=50
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(255,255,255))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        """
        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
        if not self.isChecked():
            #painter.drawText(-radius, -radius, width+radius, 2*radius, Qt.AlignLeft|Qt.AlignVCenter, "Qwerty")
            painter.drawText(0+radius, -radius, width+radius, 2*radius, Qt.AlignLeft|Qt.AlignVCenter, "Qwerty")
        else:
            painter.drawText(radius-width, -radius, width+radius, 2*radius, Qt.AlignLeft|Qt.AlignVCenter, "Qwerty")
        """
        painter.drawRoundedRect(QRect(-width, -height, 2*width, 2*height), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(width-w2-radius, -height, w2 + radius, 2*height)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
        if not self.isChecked():
            painter.drawText(0+radius, -height, width+radius, 2*height, Qt.AlignLeft|Qt.AlignVCenter, "Герметичность")
        else:
            painter.drawText(radius-width, -height, width+radius, 2*height, Qt.AlignLeft|Qt.AlignVCenter, "Герметичность")

        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 350)
        MainWindow.setMinimumSize(QtCore.QSize(550, 350))
        MainWindow.setMaximumSize(QtCore.QSize(550, 350))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        self.sw = MySwitch(self.centralwidget)
        self.sw.setChecked(True)
        #self.sw.setGeometry(QtCore.QRect(100, 10, 200, 100))


        MainWindow.setCentralWidget(self.centralwidget)
        

        #self.retranslateUi(MainWindow)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)


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