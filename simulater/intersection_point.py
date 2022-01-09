# https://www.hiramine.com/programming/graphics/2d_segmentintersection.html

# 線分ABと線分CDの交点を求める関数


def calculateIntersectionPoint(pointA, pointB, pointC, pointD):
    intersectionPoint = [0, 0]
    bunbo = (pointB[0] - pointA[0]) * (pointD[1] - pointC[1]) - \
        (pointB[1] - pointA[1]) * (pointD[0] - pointC[0])

    # 2つの線分が平行の時実行
    if bunbo == 0:
        return False, intersectionPoint

    ac = ((pointC[0] - pointA[0]), (pointC[1] - pointA[1]))
    r = ((pointD[1] - pointC[1]) * ac[0] -
         (pointD[0] - pointC[0]) * ac[1]) / bunbo
    s = ((pointB[1] - pointA[1]) * ac[0] -
         (pointB[0] - pointA[0]) * ac[1]) / bunbo

    if r < 0 or r > 1 or s < 0 or s > 1:
        return False, intersectionPoint

    # rを使った計算の場合
    distance = ((pointB[0] - pointA[0]) * r, (pointB[1] - pointA[1]) * r)
    intersectionPoint = [pointA[0] + distance[0], pointA[1] + distance[1]]

    return True, intersectionPoint


if __name__ == '__main__':
    # 交点があるとき
    print(calculateIntersectionPoint([0, 0], [10, 10], [0, 10], [10, 0]))
    # 交点がないとき
    print(calculateIntersectionPoint([0, 0], [10, 10], [0, 10], [2, 8]))
    # 線分が平行であるとき
    print(calculateIntersectionPoint([0, 0], [10, 10], [0, 5], [10, 15]))
