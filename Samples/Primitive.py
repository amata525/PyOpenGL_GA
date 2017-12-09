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
    glClearColor(0.0, 0.0, 0.0, 1.0) # クリア色の指定

    # 座標系の設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 100, 0, 100)

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT) # 画面のクリア

    # 四角形を描く
    #glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)  # 赤
    glVertex2i(10, 10)
    glColor3f(0.0, 1.0, 0.0)  # 緑
    glVertex2i(20, 10)
    glColor3f(1.0, 0.0, 0.0)  # 赤
    glVertex2i(20, 20)
    glColor3f(1.0, 1.0, 0.0)  # 黄色
    glVertex2i(10, 20)
    glEnd()

    # 点の描画
    glColor3f(0.0, 0.2, 1.0)
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glVertex2i(30, 30)
    glVertex2i(35, 35)
    glVertex2i(40, 40)
    glEnd()

    # 線の描画
    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(31.4, 33.3)
    glVertex2f(31.4, 55.5)
    glEnd()

    # ポリゴンの描画
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_POLYGON)
    glVertex2i(90, 90)
    glVertex2i(95, 80)
    glVertex2i(95, 70)
    glVertex2i(90, 60)
    glVertex2i(85, 70)
    glVertex2i(85, 80)
    glEnd()


    glFlush() # OpenGLコマンドの強制実行

def keyboard(key, x, y):

    if key == "\033": # ESC
        glutDestroyWindow(window)
        sys.exit()

if __name__ == "__main__":
    main()
