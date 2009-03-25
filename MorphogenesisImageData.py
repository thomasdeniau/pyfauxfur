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
from time import time

from OpenGL.GL import *
from OpenGL.GLU import *

class MorphogenesisImageData:
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
    print '-r -s', D_s, '-a', D_a, '-b', D_b, '-d', beta_i, '-x', width, '-y', height
    print ''
      
    self.width  = width
    self.height = height
    
    self.generate('stripe')
    
    self.texture_id = glGenTextures(1) # Generate 1 texture name
    glBindTexture(GL_TEXTURE_2D, self.texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    blank = (GLubyte * (width * height * 4))()
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, 
                 GL_RGBA, GL_UNSIGNED_BYTE, blank)
    glFlush()
        
    self.texture_row_length = 3*width
    if self.texture_row_length & 0x1:
      self.alignment = 1
    elif self.texture_row_length & 0x2:
      self.alignment = 2
    else:
      self.alignment = 4
             
    self.D_s    = D_s
    self.D_a    = D_a
    self.D_b    = D_b
    self.beta_i = beta_i
    
    self.iteration = 0
    self.fps = 0
    self.last_time = 1
  
  def generate(self, generator):
    self.grid_a = 8 * random.rand(self.width, self.height)
    self.grid_b = 8 * random.rand(self.width, self.height)
    
    if generator == 'stripe':
      self.grid_a = self.grid_a / 8
      self.grid_a[self.width / 2, :] = 8
  
  def make_texture(self):
    '''
    Calculates the colors for each point in the grid, and then copies this
    data into the image.
    '''
    
    z = zeros((self.width, self.height), 'd')
    
    min = self.grid_a.min()
    max = self.grid_a.max()
    
    g = (self.grid_a - min) / (max - min)
    
    self.grid = (255 * dstack((g, g, z))).astype('u1')

  def dirty(self):
    '''
    Force an update of the texture data.
    '''
    glPushClientAttrib(GL_CLIENT_PIXEL_STORE_BIT)
    glPixelStorei(GL_UNPACK_ALIGNMENT, self.alignment)
    glPixelStorei(GL_UNPACK_ROW_LENGTH, self.width)
    glTexSubImage2Dub(GL_TEXTURE_2D, 0, 0, 0, GL_RGB, self.grid)

    glPopClientAttrib()
  
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
      double A_ij, B_ij;
      
      for (i = 0; i < width; i++) {
        // Treat the surface as a torus by wrapping at the edges
        iplus1  = i < width - 1 ? i + 1 : 0;
        iminus1 = i > 0 ? i - 1 : width - 1;
      
        for (j = 0; j < height; j++) {
          jplus1  = j < height - 1 ? j + 1 : 0;
          jminus1 = j > 0 ? j - 1 : height - 1;
          
          A_ij = A_o(i, j); B_ij = B_o(i, j);
          
          // Component A
          A_n(i, j) = A_ij
            // Reaction component
            + D_s * (16.0 - A_ij * B_ij)
            // Diffusion component
            + D_a * (A_o(iplus1, j) - 2.0 * A_ij + A_o(iminus1, j) + A_o(i, jplus1) - 2.0 * A_ij + A_o(i, jminus1));
          
          A_ij = A_n(i, j);
          
          if (A_ij < 0.0) {
            A_n(i, j) = 0.0;
          } else if (A_ij > 8.0) {
            A_n(i, j) = 8.0;
          }
          
          // Component B
          B_n(i, j) = B_ij
            // Reaction component
            + D_s * (A_ij * B_ij - B_ij - beta_i)
            // Diffusion component
            + D_b * (B_o(iplus1, j) - 2.0 * B_ij + B_o(iminus1, j) + B_o(i, jplus1) - 2.0 * B_ij + B_o(i, jminus1));
          
          B_ij = B_n(i, j);

          if (B_ij < 0.0) {
            B_n(i, j) = 0.0;
          } else if (B_ij > 8.0) {
            B_n(i, j) = 8.0;
          }
        }
      }
      ''',
      ['D_s', 'D_a', 'D_b', 'beta_i', 'height', 'width', 'A_o', 'A_n', 'B_o', 'B_n'],
      type_converters=weave.converters.blitz)
    
    self.grid_a = A_n
    self.grid_b = B_n
    
    self.last_time = time() - t
    self.fps = self.fps * 29. / 30. + 1. / (self.last_time * 30.)
    
  def verboseStep(self):
    print 'Start iteration', self.iteration
    
    self.step()
    
    print 'mean(A) =', self.grid_a.mean(), 'mean(B) =', self.grid_b.mean()
    
    print 'Time : %fs'%self.last_time
  
  def logDebugInfo(self):
    print "Min A : %f, Min B : %f" %(self.grid_a.min(), self.grid_b.min())
    print "Mean A : %f, Mean B : %f" %(self.grid_a.mean(), self.grid_b.mean())
    print "Max A : %f, Max B : %f" %(self.grid_a.max(), self.grid_b.max())
  
  def imageName(self):
    return 'D_s=%s-D_a=%s-D_b=%s-beta_i=%s-iter=%d'%(
      str(self.D_s), str(self.D_a), str(self.D_b), str(self.beta_i), self.iteration)
  
  def __repr__(self):
    return str((self.grid_a, self.grid_b))

class MorphogenesisImageDataTests(unittest.TestCase):
  def setUp(self):
    self.texture = MorphogenesisImageData(400, 400, 0.04, 0.25, 0.0625, 12)
  
  def testImageName(self):
    self.assertEqual(self.texture.imageName(), 'D_s=0.04-D_a=0.25-D_b=0.0625-beta_i=12.png')
  
  def testStep(self):
    self.texture.verboseStep()
    
    self.texture.verboseStep()
    
    self.texture.verboseStep()
    
    self.texture.verboseStep()
    
    self.texture.verboseStep()

if __name__ == '__main__':
  unittest.main()
