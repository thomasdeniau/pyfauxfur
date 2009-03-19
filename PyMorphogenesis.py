#!/usr/bin/env python
# encoding: utf-8
"""
PyMorphogenesis.py

Created by Olivier Le Floch on 2009-03-17.
Program written by Thomas Deniau and Olivier Le Floch.
Copyright (c) 2009. All rights reserved.
"""

import sys
from optparse import OptionParser

program = 'PyMorphogenesis'
version = 'Version 0.1, written by Thomas Deniau and Olivier Le Floch (c) 2009'

def main(argv=None):
  if argv is None:
    argv = sys.argv
  
  parser = OptionParser()
  parser.add_option(
    '-V', '--version', dest='version', default=False,
    action="store_true",
    help="show version information and exit")
  
  parser.add_option(
    '-q', '--quiet', dest='quiet', default=False, action='store_true',
    help='be quiet when running')
  
  parser.add_option(
    '-s', dest='D_s', type="float", default=0.04,
    help="reaction rate parameter [default: %default]", metavar='RATE')
  parser.add_option(
    '-a', dest='D_a', type="float", default=0.25,
    help="diffusion rate parameter for a [default: %default]", metavar='RATE')
  parser.add_option(
    '-b', dest='D_b', type="float", default=0.0625,
    help="diffusion rate parameter for b [default: %default]", metavar='RATE')
  parser.add_option(
    '-d', dest='beta_i', type="float", default=12,
    help="decay rate for b [default: %default]", metavar='DECAY')
  
  parser.add_option(
    '-x', '--width', dest='width', type="int", default=20,
    help="width of the generated texture [default: %default]", metavar='WIDTH')
  parser.add_option(
    '-y', '--height', dest='height', type="int", default=20,
    help="height of the generated texture [default: %default]", metavar='HEIGHT')
  
  (options, args) = parser.parse_args()
  
  if options.version:
    print program + ', ' + version
    quit()
  
  from PyQt4 import QtGui, QtOpenGL
  from MainWindow import MainWindow
  from Controller import Controller
  
  f = QtOpenGL.QGLFormat();
  f.setDoubleBuffer(False);
  QtOpenGL.QGLFormat.setDefaultFormat(f);
  
  app = QtGui.QApplication(args)
  
  window = MainWindow()
  controller = Controller(window)
  controller.awake()
  controller.setOptions(options)
  window.show()

  return app.exec_()

if __name__ == "__main__":
  sys.exit(main())
