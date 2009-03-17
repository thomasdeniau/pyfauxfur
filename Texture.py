#!/usr/bin/env python
# encoding: utf-8
"""
Texture.py

Created by Olivier Le Floch on 2009-03-17.
Program written by Thomas Deniau and Olivier Le Floch.
Copyright (c) 2009. All rights reserved.
"""

import unittest
from numpy import zeros, dot

class Texture:
  def __init__(self, width, height, D_s, D_a, D_b, beta_i):
    self.width  = width
    self.height = height
    
    self.D_s    = D_s
    self.D_a    = D_a
    self.D_b    = D_b
    self.beta_i = beta_i
    
    self.dx2     = 1.0 / width**2
    self.dy2     = 1.0 / height**2
    self.dnr_inv = 0.5 / (self.dx2 + self.dy2)
    
    self.grid_a = zeros((width, height), 'd')
    self.grid_b = zeros((width, height), 'd')
  
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

class TextureTests(unittest.TestCase):
  def setUp(self):
    pass

if __name__ == '__main__':
  unittest.main()
