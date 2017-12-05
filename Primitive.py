#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

window = None

def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)

    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    window = glutCreateWindow("プリミティブテスト")
    glutDisplayFunc(display) # 描画関数を登録
    glutKeyboardFunc(keyboard)

    init()
    glutMainLoop()

def init():
    glClearColor(0.0, 0.2, 1.0, 1.0) # クリア色の指定

    # 座標系の設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT) # 画面のクリア

    # 四角形を描く
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()

    glFlush() # OpenGLコマンドの強制実行

def keyboard(key, x, y):

    if key == "\033": # ESC
        glutDestroyWindow(window)
        sys.exit()

if __name__ == "__main__":
    main()
