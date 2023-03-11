
"""
This module uses the main graphics application to render a triangle
"""

# Import Python modules
import glm
import numpy as np
import pygame as pg

class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='textures/test.png')
        self.on_init()

    def get_texture(self, path):
        # NOTE: Flip the texture along the Y-axis because PyGame has a downward Y-axis
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture

    def update(self):
        # Rotate model around the Y-axis
        m_model = glm.rotate(self.m_model, self.app.time * 0.5, glm.vec3(0, 1, 0))
        self.shader_program['m_model'].write(m_model)
        # Move camera around the user's input
        self.shader_program['m_view'].write(self.app.camera.m_view)

    def get_model_matrix(self):
        # NOTE: This is just an identity matrix
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        # NOTE: .use() assigns a uniform texture to a shader program
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        # NOTE: .write(x) assigns a uniform value to a shader program
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        # Release all data from memory
        # NOTE: OpenGL does not have garbage collection
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        # Associate the vertex buffer object with the shader program
        # NOTE: This takes the VBO and converts it to their respective data arrays
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
        return vao

    def get_vertex_data(self):
        # Get vertex coordinates and convert it to float32
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]

        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        # NOTE: We horizontally concatonate tex_coord and vertex data
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data

    @staticmethod
    def get_data(vertices, indices):
        # NOTE: Uses list comprehension to Outputs large list of tuples!
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        # Get the vertex shader source code
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        # Get the fragment shader source code
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        # Compile the vertex and fragment shader to the application
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program