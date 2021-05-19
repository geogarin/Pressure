from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt


class QLineEditVK(QLineEdit):
    def __init__(self):
        super().__init__()
        #self.mainWindowObj = parent

        self.setFocusPolicy(Qt.ClickFocus)
        self.ignoreOpenKeyboard = False

    def focusInEvent(self, e):
        print(f'focus in {e.reason()}')
        if (e.reason()==Qt.MouseFocusReason):
        #if (not self.ignoreOpenKeyboard):
        #if (True):
        #    self.ignoreOpenKeyboard = True
            self.keyboard.currentTextBox = self
            self.keyboard.show()
            #self.mainWindowObj.virtualKeyboardWidget.currentTextBox = self
            #self.mainWindowObj.virtualKeyboardWidget.show()
            #self.mainWindowObj._model.setupSaved = False
            self.clearFocus()            
        ##else:
        ##    self.ignoreOpenKeyboard = False
        super(QLineEditVK, self).focusInEvent(e)
    #def mousePressEvent(self, e):
    #    super(QLineEditVK, self).mousePressEvent(e)