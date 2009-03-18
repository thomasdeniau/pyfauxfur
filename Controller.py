from PyQt4 import QtCore, QtGui

from MainWindow import *
from MorphogenesisImageData import MorphogenesisImageData

import sys

import threading

class WorkerThread ( threading.Thread ):
    def __init__(self, texture):
        self.texture = texture
        self.halt = False

        threading.Thread.__init__(self)
        
    def run ( self ):
        while not self.halt:
            self.texture.step()
            
class Controller:        
    def __init__(self, window):
        self.window = window
        self.timer = QtCore.QTimer(window)
        
    def awake(self):
        QtCore.QObject.connect(self.window.ui.runButton, QtCore.SIGNAL("clicked()"), self.run)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.window.ui.widget.updateGL )
        QtCore.QObject.connect(QtCore.QCoreApplication.instance(), QtCore.SIGNAL("aboutToQuit()"), self.cleanup)
    
    def cleanup(self):
        if self.worker is not None:
            self.worker.halt = True
        
    def run(self):
        da = float(window.ui.daField.text())
        db = float(window.ui.dbField.text())
        ds = float(window.ui.dsField.text())
        beta = float(window.ui.betaField.text())
        width = window.ui.widthSlider.value()
        height = window.ui.heightSlider.value()
        
        texture = MorphogenesisImageData(width, height, ds, da, db, beta)
        window.ui.widget.texture = texture
        window.ui.widget.makeCurrent()
        texture.blit(0, 0)
        
        self.worker = WorkerThread(texture)
        self.worker.start()
        
        self.timer.start(0.04)

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    window = MainWindow()
    controller = Controller(window)
    controller.awake()
    window.show()

    app.exec_()
