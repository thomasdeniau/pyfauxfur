from PyQt4.QtOpenGL import QGLWidget
from pyglet.gl import *

class GLWidget(QGLWidget):
    texture = None
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        
        if self.texture is not None:
            left = 0
            right = self.texture.width
            bottom = 0
            top = self.texture.height
        
            glMatrixMode(GL_PROJECTION);
            glLoadIdentity();
            
            aspect = float(width) / float(height)
            if aspect < 1.0:
                # window taller than wide 
                top /= aspect
            else:
                right *= aspect
            
            gluOrtho2D(left, right, bottom, top)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
    
    def setTexture(self, texture):
        self.texture = texture
        self.resizeGL(self.size().width(), self.size().height())

    def paintGL(self):
        if self.texture is not None:
            self.texture.make_texture()
            self.texture.dirty()
        else:
            glClearColor(0,0,0,0) # noir
            glClear(GL_COLOR_BUFFER_BIT)
            glFlush()