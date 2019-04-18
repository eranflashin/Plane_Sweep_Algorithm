import math
from enum import Enum

class Sign(Enum):
    POSITIVE=1
    ZERO=0
    NEGATIVE=-1

    @staticmethod
    def getSign(x):
        if x<0:
            return Sign.NEGATIVE
        elif x==0:
            return Sign.ZERO
        else:
            return Sign.NEGATIVE

def orientation(point1,point2,point3)->Sign:
    det=point1.getX()*(point2.getY()-point3.getY())-point1.getY()*(point2.getX()-point3.getX())+\
        (point2.getX()*point3.getY()-point2.getY()*point3.getX())
    return Sign.getSign(det)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distanceFrom(self, otherPoint):
        return math.hypot(otherPoint.x - self.x, otherPoint.y - self.y)

    def __lt__(self, other):
        return self.x < other.x


class Segment(object):
    def __init__(self, point1, point2):
        if point1 < point2:
            self.startPoint = point1
            self.endPoint = point2
        else:
            self.startPoint = point2
            self.endPoint = point1

    def intersectsWith(self,otherSeg):
