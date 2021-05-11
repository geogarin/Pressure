import sys
from MainInterface import MainInterface
from MainModel import MainModel

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    m = MainModel()
    p = MainInterface(m)
    p.show()
    sys.exit(app.exec_())

