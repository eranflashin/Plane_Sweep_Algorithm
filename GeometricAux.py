import math
from enum import Enum


def epsilon_eq(x, y, epsilon):
    return abs(x - y) <= epsilon


class Sign(Enum):
    """
        Represents the sign of the triangle orientation computation
    """
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

    def distanceFrom(self, otherPoint):
        return math.hypot(otherPoint.x - self.x, otherPoint.y - self.y)

    def __lt__(self, other):
        """
        :param other:
        :return: true iff self < other. < by x firstly, by y secondly
        """
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return self > other or self == other

    @staticmethod
    def orientation(point1, point2, point3) -> Sign:
        """
            triangle orientation computation as was taught in class
        """
        det = point1.x * (point2.y - point3.y) - point1.y * (point2.x - point3.x) + \
              (point2.x * point3.y - point2.y * point3.x)
        det = round(det, 6)
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

        """
            lastVisitedPoint- the most recently inspected point on the segment
        """
        self.lastVisitedPoint = self.startPoint
        self.slope = round((self.endPoint.y - self.startPoint.y) / (self.endPoint.x - self.startPoint.x), 6)

    def containsPoint(self, point):
        """

        :param point:
        :return: true iff point belongs to Self (segment)
        """
        return self.startPoint.distanceFrom(self.endPoint) == \
               self.startPoint.distanceFrom(point) + point.distanceFrom(self.endPoint)

    def intersectsWith(self, otherSeg):
        """

        :param otherSeg:
        :return: None if seg does not intersect with otherSeg, otherwise the intersection point
        """
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
        """
            Assumption: seg1 intersects with seg2
        """
        p1 = seg1.startPoint
        p2 = seg1.endPoint
        q1 = seg2.startPoint
        q2 = seg2.endPoint

        if seg1.slope == 0:
            Y = p1.y
            Param = (Y - q2.y) / (q1.y - q2.y)
            X = q1.x * Param + (1 - Param) * q2.x
        elif seg2.slope == 0:
            Y = q1.y
            Param = (Y - p2.y) / (p1.y - p2.y)
            X = p1.x * Param + (1 - Param) * p2.x
        else:

            seg2Param = ((q2.x - p2.x) - (
                    ((q2.y - p2.y) * (p1.x - p2.x)) / (p1.y - p2.y))) \
                        / ((((p1.x - p2.x) * (q1.y - q2.y)) / (p1.y - p2.y)) - (
                    q1.x - q2.x))

            X = q1.x * seg2Param + (1 - seg2Param) * q2.x
            Y = q1.y * seg2Param + (1 - seg2Param) * q2.y

        return Point(round(X, 7), round(Y, 7))

    def setLastVisitedPoint(self, point):
        self.lastVisitedPoint = point

    def calcYValueByX(self, x):
        """
            given x, calculates the y value corresponding to the point (x,y) belonging to self segment
            Assumption: x is valid
        """
        if self.slope == 0:
            return self.startPoint.y

        st = self.startPoint
        en = self.endPoint
        return round((en.y * st.x - en.x * st.y - en.y * x + st.y * x) / (st.x - en.x), 7)

    def __lt__(self, other):
        """
            defines a < operator for segments: A is less than B if
            in relation to the sweep line which intersects them both,
            A's y value of intersection with the sweep line is less than that of B
            or in case their intersection points with sweep line overlap then
            A's slope is smaller
        """
        lineSweepPos = max(self.lastVisitedPoint.x, other.lastVisitedPoint.x)

        selfY = self.calcYValueByX(lineSweepPos)
        otherY = other.calcYValueByX(lineSweepPos)

        if epsilon_eq(selfY, otherY, 0.000001):
            return self.slope < other.slope
        return selfY < otherY

    def __str__(self):
        return "start: {0} end: {1}".format(self.startPoint, self.endPoint)
