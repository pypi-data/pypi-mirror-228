import numpy as np

def points_distance(a, b):
    if a[0] == b[0] and a[1] == b[1]:
        return 0
    #d = np.sqrt(np.einsum("ij,ij->j", a_b, a_b))
    d = np.sqrt(np.sum((a - b) ** 2, axis=0))
    return d

def calculate_a_and_b(p1, p2):
    a = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - (a * p1[0])
    return a, b

def calculate_cross(a1, b1, a2, b2):
    # y = a * x + b
    # a1 * x + b1 = a2 * x + b2
    # a1 * x - a2 * x = b2 - b1
    # x (a1 - a2) = b2 - b1
    # x = (b2 - b1) / (a1 - a2)
    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    return (x, y)

def calculate_ortogonal_a_and_b(a, p):
    # a_o = - ( 1 / a )
    # y = a * x + b
    # b = y - (a * x)
    ao = - ( 1 / a )
    b = p[1] - (ao * p[0])
    return ao, b
