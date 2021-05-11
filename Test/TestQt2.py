from PyQt5 import QtGui, QtCore


#app = QtGui.QApplication([])
app = QtGui.QGuiApplication([])
window = QtGui.QWidget(f=QtCore.Qt.WindowStaysOnTopHint)

child_window = QtGui.QWidget(window, f=QtCore.Qt.Window)
child_window.resize(400, 300)

layout = QtGui.QVBoxLayout(window)
exit = QtGui.QPushButton('Exit')
exit.clicked.connect(app.exit)
layout.addWidget(exit)
create = QtGui.QPushButton('Create child window')
create.clicked.connect(child_window.show)
layout.addWidget(create)
layout.addStretch()

window.showFullScreen()

app.exec_()