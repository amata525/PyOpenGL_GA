#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# 直方体の描画
def myBox(x, y, z):
    hx = x * 0.5
    hz = z * 0.5

    vertex = [
        [-hx,  -y, -hz],
        [ hx,  -y, -hz],
        [ hx, 0.0, -hz],
        [-hx, 0.0, -hz],
        [-hx,  -y, hz],
        [ hx,  -y, hz],
        [ hx, 0.0, hz],
        [-hx, 0.0, hz]
    ]

    face = [
        [0, 1, 2, 3],
        [1, 5, 6, 2],
        [5, 4, 7, 6],
        [4, 0, 3, 7],
        [4, 5, 1, 0],
        [3, 2, 6, 7]
    ]

    normal = [
        [0.0, 0.0, -1.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0],
        [0.0, 1.0, 0.0]
    ]

    glBegin(GL_QUADS)
    for j in range(6):
        glNormal3fv(normal[j])
        for i in range(3, -1, -1):
            glVertex3fv(vertex[face[j][i]])

    glEnd()

# 足
def myLeg(girth, length):
    myBox(girth, length, girth)
    glTranslated(0.0, -0.05 - length, 0.0)
    myBox(girth, length, girth)

def myArm(girth, length, rx, rz):
    myBox(girth, length, girth)
    glTranslated(0.0, -0.05 - length, 0.0)
    glRotated(rx, 1.0, 0.0, 0.0)
    glRotated(rz, 0.0, 0.0, 1.0)
    myBox(girth, length, girth)

# 地面
def myGround(height):
    ground = [
        [0.6, 0.6, 0.6, 1.0],
        [0.3, 0.3, 0.3, 1.0]
    ]

    glBegin(GL_QUADS)
    glNormal3d(0.0, 1.0, 0.0)

    for j in range(-10, 11, 1):
        for i in range(-10, 10, 1):
            glMaterialfv(GL_FRONT, GL_DIFFUSE, ground[(i+j) & 1])
            glVertex3f(float(i), height, float(j))
            glVertex3f(float(i), height, float(j+1))
            glVertex3f(float(i+1), height, float(j+1))
            glVertex3f(float(i+1), height, float(j))

    glEnd()
