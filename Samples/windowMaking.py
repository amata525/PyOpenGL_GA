#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)

    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("OpenGLウィンドウの表示")
    glutDisplayFunc(display) # 描画関数を登録

    init()
    glutMainLoop()

def init():
    glClearColor(0.5, 0.5, 0.5, 1.0) # クリア色の指定

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT) # 画面のクリア
    glFlush() # OpenGLコマンドの強制実行

if __name__ == "__main__":
    main()
