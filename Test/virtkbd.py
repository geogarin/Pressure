import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QSlider, QComboBox, QCheckBox, QWidget, QMainWindow, QPushButton, QLabel, QGridLayout, QGroupBox, QRadioButton, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QRect, pyqtSlot, Qt
import subprocess

class MatchBoxLineEdit(QLineEdit):
    def focusInEvent(self, e):
        try:
            subprocess.Popen(["onboard"])
        except FileNotFoundError:
            pass

    def focusOutEvent(self,e):
        subprocess.Popen(["killall","onboard"])
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'GUI TESTS'
        
        
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1025
        self.statusBarMessage = "GUI TEST"
        self.currentSprite = 'TEST.png'
        self.btn1Active = False
        self.btn2Active = False
        self.btn3Active = False
        self.btn4Active = False
        self.btn5Active = False
        self.btn6Active = False
        self.btn7Active = False
        self.btn8Active = False
        self.saveLocationDir = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage(self.statusBarMessage)

        self.userNameLabel = QLabel(self)
        self.userNameLabel.move(0,125)
        self.userNameLabel.setText("What is your name?")
        self.userNameLabel.resize(120,20)

        self.nameInput = MatchBoxLineEdit(self)
        self.nameInput.move(0,145)
        self.nameInput.resize(200,32)
        self.nameInput.setEchoMode(0)

        #self.showFullScreen()
        #self.nameInput.mousePressEvent=self.showKeyboard
        #self.nameInput.focusInEvent=self.showKeyboard

    


if __name__ == '__main__':
    app1 = QApplication(sys.argv)

    screen = app1.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))

    #m = MainModel()
    p = App()
    

    p.show()
    sys.exit(app1.exec_())

