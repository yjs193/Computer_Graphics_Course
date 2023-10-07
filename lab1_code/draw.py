"""
Author: Johnson
Time：2023-09-29 12:59
"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def draw_axes():
    glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）

    # 以红色绘制x轴
    glColor4f(1.0, 0.0, 0.0, 1.0)  
    glVertex3f(-2, 0.0, 0.0)  
    glVertex3f(2, 0.0, 0.0)  

    # 以绿色绘制y轴
    glColor4f(0.0, 1.0, 0.0, 1.0)  
    glVertex3f(0.0, -2, 0.0)  
    glVertex3f(0.0, 2, 0.0)  

    # 以蓝色绘制z轴
    glColor4f(0.0, 0.0, 1.0, 1.0)  
    glVertex3f(0.0, 0.0, -2)  
    glVertex3f(0.0, 0.0, 2) 

    glEnd()  # 结束绘制线段


def draw_triangle():
    draw_axes()

    glBegin(GL_TRIANGLES) 

    glColor4f(1.0, 0.0, 0.0, 1.0)  
    glVertex3f(-0.5, -0.366, -0.5)  
    glColor4f(0.0, 1.0, 0.0, 1.0)  
    glVertex3f(0.5, -0.366, -0.5)  
    glColor4f(0.0, 0.0, 1.0, 1.0) 
    glVertex3f(0.0, 0.5, -0.5)  

    glEnd()  

    # ---------------------------------------------------------------
    glBegin(GL_TRIANGLES)  

    glColor4f(1.0, 0.0, 0.0, 1.0)  
    glVertex3f(-0.5, 0.5, 0.5) 
    glColor4f(0.0, 1.0, 0.0, 1.0)  
    glVertex3f(0.5, 0.5, 0.5)  
    glColor4f(0.0, 0.0, 1.0, 1.0)  
    glVertex3f(0.0, -0.366, 0.5)  

    glEnd()  


def draw_obj(vertices, faces, model_num):
    # glScalef(3, 3, 3)  # 缩放（X,Y,Z）
    draw_axes()

    if model_num == 3:
        glBegin(GL_TRIANGLES)
        glColor4f(0, 1.0, 1.0, 0.9)
        for face in faces:
            # print(len(face))
            for vertex_id in face:
                glVertex3fv(vertices[vertex_id])
        glEnd()
    elif model_num == 4:
        glBegin(GL_QUADS)
        glColor4f(0, 1.0, 1.0, 0.9)
        # print(faces)
        for face in faces:
            # print(len(face))
            for vertex_id in face:
                glVertex3fv(vertices[vertex_id])
        glEnd()


def determine_mesh_type(faces):
    num_faces = len(faces)
    if num_faces == 0:
        return "无效的模型"
    elif all(len(face) == 3 for face in faces):
        return 3
    elif all(len(face) == 4 for face in faces):
        return 4
    else:
        return "多边形网格模型"


