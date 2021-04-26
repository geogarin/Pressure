import sys
from Interface.MainInterface import MainInterface
from Interface.MainModel import MainModel

from PyQt5.QtWidgets import QApplication

channelsQty = 4 # Взять из настроек!


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    m = MainModel(channelsQty)
    p = MainInterface(m)
    p.show()
    sys.exit(app.exec_())

