from PyQt4 import QtCore, QtGui
from Ui_MainWindow import Ui_MainWindow


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)