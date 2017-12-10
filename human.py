#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from numpy.random import *
import sys

from myInitialize import *
from myObjects import *
from decision import *

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
rHandBall = -1 #右手が持っているボールの番号
lHandBall = -1 #左手が持っているボールの番号

# 角度の限界
HAND_ANGLE_LIMIT = 60.0
"""あとで消す"""
tmp_rangle_change = 8.0
tmp_langle_change = 8.0
tmp_throw = 0

# 人の座標
px = 0.0
pz = 0.0
py = 1.6
r = 30.0

# ボールの座標 (x,y,z)
ballPosition = [[0.3, 0.95, 0.4],
                [-0.3, 2.0, 0.4],
                [-0.3, 0.95, 0.4]]

# 0でないならキャッチされない
ballRelease = [0, 0, 0]

ballVelocity = [[0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]]

BALL_SIZE = 0.1 # ボールの半径
BALL_NUM = 3    # ボールの数

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

    global rHandPosition, lHandPosition

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
    glTranslated(ballPosition[0][0], ballPosition[0][1], ballPosition[0][2])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.2, 0.8, 1.0]);
    glutSolidSphere(BALL_SIZE, 20, 20)

    glLoadIdentity()
    glTranslated(ballPosition[1][0], ballPosition[1][1], ballPosition[1][2])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.8, 0.2, 1.0]);
    glutSolidSphere(BALL_SIZE, 20, 20)

    glLoadIdentity()
    glTranslated(ballPosition[2][0], ballPosition[2][1], ballPosition[2][2])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.8, 0.8, 1.0]);
    glutSolidSphere(BALL_SIZE, 20, 20)

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



    # 描画反映
    glFlush()

""" １フレーム毎の処理 """
def idle():
    """アイドル時に呼ばれるコールバック関数"""
    global frame
    global time
    global lAngle, rAngle
    global lHandBall, rHandBall
    global tmp_langle_change, tmp_rangle_change, tmp_throw


    frame = frame + 1
    time = time + dt

    # 手関連
    # 手の角度を往復させる
    rAngle = rAngle + tmp_rangle_change * rand() * 2 - tmp_rangle_change
    lAngle = lAngle + tmp_langle_change * rand() * 2 - tmp_langle_change

    # 手首座標の更新
    lHandPosition = [0.3, 0.95, 0.0]
    lHandPosition[1] += ARM_LENGTH*sin(radians(lAngle-90))
    lHandPosition[2] += ARM_LENGTH*sin(radians(lAngle))

    rHandPosition = [-0.3, 0.95, 0.0]
    rHandPosition[0] += ARM_LENGTH*sin(radians(-rAngle))
    rHandPosition[2] += ARM_LENGTH*cos(radians(rAngle))


    if rAngle >= HAND_ANGLE_LIMIT:
        rAngle = HAND_ANGLE_LIMIT
    elif rAngle <= -HAND_ANGLE_LIMIT:
        rAngle = -HAND_ANGLE_LIMIT

    if lAngle >= HAND_ANGLE_LIMIT+90.0:
        lAngle = HAND_ANGLE_LIMIT+90.0
    elif lAngle <= -HAND_ANGLE_LIMIT+90.0:
        lAngle = -HAND_ANGLE_LIMIT+90.0

    # 手と球の衝突判定
    for i in range(BALL_NUM):
        lCheck = inSphere(lHandPosition[0], lHandPosition[1], lHandPosition[2], BALL_SIZE,
                          ballPosition[i][0], ballPosition[i][1], ballPosition[i][2], BALL_SIZE)

        rCheck = inSphere(rHandPosition[0], rHandPosition[1], rHandPosition[2], BALL_SIZE,
                          ballPosition[i][0], ballPosition[i][1], ballPosition[i][2], BALL_SIZE)

        # 左手と衝突
        if lCheck and lHandBall == -1 and ballRelease[i] == 0:
            lHandBall = i;
            for j in range(3):
                ballVelocity[i][j] = 0.0
                tmp_throw = 60  # あとで消す

        # 右手と衝突
        if rCheck and rHandBall == -1 and ballRelease[i] == 0:
            rHandBall = i;
            for j in range(3):
                ballVelocity[i][j] = 0.0

    # ボール関連
    # 速度変更処理
    for i in range(BALL_NUM):
        ballVelocity[i][1] = ballVelocity[i][1] - dt * g # 自由落下


    # 変位変更処理
    for i in range(BALL_NUM):
        for j in range(3):
            ballPosition[i][j] = ballPosition[i][j] + ballVelocity[i][j] * dt

    # 地面衝突処理
    for i in range(BALL_NUM):
        if ballPosition[i][1] < 0.0:
            ballVelocity[i][1] = 0.0
            ballPosition[i][1] = 0.0

    # 手にあるボールは手に追従させる
    if lHandBall != -1:
        for j in range(3):
            ballPosition[lHandBall][j] = lHandPosition[j]
            tmp_throw -= 1

    if rHandBall != -1:
        for j in range(3):
            ballPosition[rHandBall][j] = rHandPosition[j]

    # 投げたボールをすぐキャッチしないようにカウント
    for i in range(BALL_NUM):
        if ballRelease[i] > 0:
            ballRelease[i] -= 1

    """あとで消す 投げのテスト"""
    if tmp_throw <= -1:
        ballRelease[0] = 10
        lHandBall = -1
        throwball(0, 0.0, 3.0, 0.0)
        tmp_throw = 0



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

    ballVelocity[no][0] = vx
    ballVelocity[no][1] = vy
    ballVelocity[no][2] = vz



""" メイン呼び出し """
if __name__ == "__main__":
    main()
