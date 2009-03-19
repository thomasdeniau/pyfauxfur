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
        print "paintGL"
        if self.texture is not None:
            self.texture.make_texture()
            self.texture.dirty()
            #glEnable(GL_TEXTURE_2D)
            #glBindTexture(GL_TEXTURE_2D, self.texture.texture.id)
            #glBegin( GL_QUADS )
            #glTexCoord2d(0.0,0.0)
            #glVertex2d(0.0,0.0)
            #glTexCoord2d(1.0,0.0)
            #glVertex2d(self.texture.width,0.0)
            #glTexCoord2d(1.0,1.0)
            #glVertex2d(self.texture.width, self.texture.height)
            #glTexCoord2d(0.0,1.0)
            #glVertex2d(0.0,self.texture.height)
            #glEnd()
            self.texture.blit(0,0)
        else:
            glClearColor(0,0,0,0) # noir
            glClear(GL_COLOR_BUFFER_BIT)
        glFlush()