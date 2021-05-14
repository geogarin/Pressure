from PyQt5.QtWidgets import QDesktopWidget, QDialog, QDialogButtonBox,QLineEdit, QGroupBox, QVBoxLayout,QWidget,QGridLayout,QProgressBar,QPushButton,QHBoxLayout,QMessageBox,QSpinBox
from PyQt5 import QtGui
from PyQt5.QtCore import QElapsedTimer, Qt,pyqtSlot,QSignalMapper

import Config

class VirtualKeyboard(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.currentTextBox = None
        self.buttonSize=70
        #self.setWindowFlags(Qt.Window|Qt.WindowTitleHint|Qt.CustomizeWindowHint)
        #setWindowFlags(Qt::Window | Qt::FramelessWindowHint);
        #self.setWindowFlags(Qt.WindowTitleHint|Qt.CustomizeWindowHint)
        self.setWindowTitle(' ')
        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.onButtonPressed)
        layout = QGridLayout()

        positions = [(i, j) for i in range(4) for j in range(10)]
       
        for position, name in zip(positions, Config.KEYBOARD_CHARS):
            if name == ' ':
                continue
            button = QPushButton(name)
            #button.setFont(QFont('Arial', 12))
            button.setFixedHeight(70)
            button.setFixedWidth(70)

            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button.KEY_CHAR)
            layout.addWidget(button, *position)

        # Space button
        space_button = QPushButton('Space')
        space_button.setFixedHeight(self.buttonSize)
        space_button.setFixedWidth(6*self.buttonSize)        
        space_button.KEY_CHAR = Qt.Key_Space
        layout.addWidget(space_button, 5, 2, 1, 6,Qt.AlignCenter)
        space_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
        
        # Back button
        back_button = QPushButton('Back')
        back_button.setFixedHeight(self.buttonSize)
        back_button.setFixedWidth(self.buttonSize)
        back_button.KEY_CHAR = Qt.Key_Backspace
        layout.addWidget(back_button, 0, 10, 1, 1,Qt.AlignRight)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        
        # Done button
        done_button = QPushButton('Done')
        done_button.setFixedHeight(2*self.buttonSize)
        done_button.setFixedWidth(2*self.buttonSize)
        done_button.KEY_CHAR = Qt.Key_Home
        layout.addWidget(done_button, 2, 9, 2, 2,Qt.AlignRight|Qt.AlignBottom)
        done_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
        

        self.setGeometry(0, 0, 11*self.buttonSize, 5*self.buttonSize)
        fg = self.frameGeometry()
        
        #ag=QDesktopWidget.availableGeometry().center()
        #sz=QDesktopWidget.availableGeometry(self)
        sz=QtGui.QGuiApplication.primaryScreen().geometry()
        print(f'{fg} {sz}')
        x=(sz.width()-fg.width())/2
        y=sz.height()-fg.height()
        self.move(x,y)
        
        self.setLayout(layout)

    def onButtonPressed(self, char_ord):
        txt = self.currentTextBox.text()
        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]
        elif char_ord == Qt.Key_Space:
            txt += ' '
        elif char_ord == Qt.Key_Home: 
            pass   
        else:
            txt += chr(char_ord)

        self.currentTextBox.setText(txt)

        if (char_ord==Qt.Key_Home):
            self.hide()
            
