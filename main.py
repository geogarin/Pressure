import sys


# dif
PINS_DIF = [480,483,476,477]

# abs
PINS_ABS = [479,492,490,434]


class PressureMain(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.showFullScreen()

        self.channels = []
        self.mainLayout = QGridLayout()
        channelsQty = 4
        for i in range(channelsQty):
            print(i)
            model = PressureModel(PINS_ABS[i],PINS_DIF[i])
            ch = PressureChannel(f'Канал {i+1}',model)
            self.channels.append(ch)
            #self.groups.append(ch.getGroup())
            self.mainLayout.addWidget(self.channels[i].group,1,i,3,1)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(5000) 

        self.mainLayout.addWidget(self.progressBar,5,0,1,channelsQty)
        
        self.setLayout(self.mainLayout)

        




if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    pm = PressureMain()
    pm.show()
    sys.exit(app.exec_())

