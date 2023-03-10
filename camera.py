
import glm

FOV = 50 # Value in degrees
NEAR = 0.1
FAR = 100

class Camera:
    def __init__(self, app):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        # Get camera/eye position and up-vector
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        # View matrix
        self.m_view = self.get_view_matrix()
        # Projection matrix
        self.m_proj = self.get_projection_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, glm.vec3(0), self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)