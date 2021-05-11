import sys
from Channel import Channel
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QPushButton,QDialog,QLineEdit,QVBoxLayout,QHBoxLayout,QFrame,QGroupBox,QGridLayout,QStyleFactory,QDial,QSlider,QProgressBar
from PyQt5.QtCore import Qt,QTimer

class Example(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()


    def addChannel(self,group,w,h):

        #print(f'w={w} h={h}')

        #self.group = QGroupBox('Канал')


        #self.setWindowTitle('widget')
        button = QPushButton("Hello",group)
        #button.setGeometry(10,10,200,100)
        #button.show()

        dial = QDial(group)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        slider = QSlider(Qt.Horizontal, group)
        slider.setValue(40)

        #progressBar = QProgressBar()
        #progressBar.setRange(0, 10000)
        #progressBar.setValue(0)

        #timer = QTimer(self)
        #timer.timeout.connect(progressBar)
        #timer.start(1000)

        lay = QVBoxLayout()
        lay.addWidget(button)
        lay.addWidget(dial)
        lay.addWidget(slider)
        #lay.addStretch(1)

        group.setLayout(lay)


        """
        self.fr = QFrame(self)
        
        self.fr.setFrameRect(self.frameGeometry())
        self.fr.setFrameStyle(QFrame.Box)
        self.fr.setFrameShadow(QFrame.Raised)
        print(f'{self.fr.frameRect()}')
        """

        #p = self.palette()
        #p.setColor(self.backgroundRole(),Qt.red)
        #self.setPalette(p)
        #self.setAutoFillBackground(True)
        #self.setStyleSheet("background-color:red;")

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        minVal = self.progressBar.minimum()
        if curVal<=0: self.n=1
        if curVal>=maxVal: self.n=-1


        self.progressBar.setValue(curVal + self.n*(maxVal - minVal) // 100)
        
    def initUI(self):
        self.groups = []


        #cp = QDesktopWidget().availableGeometry().center()
        #qr = self.frameGeometry()
        #print(f'{qr}')
        #self.resize(300, 300)
        self.n = 1
        self.showFullScreen()
        
        #p = self.palette()
        #p.setColor(self.backgroundRole(),Qt.red)
        #self.setPalette(p)

        #self.setAutoFillBackground(True)
        #self.setStyleSheet("background-color:gray;")



        #self.center()
        #button = QPushButton("Hello",self)
        #button.setGeometry(100,100,200,100)
        #button.show()

        #self.setWindowTitle('Center')
        #w1 = Channel(self)
        #w1.initWidget(220,500)
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advanceProgressBar)
        self.timer.start(20)
        


        self.channels = []
        mainLayout = QGridLayout()
        channelsQty = 4
        for i in range(channelsQty):
            ch = Channel(f'Канал {i+1}')
            self.channels.append(ch)
            self.groups.append(ch.getGroup())
            mainLayout.addWidget(self.groups[i],1,i,3,1)
        mainLayout.addWidget(self.progressBar,5,0,1,channelsQty)
        
        self.setLayout(mainLayout)
        """
        self.g1 = QGroupBox('Канал 1')
        self.addChannel(self.g1,220,500)
        self.g2 = QGroupBox('Канал 2')
        self.addChannel(self.g2,220,500)
        self.g3 = QGroupBox('Канал 3')
        self.addChannel(self.g3,220,500)
        self.g4 = QGroupBox('Канал 4')
        self.addChannel(self.g4,220,500)
        self.g5 = QGroupBox('Канал 5')
        self.addChannel(self.g5,220,500)

        

        mainLayout = QGridLayout()
        #mainLayout = QHBoxLayout(self)
        
        mainLayout.addWidget(self.g1,0,0,3,1)
        mainLayout.addWidget(self.g2,0,1,3,1)
        mainLayout.addWidget(self.g3,0,2,3,1)
        mainLayout.addWidget(self.g4,0,3,3,1)
        mainLayout.addWidget(self.g5,0,4,3,1)
        mainLayout.addWidget(self.progressBar,4,0,2,5)
        """
        '''
        mainLayout.addWidget(self.g1)
        mainLayout.addWidget(self.g2)
        mainLayout.addWidget(self.g3)
        mainLayout.addWidget(self.g4)
        mainLayout.addWidget(self.progressBar)
        '''
        #mainLayout.setRowStretch(1,1)
        #mainLayout.setRowStretch(2,1)
        #mainLayout.setColumnStretch(0,1)
        #mainLayout.setColumnStretch(1,1)
        #self.setLayout(mainLayout)

        

        

        #QApplication.setStyle(QStyleFactory.create('Coffee'))








        """

        w2 = Channel(self)
        w2.initWidget(220,500)

        
        w3 = Channel(self)
        w3.initWidget(220,500)
        w4 = Channel(self)
        w4.initWidget(220,500)
        w5 = Channel(self)
        w5.initWidget(220,500)
        

        layHor = QHBoxLayout()
        layHor.addWidget(w1)
        layHor.addWidget(w2)
        layHor.addWidget(w3)
        layHor.addWidget(w4)
        layHor.addWidget(w5)
        self.setLayout(layHor)
        """

        """
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        """        



        self.show()

    
    def center(self):

        qr = self.frameGeometry()
        
        cp = QDesktopWidget().availableGeometry().center()
        #a = QDesktopWidget().availableGeometry()
    
        print(f'{qr} {cp}')
        
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    #app.setStyleSheet("background-color: yellow")
    #app.setStyle('Fusion')
    ex = Example()
    sys.exit(app.exec_())