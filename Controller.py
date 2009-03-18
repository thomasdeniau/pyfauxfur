from PyQt4 import Qt
from MainWindow import *
import sys

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()

#    app.setMainWidget(window)
    app.exec_()
