#coding:utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from numpy.random import *
import numpy as np
import sys

from myInitialize import *
from myObjects import *
from decision import *

window = None

light_position = [6.0, 7.0, 8.0, 1.0]

frame = 0    # 経過フレーム
FPS = 60.0   # フレームレート
dt = 1.0/FPS # 単位時間
g = 9.8 # 重力定数

ARM_LENGTH = 0.4 # 腕の長さ
lAngle = 90.0 # 左肘関節x方向の角度
rAngle = 0.0 # 右肘関節y方向の角度

rHandPosition = [0.0, 0.0, 0.0] # 右手の位置
lHandPosition = [0.0, 0.0, 0.0] # 左手の位置
rHandBall = -1 #右手が持っているボールの番号
lHandBall = -1 #左手が持っているボールの番号

# 角度の限界
HAND_ANGLE_LIMIT = 60.0

# 人の座標
humanPosition = [0.0, 1.6, 0.0]

# ボールの座標 (x,y,z)
ballPosition = [[0.3, 0.95, 0.4],
                [-0.3, 2.0, 0.4],
                [-0.3, 0.95, 0.4]]

# 0でないならキャッチされない
ballRelease = [0, 0, 0]
# 左右交互にキャッチするためのフラグ
prevIsLeft = [0, 1, 1]

ballVelocity = [[0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]]

BALL_SIZE = 0.1 # ボールの半径
BALL_NUM = 3    # ボールの数

GENE_NUM = 20 # 遺伝子数
GENE_LEN = 100 # 単位遺伝子長
POWER_LEN = 10 # 単位射出遺伝子長
THROW_STEP = 10 # 射出間隔

armAngleGene = np.zeros((GENE_NUM, 2, GENE_LEN))   # 腕の角度遺伝子
leftPowerGene = np.zeros((GENE_NUM, 2, POWER_LEN))  # 左手の射出遺伝子
rightPowerGene = np.zeros((GENE_NUM, 2, POWER_LEN)) # 右手の射出遺伝子
nowGeneLength = GENE_LEN    # 現在の遺伝子長
nowPowerLength = POWER_LEN  # 現在の射出遺伝子長
nowGeneNo = 0               # 評価中の遺伝子番号

catchNum = np.zeros((GENE_NUM))
frameNum = np.zeros((GENE_NUM))
generation = 1


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

    # OpenGL関連の初期化
    init()

    # 遺伝子データの初期化
    geneInit()

    # 評価環境の初期化
    humanInit()

    # メインループ開始
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
    #glTranslated(px, py, pz)
    glTranslated(humanPosition[0], humanPosition[1], humanPosition[2])
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
    global frame
    global lAngle, rAngle
    global lHandBall, rHandBall
    global ballPosition, ballVelocity, ballRelease
    global nowGeneNo
    global generation
    global prevIsLeft

    end_flg = False

    # １個体の評価
    if frame < nowGeneLength:

        # 手関連
        # 手の角度を往復させる
        lAngle = lAngle + armAngleGene[nowGeneNo][1][frame]
        rAngle = rAngle + armAngleGene[nowGeneNo][1][frame]


        # 手首座標の更新
        lHandPosition = [0.3, 0.95, 0.0]
        lHandPosition[1] += ARM_LENGTH*sin(radians(lAngle-90))
        lHandPosition[2] += ARM_LENGTH*sin(radians(lAngle))

        rHandPosition = [-0.3, 0.95, 0.0]
        rHandPosition[0] += ARM_LENGTH*sin(radians(-rAngle))
        rHandPosition[2] += ARM_LENGTH*cos(radians(rAngle))

        # 制限角度内におさめる
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
            if lCheck and lHandBall == -1 and ballRelease[i] == 0 and prevIsLeft[i] == 0:
                lHandBall = i;
                catchNum[nowGeneNo] += 1
                prevIsLeft[i] = 1
                for j in range(3):
                    ballVelocity[i][j] = 0.0

            # 右手と衝突
            if rCheck and rHandBall == -1 and ballRelease[i] == 0 and prevIsLeft[i] == 1:
                rHandBall = i;
                catchNum[nowGeneNo] += 1
                prevIsLeft[i] = 0
                for j in range(3):
                    ballVelocity[i][j] = 0.0

        # ボール関連
        # 自由落下処理
        for i in range(BALL_NUM):
            ballVelocity[i][1] = ballVelocity[i][1] - dt * g


        # 変位処理
        for i in range(BALL_NUM):
            for j in range(3):
                ballPosition[i][j] = ballPosition[i][j] + ballVelocity[i][j] * dt

        # 地面衝突処理
        for i in range(BALL_NUM):
            if ballPosition[i][1] < 0.0:
                ballVelocity[i][1] = 0.0
                ballPosition[i][1] = 0.0
                end_flg = True

        # 手にあるボールは手に追従させる
        if lHandBall != -1:
            for j in range(3):
                ballPosition[lHandBall][j] = lHandPosition[j]

        if rHandBall != -1:
            for j in range(3):
                ballPosition[rHandBall][j] = rHandPosition[j]

        # 投げたボールをすぐキャッチしないようにカウント
        for i in range(BALL_NUM):
            if ballRelease[i] > 0:
                ballRelease[i] -= 1

        # ボール射出処理
        if frame % THROW_STEP == 0:
            throw_index = frame / THROW_STEP
            # 左手にボールがある
            if lHandBall != -1:
                throwball(lHandBall, leftPowerGene[nowGeneNo][0][throw_index], leftPowerGene[nowGeneNo][1][throw_index], 0.0)
                ballRelease[lHandBall] = 5
                lHandBall = -1

            # 右手にボールがある
            if rHandBall != -1:
                throwball(rHandBall, rightPowerGene[nowGeneNo][0][throw_index], rightPowerGene[nowGeneNo][1][throw_index], 0.0)
                ballRelease[rHandBall] = 5
                rHandBall = -1
    else:
        end_flg = True

    # 地面に着いたらその個体は評価終了
    if end_flg:
        frameNum[nowGeneNo] = frame
        humanInit()
        nowGeneNo += 1

        if nowGeneNo >= GENE_NUM:
            print '第', generation, '世代'
            print frameNum
            generation += 1
            nowGeneNo = 0
            geneCross()

            if generation == 501: # 501世代で終了
                glutDestroyWindow(window)
                sys.exit()

    else:
        glutPostRedisplay()  # 再描画
        frame = frame + 1




