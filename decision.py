#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# 球と球の衝突判定を行う
# x1, y1, z1, r1:１つ目の球の座標と半径
# x2, y2, z2, r2:２つ目の球の座標と半径
def inSphere(x1, y1, z1, r1, x2, y2, z2, r2):
    in_tmp = (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2

    if in_tmp <= (r1+r2)**2:
        return True
    else:
        return False
