import math
from enum import Enum


class Sign(Enum):
    POSITIVE = 1
    ZERO = 0
    NEGATIVE = -1

    @staticmethod
    def getSign(x):
        if x < 0:
            return Sign.NEGATIVE
        elif x == 0:
            return Sign.ZERO
        else:
            return Sign.POSITIVE


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def orientation(point1, point2, point3) -> Sign:
        det = point1.getX() * (point2.getY() - point3.getY()) - point1.getY() * (point2.getX() - point3.getX()) + \
              (point2.getX() * point3.getY() - point2.getY() * point3.getX())
        return Sign.getSign(det)

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)


class Segment(object):
    def __init__(self, point1, point2):
        if point1 < point2:
            self.startPoint = point1
            self.endPoint = point2
        else:
            self.startPoint = point2
            self.endPoint = point1

        self.lastVisitedPoint = self.startPoint

    def getStartPoint(self):
        return self.startPoint

    def getEndPoint(self):
        return self.endPoint

    def containsPoint(self, point):
        return self.startPoint.distanceFrom(self.endPoint) == \
               self.startPoint.distanceFrom(point) + point.distanceFrom(self.endPoint)

    def intersectsWith(self, otherSeg):
        orientation1 = Point.orientation(self.startPoint, self.endPoint, otherSeg.startPoint)
        orientation2 = Point.orientation(self.startPoint, self.endPoint, otherSeg.endPoint)
        orientation3 = Point.orientation(otherSeg.startPoint, otherSeg.endPoint, self.startPoint)
        orientation4 = Point.orientation(otherSeg.startPoint, otherSeg.endPoint, self.endPoint)

        if orientation1 != orientation2 and orientation3 != orientation4:
            return Segment.getIntersectionPoint(self, otherSeg)

        if orientation1 == Sign.ZERO and self.containsPoint(otherSeg.startPoint):
            return otherSeg.startPoint

        if orientation2 == Sign.ZERO and self.containsPoint(otherSeg.endPoint):
            return otherSeg.endPoint

        if orientation3 == Sign.ZERO and otherSeg.containsPoint(self.startPoint):
            return self.startPoint

        if orientation4 == Sign.ZERO and otherSeg.containsPoint(self.endPoint):
            return self.endPoint

        return None

    @staticmethod
    def getIntersectionPoint(seg1, seg2):
        p1 = seg1.getStartPoint()
        p2 = seg1.getEndPoint()
        q1 = seg2.getStartPoint()
        q2 = seg2.getEndPoint()
        seg2Param = ((q2.getX() - p2.getX()) - (
                ((q2.getY() - p2.getY()) * (p1.getX() - p2.getX())) / (p1.getY() - p2.getY()))) \
                    / ((((p1.getX() - p2.getX()) * (q1.getY() - q2.getY())) / (p1.getY() - p2.getY())) - (
                q1.getX() - q2.getX()))

        X = q1.getX() * seg2Param + (1 - seg2Param) * q2.getX()
        Y = q1.getY() * seg2Param + (1 - seg2Param) * q2.getY()
        return Point(X, Y)

    def setLastVisitedPoint(self, point):
        self.lastVisitedPoint = point

    def compareRank(self):
        return self.lastVisitedPoint.y + (
                0.01 * ((self.endPoint.y - self.lastVisitedPoint.y) / (self.endPoint.x - self.lastVisitedPoint.x)))

    def __str__(self):
        return "start: {0} end: {1}".format(self.startPoint, self.endPoint)
