from PyQt4.QtOpenGL import QGLWidget
from pyglet.gl import *

class GLWidget(QGLWidget):
    texture = None
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        
        if self.texture is not None:
            left = -self.texture.width
            right = self.texture.width
            bottom = -self.texture.height
            top = self.texture.height
        
            glMatrixMode(GL_PROJECTION);
            glLoadIdentity();
        
            aspect = float(width) / float(height)
            if aspect < 1.0:
                # window taller than wide 
                bottom /= aspect
                top /= aspect
            else:
                left *= aspect
                right *= aspect
            
            glOrtho(left, right, bottom, top, 1, 10)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
        
    def paintGL(self):
        self.resizeGL(self.size().width(), self.size().height())
        if self.texture is not None:
            self.texture.make_texture()
            self.texture.dirty()