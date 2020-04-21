import math


def angle_tank(p):
    """
    :param p: polygon from map
    :param coords: coordination of tank bottom
    :return: angle
    """

    """
    if p is None:
        p = [(0, 2), (2, 0)]
    b_a = (p[0][0] - p[1][0], p[1][0] - p[1][1])
    b_c = (-p[1][0], -p[1][1])
    tetha = math.acos((b_a[0] * b_c[0] + b_a[1] * b_c[1]) /
                      (math.sqrt(b_a[0] * b_a[0] + b_a[1] * b_a[1]) * math.sqrt(b_c[0] * b_c[0] + b_c[1] * b_c[1])))
    tetha = math.degrees(tetha)

    if p[0][0] < p[1][0]:
        tetha += 270
    else:
        tetha += 0
    """
    angles = []

    for i in range(len(p)-1):
        b_a = (p[i][0] - p[i+1][0], p[i+1][0] - p[i+1][1])
        b_c = (-p[i+1][0], -p[i+1][1])
        tetha = int(math.degrees(math.acos((b_a[0] * b_c[0] + b_a[1] * b_c[1]) /
                      (math.sqrt(b_a[0] * b_a[0] + b_a[1] * b_a[1]) *
                       math.sqrt(b_c[0] * b_c[0] + b_c[1] * b_c[1])))))

        if p[i][i] < p[i+1][i]:
            tetha += 270

        angles.append(tetha)




angle_tank([(0, 2), (2, 0), (0, -2)])
