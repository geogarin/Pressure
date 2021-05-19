from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect

class RoundedRect(QWidget):
    def __init__(self,parent=None,width=90,height=180,radius=20,value=0):
        super().__init__(parent)
        
        self._w = width/2
        self._h = height/2
        self._r = radius
        self.value=value
        
        self.setMinimumWidth(int(2*self._w))
        self.setMinimumHeight(int(2*self._h))


    def setValue(self, val):
        if self.value != val:    
            self.value = val
            self.update()

    def paintEvent(self, event):
        
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
        pen.setWidth(1)
        
        painter.setPen(pen)
        
        painter.drawRoundedRect(QRect(-self._w, -self._h, 2*self._w, 2*self._h), self._r, self._r)


