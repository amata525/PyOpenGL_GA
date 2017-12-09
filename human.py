#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from myInitialize import *
from myObjects import *
from math import *
from numpy.random import *
import sys

window = None

light_position = [6.0, 7.0, 8.0, 1.0]

frame = 0
time = 0
FPS = 60.0
dt = 1.0/FPS

ARM_LENGTH = 0.4 # 腕の長さ
lAngle = 120.0 # 左肘関節x方向の角度
rAngle = 0.0 # 右肘関節y方向の角度

rHandPosition = [0.0, 0.0, 0.0] # 右手の位置
lHandPosition = [0.0, 0.0, 0.0] # 左手の位置

# 角度の限界
HAND_ANGLE_LIMIT = 60.0
"""あとで消す"""
tmp_rangle_change = 8.0
tmp_langle_change = 8.0

# 人の座標
px = 0.0
pz = 0.0
r = 30.0
py = 1.6

# ボールの座標
bpx = [1.0, 0.0]
bpy = [3.0, 0.0]
bpz = [0.0, 0.0]

# ボールの速度
bvx = [0.0, 0.0]
bvy = [0.0, 0.0]
bvz = [0.0, 0.0]

g = 9.8 # 重力定数

key_test = [0.0, 0.0, 0.0, 0.0] # キー入力テスト


""" メイン処理 """
def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)
    window = glutCreateWindow("Human Test")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)

    glutIdleFunc(idle)

    init()
    glutMainLoop()

""" 描画更新 """
def display():

    # 画面クリア
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    # 光源の位置設定
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)


    # 行列初期化
    glLoadIdentity()

    """シーンの描画"""

    # 地面
    myGround(0.0)

    # ボール生成
    glTranslated(bpx[0], bpy[0], bpz[0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.2, 0.8, 1.0]);
    glutSolidSphere(0.1, 20, 20)

    glLoadIdentity()
    glTranslated(bpx[1], bpy[1], bpz[1])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.8, 0.2, 1.0]);
    glutSolidSphere(0.01, 20, 20)


    """人モデルの描画"""
    glLoadIdentity()
    # マテリアルの設定
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.2, 0.2, 1.0]);

    # 人間モデルの位置と方向
    glTranslated(px, py, pz)
    glRotated(180.0, 0.0, 1.0, 0.0)

    # 頭
    glutSolidSphere(0.15, 20, 20)

    # 胴体
    glTranslated(0.0, -0.2, 0.0)
    myBox(0.4, 0.6, 0.3)

    # 右足
    glPushMatrix()
    glTranslated(0.11, -0.65, 0.0)
    myLeg(0.19, 0.35)
    glPopMatrix()

    # 左足
    glPushMatrix()
    glTranslated(-0.11, -0.65, 0.0)
    myLeg(0.19, 0.35)
    glPopMatrix()

    # 右腕
    glPushMatrix()
    glTranslated(0.30, 0.0, 0.0)
    myArm(0.16, ARM_LENGTH, 90.0, rAngle)
    glPopMatrix()

    # 左腕
    glPushMatrix()
    glTranslated(-0.30, 0.0, 0.0)
    myArm(0.16, ARM_LENGTH, lAngle, 0.0)
    glPopMatrix()


    """手座標の描画"""
    # マテリアルの設定
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.8, 0.2, 1.0]);



    # 左手の座標に球体を設置してみる
    glLoadIdentity()
    lHandPosition = [0.3, 0.95, 0.0]
    lHandPosition[1] += ARM_LENGTH*sin(radians(lAngle-90))
    lHandPosition[2] += ARM_LENGTH*sin(radians(lAngle))
    glTranslated(lHandPosition[0], lHandPosition[1], lHandPosition[2])
    glutSolidSphere(0.1, 20, 20)

    # 左手の座標に球体を設置してみる
    glLoadIdentity()
    rHandPosition = [-0.3, 0.95, 0.0]
    rHandPosition[0] += ARM_LENGTH*sin(radians(-rAngle))
    rHandPosition[2] += ARM_LENGTH*cos(radians(rAngle))
    glTranslated(rHandPosition[0], rHandPosition[1], rHandPosition[2])
    glutSolidSphere(0.1, 20, 20)


    # 描画反映
    glFlush()

""" １フレーム毎の処理 """
def idle():
    """アイドル時に呼ばれるコールバック関数"""
    global frame
    global time
    global rAngle, lAngle
    global bpx, bpy, bpz
    global bvx, bvy, bvz
    global tmp_langle_change, tmp_rangle_change


    frame = frame + 1
    time = time + dt

    # 速度変更処理
    bvy[0] = bvy[0] - dt * g #　自由落下

    # 変位変更処理
    bpx[0] = bpx[0] + bvx[0] * dt
    bpy[0] = bpy[0] + bvy[0] * dt
    bpz[0] = bpz[0] + bvz[0] * dt

    if bpy[0] < 0.0:
        bvy[0] = 0.0
        bpy[0] = 0.0

    if frame == 300:
        throwball(0, 0.0, 100.0, 0.1)

    # 手の角度を往復させる
    rAngle = rAngle + tmp_rangle_change * rand() * 2 - tmp_rangle_change
    lAngle = lAngle + tmp_langle_change * rand() * 2 - tmp_langle_change

    if rAngle >= HAND_ANGLE_LIMIT:
        rAngle = HAND_ANGLE_LIMIT
    elif rAngle <= -HAND_ANGLE_LIMIT:
        rAngle = -HAND_ANGLE_LIMIT

    if lAngle >= HAND_ANGLE_LIMIT+90.0:
        lAngle = HAND_ANGLE_LIMIT+90.0
    elif lAngle <= -HAND_ANGLE_LIMIT+90.0:
        lAngle = -HAND_ANGLE_LIMIT+90.0

    glutPostRedisplay()  # 再描画




def keyboard(key, x, y):

    global key_test

    if key == "\033": # ESC
        glutDestroyWindow(window)
        sys.exit()

    if key == GLUT_KEY_UP:
        key_test[0] = key_test[0] + 0.1;

    elif key == GLUT_KEY_DOWN:
        key_test[0] = key_test[0] - 0.1;

    elif key == GLUT_KEY_RIGHT:
        key_test[1] = key_test[1] + 0.1;

    elif key == GLUT_KEY_LEFT:
        key_test[1] = key_test[1] - 0.1;

    print key_test[0]
    print key_test[1]



""" モーション関連 """
# ボール射出関数
# どのボールを(no)どの方向へどれくらいの速度で投げるか(vx, vy, vz)
def throwball(no, vx, vy, vz):
    global bvx, bvy, bvz

    bvx[no] = vx
    bvy[no] = vy
    bvz[no] = vz



""" メイン呼び出し """
if __name__ == "__main__":
    main()
