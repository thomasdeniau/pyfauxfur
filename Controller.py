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
        self.worker = None
        self.timer = QtCore.QTimer(window)
        
    def awake(self):
        QtCore.QObject.connect(self.window.ui.runButton, QtCore.SIGNAL("clicked()"), self.run)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.window.ui.widget.updateGL )
        QtCore.QObject.connect(QtCore.QCoreApplication.instance(), QtCore.SIGNAL("aboutToQuit()"), self.cleanup)
    
    def cleanup(self):
        if self.worker is not None:
            self.worker.halt = True
        
    def run(self):
        da = float(self.window.ui.daField.text())
        db = float(self.window.ui.dbField.text())
        ds = float(self.window.ui.dsField.text())
        beta = float(self.window.ui.betaField.text())
        width = self.window.ui.widthSlider.value()
        height = self.window.ui.heightSlider.value()
        
        texture = MorphogenesisImageData(width, height, ds, da, db, beta)
        self.window.ui.widget.setTexture(texture)
        self.window.ui.widget.makeCurrent()
        texture.blit(0, 0)
        
        self.worker = WorkerThread(texture)
        self.worker.start()
        
        self.timer.start(0.04)

    def setOptions(self, options):
        self.window.ui.daField.setText(str(options.D_a))
        self.window.ui.dbField.setText(str(options.D_b))
        self.window.ui.dsField.setText(str(options.D_s))
        self.window.ui.betaField.setText(str(options.beta_i))
        self.window.ui.widthSlider.setValue(options.width)
        self.window.ui.heightSlider.setValue(options.height)