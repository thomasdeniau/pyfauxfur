from PyQt4 import QtCore, QtGui

from MainWindow import *

import sys


class Controller:        
    def __init__(self, window):
        self.window = window
        self.timer = QtCore.QTimer(window)
        
    def awake(self):
        QtCore.QObject.connect(self.window.ui.runButton, QtCore.SIGNAL("clicked()"), self.run)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.window.ui.widget.updateGL )
        self.timer.start(0)
        
    def run(self):
        da = float(window.ui.daField.text())
        db = float(window.ui.dbField.text())
        ds = float(window.ui.dsField.text())
        beta = float(window.ui.betaField.text())
        width = window.ui.widthSlider.value()
        height = window.ui.heightSlider.value()
        
        
        print "bla"
        

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    window = MainWindow()
    controller = Controller(window)
    controller.awake()
    window.show()

    app.exec_()
