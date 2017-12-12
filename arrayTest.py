#coding:utf-8
import numpy as np
from numpy.random import *

GENE_NUM = 5

armAngleGene = np.zeros((GENE_NUM, 2, 1))
leftPowerGene = np.zeros((GENE_NUM, 2, 1))
rightPowerGene = np.zeros((GENE_NUM, 2, 1))

# ランダムに遺伝子データを追記する
def appendArmAngle():
    # 最後尾につける遺伝子データを生成

    global armAngleGene
    global leftPowerGene
    global rightPowerGene

    gene = np.zeros((GENE_NUM, 2, 1))

    for i in range(GENE_NUM):
        for j in range(2):
            gene[i][j][0] = np.random.randn()

    print gene

    armAngleGene = np.append(armAngleGene, gene, axis=2)

def geneSelect(values):
    getTwoPear = False
    sumValue = sum(values)

    sum1 = 0
    sum2 = 0
    select1 = 0
    select2 = 0

    while not getTwoPear:
        selectValue1 = rand() * sumValue
        selectValue2 = rand() * sumValue

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



if __name__ == '__main__':



    # appendArmAngle()

    # print armAngleGene

    print range(1, 8)
    print randint(0, 2, 10)

    data = np.zeros((3, 3, 3))

    index = 1

    np.savetxt(("test" + str(index) + ".csv"), data[1], delimiter=",")
