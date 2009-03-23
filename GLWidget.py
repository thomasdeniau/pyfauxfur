from PyQt4.QtOpenGL import *
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
        # (x,y) in tex coordinates [0,1]x[0,1] -> (x,y) image
        self.texCoords = (GLfloat * 20)(
             0., 0.,    0., 0., 0.,
             1., 0.,    float(texture.width), 0., 0.,
             1., 1.,    float(texture.width), float(texture.height), 0.,
             0., 1.,    0., float(texture.height), 0.)
             
        self.resizeGL(self.size().width(), self.size().height())

    def paintGL(self):
        if self.texture is not None:
            self.texture.make_texture()
            self.texture.dirty()

            glPushAttrib(GL_ENABLE_BIT)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture.texture_id.value)
            glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
            glInterleavedArrays(GL_T2F_V3F, 0, self.texCoords)
            glDrawArrays(GL_QUADS, 0, 4)
            glPopClientAttrib()
            glPopAttrib()
        else:
            glClearColor(0,0,0,0) # noir
            glClear(GL_COLOR_BUFFER_BIT)
        glFlush()