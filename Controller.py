from PyQt4 import QtCore, QtGui

from MainWindow import *
from MorphogenesisImageData import MorphogenesisImageData

import sys

import time

class WorkerThread ( QtCore.QThread ):
    def __init__(self, controller, texture):
        QtCore.QThread.__init__(self)
        self.controller = controller
        self.texture = texture
        self.halt = False
        
    def run ( self ):
        while not self.halt:
            self.texture.step()
            time.sleep(0.001)

class Controller:        
    def __init__(self, window):
        self.window = window
        self.worker = None
        self.texture = None
        self.running = False
        self.timer = QtCore.QTimer()
    
    def setThreadRunning(self, flag):
        self.running = flag
        self.window.ui.pauseButton.setEnabled(flag)
        self.window.ui.runButton.setEnabled(not flag)
    
    def setThreadFinished(self):
        self.setThreadRunning(False)
        
    def awake(self):
        QtCore.QObject.connect(self.window.ui.runButton, QtCore.SIGNAL("clicked()"), self.run)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.window.ui.widget.updateGL )
        QtCore.QObject.connect(self.window.ui.initButton, QtCore.SIGNAL("clicked()"), self.init)
        QtCore.QObject.connect(self.window.ui.stepButton, QtCore.SIGNAL("clicked()"), self.step)
        QtCore.QObject.connect(self.window.ui.pauseButton, QtCore.SIGNAL("clicked()"), self.pause)
        QtCore.QObject.connect(QtCore.QCoreApplication.instance(), QtCore.SIGNAL("aboutToQuit()"), self.cleanup)
        self.setThreadRunning(False)
        
    def pause(self):
        self.timer.stop()
        if self.worker is not None:
            self.worker.halt = True

    def cleanup(self):
        if self.worker is not None:
            self.worker.halt = True
            
    def init(self):
        self.pause()
        
        da = float(self.window.ui.daField.text())
        db = float(self.window.ui.dbField.text())
        ds = float(self.window.ui.dsField.text())
        beta = float(self.window.ui.betaField.text())
        width = self.window.ui.widthSlider.value()
        height = self.window.ui.heightSlider.value()
        
        self.texture = MorphogenesisImageData(width, height, ds, da, db, beta)
        self.window.ui.widget.setTexture(self.texture)
        self.window.ui.widget.makeCurrent()
        self.texture.blit(0, 0)
    
    def step(self):
        if self.texture == None:
            self.init()
        self.texture.step()
        self.window.ui.widget.updateGL()
        
    def run(self):
        if self.texture == None:
            self.init()
        if not self.running:
            self.worker = WorkerThread(self, self.texture)
            QtCore.QObject.connect(self.worker, QtCore.SIGNAL("finished()"), self.setThreadFinished)
            self.worker.start()
            self.timer.start(40)
            self.setThreadRunning(True)
            
    def setOptions(self, options):
        self.window.ui.daField.setText(str(options.D_a))
        self.window.ui.dbField.setText(str(options.D_b))
        self.window.ui.dsField.setText(str(options.D_s))
        self.window.ui.betaField.setText(str(options.beta_i))
        self.window.ui.widthSlider.setValue(options.width)
        self.window.ui.heightSlider.setValue(options.height)