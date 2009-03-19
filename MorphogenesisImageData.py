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
from numpy import dstack, random, zeros
from scipy import weave
from pyglet.image import ImageData
from time import time

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
    
    print 'Generating texture with the following parameters :'
    print '   Reaction rate =', D_s
    print 'A diffusion rate =', D_a
    print 'B diffusion rate =', D_b
    print '    B decay rate =', beta_i
    print ''
    print '   texture width =', width
    print '  texture height =', height
    print ''
    
    # TODO : Do we need to specify the 'pitch' keyword parameter ?
    super(MorphogenesisImageData, self).__init__(
      width, height, 'RGB', None)
      
    self.width  = width
    self.height = height
    
    self.grid_a = 8 * random.rand(width, height)
    self.grid_b = 8 * random.rand(width, height)
    
    self.data_ptr = ctypes.c_void_p()
    self.make_texture()
    
    self.D_s    = D_s
    self.D_a    = D_a
    self.D_b    = D_b
    self.beta_i = beta_i
    
    self.iteration = 0
    self.last_time = 1
  
  def _convert(self, format, pitch):
    if format == self._current_format and pitch == self._current_pitch:
      return self.data_ptr
    else:
      raise ValueError('Unable to retrieve the texture data without converting.')

  def make_texture(self):
    '''
    Calculates the colors for each point in the grid, and then copies this
    data into the image.
    '''
    
    # make sure to retain references to grid and array_interface in self to avoid garbage collecting
    
    self.grid = (255 * dstack((self.grid_a, zeros((self.width, self.height), 'd'), self.grid_b))).astype('u1')
    self.array_interface = self.grid.__array_interface__
    
    data_ptr_int, readonly = self.array_interface['data']
    self.data_ptr.value = data_ptr_int
    
  def dirty(self):
    '''
    Force an update of the texture data.
    '''
    texture = self.texture
    internalformat = None
    self.blit_to_texture(texture.target, texture.level, 0, 0, 0, internalformat)
  
  def step(self):
    D_s    = self.D_s
    D_a    = self.D_a
    D_b    = self.D_b
    beta_i = self.beta_i
    
    height = self.height
    width  = self.width
    
    A_o = self.grid_a
    A_n = zeros((width, height), 'd')
    B_o = self.grid_b
    B_n = zeros((width, height), 'd')
    
    self.iteration += 1
    
    t = time()
    
    weave.inline(
      '''
      #line 119 "MorphogenesisImageData.py"
      int i, j, iplus1, jplus1, iminus1, jminus1;
      double A_o_ij, B_o_ij;
      
      for (i = 0; i < width; i++) {
        // Treat the surface as a torus by wrapping at the edges
        iplus1  = i < width - 1 ? i + 1 : 0;
        iminus1 = i > 0 ? i - 1 : width - 1;
      
        for (j = 0; j < height; j++) {
          jplus1  = j < height - 1 ? j + 1 : 0;
          jminus1 = j > 0 ? j - 1 : height - 1;
          
          A_o_ij = A_o(i, j); B_o_ij = B_o(i, j);
          
          // Component A
          A_n(i, j) = A_o_ij
            // Reaction component
            + D_s * (16 - A_o_ij * B_o_ij)
            // Diffusion component
            + D_a * (A_o(iplus1, j) - 2.0 * A_o_ij + A_o(iminus1, j) + A_o(i, jplus1) - 2.0 * A_o_ij + A_o(i, jminus1));
          
          if (A_n(i, j) < 0.0) {
            A_n(i, j) = 0.0;
          }
          
          // Component B
          B_n(i, j) = B_o_ij
            // Reaction component
            + D_s * (A_o_ij * B_o_ij - B_o_ij - beta_i)
            // Diffusion component
            + D_b * (B_o(iplus1, j) - 2.0 * B_o_ij + B_o(iminus1, j) + B_o(i, jplus1) - 2.0 * B_o_ij + B_o(i, jminus1));
          
          if (B_n(i, j) < 0.0) {
            B_n(i, j) = 0.0;
          }
        }
      }
      ''',
      ['D_s', 'D_a', 'D_b', 'beta_i', 'height', 'width', 'A_o', 'A_n', 'B_o', 'B_n'],
      type_converters=weave.converters.blitz)
    
    self.grid_a = A_n
    self.grid_b = B_n
    
    self.last_time = time() - t
  
  def verboseStep(self):
    print 'Start iteration', self.iteration
    
    self.step()
    
    print 'mean(A) =', self.meanA(), 'mean(B) =', self.meanB()
    
    print 'FPS : ', self.fps()
  
  def meanA(self):
    return self.grid_a.mean()
  
  def meanB(self):
    return self.grid_b.mean()
  
  def fps(self):
    '''Return the number of frames per second based on the length of the last execution'''
    return "%.1f"%(1 / self.last_time)
  
  def __repr__(self):
    return str((self.grid_a, self.grid_b))

class MorphogenesisImageDataTests(unittest.TestCase):
  def setUp(self):
    self.texture = MorphogenesisImageData(400, 400, 0.04, 0.25, 0.0625, 12)
  
  def testStep(self):
    self.texture.verboseStep()
    
    self.texture.verboseStep()

if __name__ == '__main__':
  unittest.main()
