from PyQt4.QtOpenGL import QGLWidget

class GLWidget(QGLWidget):
    texture = None
    
    def paintGL(self):
        if self.texture is not None:
            self.texture.make_texture()
            self.texture.dirty()