#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# 照明系
light_ambient = [1.0, 1.0, 1.0, 1.0]    # 環境光（白色）
light_diffuse = [1.0, 1.0, 1.0, 1.0]    # 拡散光（白色）
light_specular = [1.0, 1.0, 1.0, 1.0]   # 鏡面光（白色）
light_position = [2.0, 2.0, 1.0, 1.0]   # 照明の位置

# マテリアル系
no_mat = [0.0, 0.0, 0.0, 1.0]        # 反射しない
mat_ambient = [0.0, 0.0, 0.3, 1.0]   # 環境光の青成分だけ少し反射
mat_diffuse = [1.0, 0.0, 0.0, 1.0]  # 拡散光は赤成分のみ全反射
mat_specular = [1.0, 1.0, 1.0, 1.0]  # 鏡面光は全反射
mat_emission = [0.3, 0.3, 0.2, 0.0]  # 放射の色
no_shininess = [0.0]                 # 鏡面反射しない
low_shininess = [5.0]                # 弱い鏡面反射
high_shininess = [100.0]             # 強い鏡面反射


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Lighting Test")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    init(300, 300)
    glutMainLoop()

def init(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # ライティング周りの設定
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHTING) # ライティング有効
    glEnable(GL_LIGHT0)   # 設定したLIGHT0を有効

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # マテリアルの設定
    glMaterialfv(GL_FRONT, GL_AMBIENT, no_mat)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, no_mat)
    glMaterialfv(GL_FRONT, GL_SHININESS, no_shininess)
    glMaterialfv(GL_FRONT, GL_EMISSION, mat_emission)

    # 球体でテスト
    glutSolidSphere(1.0, 40, 40)

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
