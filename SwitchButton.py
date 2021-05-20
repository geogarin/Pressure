from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect
import Config
import stylesheets

class SwitchButton(QtWidgets.QPushButton):
    def __init__(self, parent = None,backText='',onText='',offText='',width=200,height=30,radius=10,selectorWidth=50):
        super().__init__(parent)
        self.backText = backText
        self.onText = onText
        self.offText = offText
        self._width = width/2
        self._height = height/2
        self._radius = radius
        self._selectorWidth = selectorWidth    

        self.setCheckable(True)
        self.setMinimumWidth(2*self._width)
        self.setMinimumHeight(2*self._height)

    def paintEvent(self, event):
        label = self.offText if self.isChecked() else self.onText
        bg_color = Qt.red if self.isChecked() else Qt.green
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(stylesheets.TimerInnerBackGround[0],stylesheets.TimerInnerBackGround[1],stylesheets.TimerInnerBackGround[2]))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.drawRoundedRect(QRect(-self._width, -self._height, 2*self._width, 2*self._height), self._radius, self._radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(self._width-self._selectorWidth-self._radius, -self._height, self._selectorWidth + self._radius, 2*self._height)
        if not self.isChecked():
            sw_rect.moveLeft(-self._width)
        painter.drawRoundedRect(sw_rect, self._radius, self._radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)
        if (self.backText!=''):
            if not self.isChecked():
                painter.drawText(0+self._radius, -self._height, self._width+self._radius, 2*self._height, Qt.AlignLeft|Qt.AlignVCenter, self.backText)
            else:
                painter.drawText(self._radius-self._width, -self._height, self._width+self._radius, 2*self._height, Qt.AlignLeft|Qt.AlignVCenter, self.backText)