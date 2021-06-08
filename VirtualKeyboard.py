from PyQt5.QtWidgets import QDialog, QGridLayout,QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import  Qt, pyqtSignal,pyqtSlot,QSignalMapper

import Config
import stylesheets

class VirtualKeyboard(QDialog):
    
    def __init__(self,parent=None,buttonSize=70,digitsOnly=False):
        super().__init__(parent)
        self.currentTextBox = None
        self.p = parent
        self.buttonSize=buttonSize
        
        self.setWindowTitle(' ')
        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.onButtonPressed)
        #self.p.hideKeyboard.connect(self.onHideKeyboard)
        self.setModal(True)

        if (digitsOnly):
            self.initDigitKeyboard()
        else:
            self.initFullKeyboard()
    
    def initDigitKeyboard(self):
        layout = QGridLayout()
        positions = [(i, j) for i in range(3) for j in range(3)]
        keys=[((i, j),Config.KEYBOARD_CHARS[0][3*i+j]) for i in range(3) for j in range(3)]
        #for position, name in zip(positions, Config.KEYBOARD_CHARS):
        for position, name in keys:
            if name == ' ':
                continue
            button = QPushButton(name)
            button.setFixedHeight(self.buttonSize)
            button.setFixedWidth(self.buttonSize)
            button.setStyleSheet(stylesheets.VK_Button)
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button.KEY_CHAR)
            layout.addWidget(button, *position)

        name = Config.KEYBOARD_CHARS[0][9]
        buttonZero = QPushButton(name)
        buttonZero.setFixedHeight(self.buttonSize)
        buttonZero.setFixedWidth(self.buttonSize)
        buttonZero.setStyleSheet(stylesheets.VK_Button)
        buttonZero.KEY_CHAR = ord(name)
        buttonZero.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(buttonZero, buttonZero.KEY_CHAR)
        layout.addWidget(buttonZero, 3,1)
        
        # Back button
        back_button = QPushButton(Config.KEYBOARD_BUTTON_DELETE_DIGIT)
        back_button.setFixedHeight(self.buttonSize)
        back_button.setFixedWidth(self.buttonSize)
        back_button.setStyleSheet(stylesheets.VK_Button)
        back_button.KEY_CHAR = Qt.Key_Backspace
        layout.addWidget(back_button, 4, 2, 1, 1,Qt.AlignRight)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        
        # Done button
        done_button = QPushButton(Config.KEYBOARD_BUTTON_DONE)
        done_button.setFixedHeight(self.buttonSize)
        done_button.setFixedWidth(2*self.buttonSize)
        done_button.setStyleSheet(stylesheets.VK_Button)
        done_button.KEY_CHAR = Qt.Key_Home
        layout.addWidget(done_button, 4, 0, 1, 2)
        done_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
        

        self.setGeometry(0, 0, 3*self.buttonSize, 5*self.buttonSize)
        fg = self.frameGeometry()
        g=QtGui.QGuiApplication.primaryScreen().geometry()
        
        self.move((g.width()-fg.width())/2,g.height()-fg.height())       
        self.setLayout(layout)

    def initFullKeyboard(self):
        layout = QGridLayout()
        cols = len(Config.KEYBOARD_CHARS[0])
        rows = len(Config.KEYBOARD_CHARS)
        #positions = [(i, j) for i in range(rows) for j in range(cols))]
        keys=[((i, j),Config.KEYBOARD_CHARS[i][j]) for i in range(rows) for j in range(cols)]
       
        #for position, name in zip(positions, Config.KEYBOARD_CHARS):
        for position, name in keys:
            if name == ' ':
                continue
            button = QPushButton(name)
            button.setFixedHeight(self.buttonSize)
            button.setFixedWidth(self.buttonSize)
            button.setStyleSheet(stylesheets.VK_Button)
            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button.KEY_CHAR)
            layout.addWidget(button, *position)

        # Space button
        space_button = QPushButton(' ')
        space_button.setFixedHeight(self.buttonSize)
        space_button.setFixedWidth(6*self.buttonSize)
        space_button.setStyleSheet(stylesheets.VK_Button)        
        space_button.KEY_CHAR = Qt.Key_Space
        layout.addWidget(space_button, rows+1, 2, 1, cols-2-2,Qt.AlignCenter)
        space_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
        
        # Back button
        back_button = QPushButton(Config.KEYBOARD_BUTTON_DELETE)
        back_button.setFixedHeight(self.buttonSize)
        back_button.setFixedWidth(1.5*self.buttonSize)
        back_button.setStyleSheet(stylesheets.VK_Button)
        back_button.KEY_CHAR = Qt.Key_Backspace
        layout.addWidget(back_button, 0, cols, 1, 1,Qt.AlignRight)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        
        # Done button
        done_button = QPushButton(Config.KEYBOARD_BUTTON_DONE)
        done_button.setFixedHeight(2*self.buttonSize)
        done_button.setFixedWidth(2.5*self.buttonSize)
        done_button.setStyleSheet(stylesheets.VK_Button)
        done_button.KEY_CHAR = Qt.Key_Home
        layout.addWidget(done_button, 2, cols-1, 2, 2,Qt.AlignRight|Qt.AlignBottom)
        done_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
        

        self.setGeometry(0, 0, (cols-1)*self.buttonSize, (rows+1)*self.buttonSize)
        fg = self.frameGeometry()
        g=QtGui.QGuiApplication.primaryScreen().geometry()
        
        self.move((g.width()-fg.width())/2,g.height()-fg.height())       
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
            #self.hide()
            #self.onHideKeyboard()
            self.hide()
            self.currentTextBox.clearFocus()
            self.currentTextBox.editDone.emit()
            
    """        
    @pyqtSlot()
    def onHideKeyboard(self):
        self.currentTextBox.clearFocus()
        self.hide()
    """