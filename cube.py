#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

window = None

def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)

    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    window = glutCreateWindow("キューブテスト")
    glutDisplayFunc(display) # 描画関数を登録
    glutReshapeFunc(reshape) # リサイズコールバック関数を登録
    glutKeyboardFunc(keyboard)

    init(300, 300)
    glutMainLoop()

def init(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0) # クリア色の指定
    glEnable(GL_DEPTH_TEST) # 隠面消去を有効

    # 座標系の設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0) # 投影変換

def display():
    """描画処理"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # 画面のクリア

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # 視野変換：カメラの位置と方向のセット
    gluLookAt(-3.0, 2.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) # カメラの位置(f,f,f), 狙う方向(f,f,f), カメラの上方向(f,f,f)

    draw_cube() # 立方体を描く

    glFlush() # OpenGLコマンドの強制実行

def reshape(width, height):
    """画面サイズの変更時に呼び出されるコールバック関数"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0) # 投影変換

def draw_cube():
    glBegin(GL_QUADS)
    # 上面（緑）
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)   # A
    glVertex3f(-1.0, 1.0, -1.0)  # B
    glVertex3f(-1.0, 1.0, 1.0)   # C
    glVertex3f(1.0, 1.0, 1.0)    # D
    # 下面（オレンジ）
    glColor3f(1, 0.5, 0)
    glVertex3f(1.0, -1.0, -1.0)  # E
    glVertex3f(-1.0, -1.0, -1.0) # F
    glVertex3f(-1.0, -1.0, 1.0)  # G
    glVertex3f(1.0, -1.0, 1.0)   # H
    # 前面（赤）
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)    # D
    glVertex3f(-1.0, 1.0, 1.0)   # C
    glVertex3f(-1.0, -1.0, 1.0)  # G
    glVertex3f(1.0, -1.0, 1.0)   # H
    # 背面（黄色）
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)   # A
    glVertex3f(-1.0, 1.0, -1.0)  # B
    glVertex3f(-1.0, -1.0, -1.0) # F
    glVertex3f(1.0, -1.0, -1.0)  # E
    # 左側面（青）
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)   # C
    glVertex3f(-1.0, 1.0, -1.0)  # B
    glVertex3f(-1.0, -1.0, -1.0) # F
    glVertex3f(-1.0, -1.0, 1.0)  # G
    # 右側面（マゼンタ）
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)    # D
    glVertex3f(1.0, 1.0, -1.0)   # A
    glVertex3f(1.0, -1.0, -1.0)  # E
    glVertex3f(1.0, -1.0, 1.0)   # H
    glEnd()

def keyboard(key, x, y):

    if key == "\033": # ESC
        glutDestroyWindow(window)
        sys.exit()

if __name__ == "__main__":
    main()
