from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt,pyqtSignal


class QLineEditVK(QLineEdit):
    editDone = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)
    def focusInEvent(self, e):
        #print(f'focus in {e.reason()}')
        if (e.reason()==Qt.MouseFocusReason):
            #if not (self.keyboard.currentTextBox is None):
            #    self.keyboard.currentTextBox.editDone.emit()
            self.keyboard.currentTextBox = self           
            self.keyboard.show()
            #self.clearFocus()           
        super(QLineEditVK, self).focusInEvent(e)
    
    