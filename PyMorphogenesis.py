#!/usr/bin/env python
# encoding: utf-8
"""
PyMorphogenesis.py

Created by Olivier Le Floch on 2009-03-17.
Program written by Thomas Deniau and Olivier Le Floch.
Copyright (c) 2009. All rights reserved.
"""

import sys
import math
from optparse import OptionParser

from MorphogenesisImageData import MorphogenesisImageData

program = 'PyMorphogenesis'
version = 'Version 0.1, written by Thomas Deniau and Olivier Le Floch (c) 2009'

def main(argv=None):
  if argv is None:
    argv = sys.argv
  
  parser = OptionParser()
  parser.add_option(
    '-V', '--version', dest='version', default=False,
    action="store_true",
    help="show version information and exit", metavar='FILE')
  
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
  
  print 'Generating texture with the following parameters :'
  print '   Reaction rate =', options.D_s
  print 'A diffusion rate =', options.D_a
  print 'B diffusion rate =', options.D_b
  print '    B decay rate =', options.beta_i
  print ''
  print '   texture width =', options.width
  print '  texture height =', options.height
  print '...'
  
  texture = MorphogenesisImageData(
    options.width, options.height,
    options.D_s, options.D_a, options.D_b, options.beta_i)
  
  texture.blit(0, 0)
  
  # texture.step()
  # 
  # texture.make_texture()
  
  texture.dirty()
  
  print texture
  
  print 'Done !'

if __name__ == "__main__":
  import psyco
  psyco.full()
  
  sys.exit(main())