"""遺伝子操作関連"""
# 遺伝子配列の初期化
def geneInit():
    global armAngleGene
    global leftPowerGene, rightPowerGene

    for i in range(GENE_NUM):
        for j in range(GENE_LEN):
            armAngleGene[i][0][j] = rand() * 8.0 - 4.0
            armAngleGene[i][1][j] = rand() * 8.0 - 4.0

        for j in range(POWER_LEN):
            leftPowerGene[i][0][j] = rand() * (-1.0)
            leftPowerGene[i][1][j] = rand() * 3.0 + 4.0
            rightPowerGene[i][0][j] = rand() * 1.0
            rightPowerGene[i][1][j] = rand() * 3.0 + 4.0

# 腕角度遺伝子の追加
def appendArmGene():
    global armAngleGene
    global nowGeneLength

    g = np.zeros((GENE_NUM, 2, GENE_LEN))

    for i in range(GENE_NUM):
        for j in range(GENE_LEN):
            g[i][0][j] = rand() * 8.0 - 4.0
            g[i][1][j] = rand() * 8.0 - 4.0

    armAngleGene = np.append(armAngleGene, g, axis=2)
    nowGeneLength += GENE_LEN

# 射出遺伝子の追加
def appendPowerGene():
    global leftPowerGene, rightPowerGene
    global nowPowerLength

    gl = np.zeros((GENE_NUM, 2, POWER_LEN))
    gr = np.zeros((GENE_NUM, 2, POWER_LEN))

    for i in range(GENE_NUM):
        for j in range(POWER_LEN):
            gl[i][0][j] = rand() * (-1.0)
            gl[i][1][j] = rand() * 3.0 + 4.0
            gr[i][0][j] = rand() * 1.0
            gr[i][1][j] = rand() * 3.0 + 4.0

    leftPowerGene = np.append(leftPowerGene, gl, axis=2)
    rightPowerGene = np.append(rightPowerGene, gr, axis=2)
    nowPowerLength += POWER_LEN

# ルーレット選択
def geneSelect(values, sv):
    getTwoPear = False

    sum1 = 0
    sum2 = 0
    select1 = 0
    select2 = 0

    while not getTwoPear:
        selectValue1 = rand() * sv
        selectValue2 = rand() * sv

        sum1 += values[select1]
        sum2 += values[select2]

        while sum1 <= selectValue1:
            select1 += 1
            sum1 += values[select1]

        while sum2 <= selectValue2:
            select2 += 1
            sum2 += values[select2]

        if sum1 == sum2:
            sum1 = 0
            sum2 = 0
            select1 = 0
            select2 = 0
        else:
            return [select1, select2]

    return [0, 0]

