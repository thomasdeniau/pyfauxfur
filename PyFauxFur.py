#!/usr/bin/env python
# encoding: utf-8
"""
PyFauxFur.py

Created by Olivier Le Floch on 2009-03-17.
Program written by Thomas Deniau and Olivier Le Floch.
Copyright (c) 2009. All rights reserved.
"""

import sys
from optparse import OptionParser

program = 'PyFauxFur'
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
    '-r', '--autorun', dest='autorun', default=False, action='store_true',
    help='automatically launch morphogenesis')
  parser.add_option(
    '-i', '--iterations', dest='iterations', type='int', default=1000,
    help='when running automatically, stop after this many iterations',
    metavar='ITERATIONS')
  parser.add_option(
    '-p', '--dump_path', dest='dumpAtEndPath', type="string", default=None,
    help='when running automatically, if not empty, save the final image and quit',
    metavar='PATH')
  
  parser.add_option(
    '-s', dest='D_s', type="float", default=0.0005,
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
    '-x', '--width', dest='width', type="int", default=400,
    help="width of the generated texture [default: %default]", metavar='WIDTH')
  parser.add_option(
    '-y', '--height', dest='height', type="int", default=400,
    help="height of the generated texture [default: %default]", metavar='HEIGHT')
  
  parser.add_option(
    '-g', '--generator', dest='generator', type='string', default='random',
    help='generator to use for the initial conditions [default: %default] (other possible values: stripe)',
    metavar='NAME')
  
  (options, args) = parser.parse_args()
  
  if options.version:
    print program + ', ' + version
    quit()
  
  from PyQt4 import QtGui
  from MainWindow import MainWindow
  from Controller import Controller
  
  app = QtGui.QApplication(args)
  
  window = MainWindow()
  controller = Controller(window)
  controller.awake()
  controller.setOptions(options)
  
  window.show()
    
  if options.autorun:
    controller.run(maxIterations=options.iterations, dumpAtEndPath=options.dumpAtEndPath)

  app.exec_()

if __name__ == "__main__":
  sys.exit(main())
