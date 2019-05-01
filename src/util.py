import math
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def if_clockwise(y1, x1, y2, x2):
    angle1 = math.pi-math.atan2(y1, x1)
    y = math.sin(angle1)*x2+math.cos(angle1)*y2
    x = math.cos(angle1)*x2-math.sin(angle1)*y2
    angle2 = math.atan2(y, x)*180/math.pi
    if angle2 > 0 and angle2 < 180:
        return True
    else:
        return False

def if_all_clockwise(poly):
    x1, y1, x2, y2, x3, y3, x4, y4 = np.array(poly).flatten()
    x = (x1+x3)/2
    y = (y1+y3)/2
    if if_clockwise(y1-y, x1-x, y2-y, x2-x):
        if if_clockwise(y2-y, x2-x, y3-y, x3-x):
            if if_clockwise(y3-y, x3-x, y4-y, x4-x):
                if if_clockwise(y4-y, x4-x, y1-y, x1-x):
                    x = (x2+x4)/2
                    y = (y2+y4)/2
                    if if_clockwise(y1-y, x1-x, y2-y, x2-x):
                        if if_clockwise(y2-y, x2-x, y3-y, x3-x):
                            if if_clockwise(y3-y, x3-x, y4-y, x4-x):
                                if if_clockwise(y4-y, x4-x, y1-y, x1-x):
                                    return True
    return False

def distance(x1, y1, x2, y2, x3, y3):
    a = y1-y3
    b = x3-x1
    c = -a*x1-b*y1
    return abs(a*x2+b*y2+c)/math.sqrt(a*a+b*b)

def if_not_slim(poly):
    x1, y1, x2, y2, x3, y3, x4, y4 = np.array(poly).flatten()
    d1 = distance(x1, y1, x2, y2, x3, y3)+distance(x1, y1, x4, y4, x3, y3)
    d2 = distance(x2, y2, x3, y3, x4, y4)+distance(x2, y2, x1, y1, x4, y4)
    if d1 > 10*d2 or d2 > 10*d1 or d1 < 3 or d2 < 3:
        return False
    else:
        return True

def valid_poly(poly):
    return if_all_clockwise(poly) and if_not_slim(poly)