# 一様交叉
def geneCross():
    global armAngleGene
    global leftPowerGene, rightPowerGene

    nextArmAngleGene = np.zeros((GENE_NUM, 2, nowGeneLength))   # 次の腕の角度遺伝子
    nextLeftPowerGene = np.zeros((GENE_NUM, 2, nowPowerLength))  # 次の左手の射出遺伝子
    nextRightPowerGene = np.zeros((GENE_NUM, 2, nowPowerLength)) # 次の右手の射出遺伝子

    # 評価値とその合計を計算
    geneValue = np.zeros(GENE_NUM)
    for i in range(GENE_NUM):
        geneValue[i] = frameNum[i] * catchNum[i]

    sumValue = sum(geneValue)

    # 最優秀個体はそのまま残す
    mostValueNo = np.argmax(geneValue)

    nextArmAngleGene[0][0] = armAngleGene[mostValueNo][0]
    nextArmAngleGene[0][1] = armAngleGene[mostValueNo][1]
    nextLeftPowerGene[0][0] = leftPowerGene[mostValueNo][0]
    nextLeftPowerGene[0][1] = leftPowerGene[mostValueNo][1]
    nextRightPowerGene[0][0] = rightPowerGene[mostValueNo][0]
    nextRightPowerGene[0][1] = rightPowerGene[mostValueNo][1]

    # 50世代毎に最も良い個体を記録
    if generation % 50 == 0:
        np.savetxt(("armMVP" + str(generation/50) + ".csv"), nextArmAngleGene[0], delimiter=",")
        np.savetxt(("leftMVP" + str(generation/50) + ".csv"), nextLeftPowerGene[0], delimiter=",")
        np.savetxt(("rightMVP" + str(generation/50) + ".csv"), nextRightPowerGene[0], delimiter=",")

    # ルーレット選択
    for i in range(1, GENE_NUM):
        parents = geneSelect(geneValue, sumValue)

        selectArmPoint = randint(0, 2, nowGeneLength)
        selectPowerPoint = randint(0, 2, nowPowerLength)

        for j in range(nowGeneLength):

            nextArmAngleGene[i][0][j] = armAngleGene[parents[selectArmPoint[j]]][0][j]
            nextArmAngleGene[i][1][j] = armAngleGene[parents[selectArmPoint[j]]][1][j]

        for j in range(nowPowerLength):
            nextLeftPowerGene[i][0][j] = leftPowerGene[parents[selectPowerPoint[j]]][0][j]
            nextLeftPowerGene[i][1][j] = leftPowerGene[parents[selectPowerPoint[j]]][1][j]
            nextRightPowerGene[i][0][j] = rightPowerGene[parents[selectPowerPoint[j]]][0][j]
            nextRightPowerGene[i][1][j] = rightPowerGene[parents[selectPowerPoint[j]]][1][j]

    armAngleGene = nextArmAngleGene
    leftPowerGene = nextLeftPowerGene
    rightPowerGene = nextRightPowerGene

    # 突然変異
    mutation()

    addGeneFlg = False
    for i in range(GENE_NUM):
        if frameNum[i] >= nowGeneLength:
            addGeneFlg = True

    if addGeneFlg:
        appendArmGene()
        appendPowerGene()

# 突然変異
# 選ばれた個体のうち選ばれた遺伝子データをランダムなものに改竄する
def mutation():
    global armAngleGene
    global leftPowerGene, rightPowerGene

    mutationRate = 0.2
    changeRate = 0.2

    for i in range(1, GENE_NUM):
        mu = rand()
        # 突然変異発生
        if mu <= mutationRate:
            for j in range(nowGeneLength):
                ch = rand()
                if ch <= changeRate:
                    armAngleGene[i][0][j] = rand() * 8.0 - 4.0
                    armAngleGene[i][1][j] = rand() * 8.0 - 4.0

            for j in range(nowPowerLength):
                ch = rand()
                if ch <= changeRate:
                    leftPowerGene[i][0][j] = rand() * (-1.0)
                    leftPowerGene[i][1][j] = rand() * 3.0 + 4.0

            for j in range(nowPowerLength):
                ch = rand()
                if ch <= changeRate:
                    rightPowerGene[i][0][j] = rand() * 1.0
                    rightPowerGene[i][1][j] = rand() * 3.0 + 4.0



"""キー入力"""
def keyboard(key, x, y):

    if key == "\033": # ESC
        glutDestroyWindow(window)
        sys.exit()

    if key == GLUT_KEY_UP:
        wglSwapIntervalEXT(0);


""" モーション関連 """
# ボール射出関数
# どのボールを(no)どの方向へどれくらいの速度で投げるか(vx, vy, vz)
def throwball(no, vx, vy, vz):

    ballVelocity[no][0] = vx
    ballVelocity[no][1] = vy
    ballVelocity[no][2] = vz

# 評価パラメータのリセット
def humanInit():
    global frame
    global lAngle, rAngle
    global lHandBall, rHandBall
    global ballPosition, ballVelocity, ballRelease
    global prevIsLeft

    frame = 0    # 経過フレーム

    lAngle = 90.0 # 左肘関節x方向の角度
    rAngle = 0.0 # 右肘関節y方向の角度

    rHandPosition = [0.0, 0.0, 0.0] # 右手の位置
    lHandPosition = [0.0, 0.0, 0.0] # 左手の位置
    rHandBall = -1 #右手が持っているボールの番号
    lHandBall = -1 #左手が持っているボールの番号

    # ボールの座標 (x,y,z)
    ballPosition = [[0.3, 0.95, 0.4],
                    [-0.3, 2.0, 0.4],
                    [-0.3, 0.95, 0.4]]

    # 0でないならキャッチされない
    ballRelease = [0, 0, 0]

    # 交互にキャッチするためのフラグ
    prevIsLeft = [0, 1, 1]

    # ボールの速度
    ballVelocity = [[0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0]]


""" メイン呼び出し """
if __name__ == "__main__":
    main()
