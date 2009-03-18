#!/usr/bin/env python
# encoding: utf-8
"""
Texture.py

Created by Olivier Le Floch on 2009-03-17.
Program written by Thomas Deniau and Olivier Le Floch.
Copyright (c) 2009. All rights reserved.

Portions of this code have been adapted from pygarrayimage :
  http://pypi.python.org/pypi/pygarrayimage/0.0.5
  http://code.astraw.com/projects/motmot/trac/browser/trunk/pygarrayimage

Please see the LICENSE file for this software and pygarrayimage's software
license.
"""

import unittest
import ctypes
from numpy import dstack, zeros
from pyglet.image import ImageData

class MorphogenesisImageData(ImageData):
  def __init__(self, width, height, D_s, D_a, D_b, beta_i):
    '''Initialize morphogenesis image data with specific calculation parameters

    :Parameters:
      `width` : int
        Width in pixels of the calculated image
      `height` : int
        Height in pixels of the calculated image
      `D_s` : float
      `D_a` : float
      `D_b` : float
      `beta_i` : float
    '''
    
    self.width  = width
    self.height = height
    
    self.data_ptr = ctypes.c_void_p()
    self.data_ptr.value = 0
    
    # TODO : Do we need to specify the 'pitch' keyword parameter ?
    super(MorphogenesisImageData, self).__init__(
      width, height, 'RGB', None)
    
    self.D_s    = D_s
    self.D_a    = D_a
    self.D_b    = D_b
    self.beta_i = beta_i
    
    self.dx2     = 1.0 / width**2
    self.dy2     = 1.0 / height**2
    self.dnr_inv = 0.5 / (self.dx2 + self.dy2)
    
    self.grid_a = zeros((width, height), 'd')
    self.grid_b = zeros((width, height), 'd')
  
  def _convert(self, format, pitch):
    if format == self._current_format and pitch == self._current_pitch:
      return self.data_ptr
    else:
      raise ValueError('Unable to retrieve the texture data without converting.')

  def view(self):
    '''
    Calculates the colors for each point in the grid, and then copies this
    data into the image.
    '''
    grid = (255 * dstack((self.grid_a, zeros((self.width, self.height), 'd'), self.grid_b))).astype('u1')
    array_interface = grid.__array_interface__
    
    data_ptr_int, readonly = array_interface['data']
    self.data_ptr.value = data_ptr_int
    
    # Maintain references so they're not deallacoted
    self.grid_retainer            = grid
    self.array_interface_retainer = array_interface
    
    self.dirty()
  
  def dirty(self):
    '''
    Force an update of the texture data.
    '''

    texture = self.texture
    internalformat = None
    self.blit_to_texture(
      texture.target, texture.level, 0, 0, 0, internalformat)
  
  def step(self):
    dx2     = self.dx2
    dy2     = self.dy2
    dnr_inv = self.dnr_inv
    
    g_a = self.grid_a
    g_b = self.grid_b
    
    g_a[1:-1, 1:-1] = ((g_a[0:-2, 1:-1] + g_a[2:, 1:-1]) * dy2
        + (g_a[1:-1,0:-2] + g_a[1:-1, 2:]) * dx2) * dnr_inv
    
    g_b[1:-1, 1:-1] = ((g_b[0:-2, 1:-1] + g_b[2:, 1:-1]) * dy2
        + (g_b[1:-1,0:-2] + g_b[1:-1, 2:]) * dx2) * dnr_inv
  
  def __repr__(self):
    print (self.grid_a, self.grid_b)

class TextureTests(unittest.TestCase):
  def setUp(self):
    pass

if __name__ == '__main__':
  unittest.main()