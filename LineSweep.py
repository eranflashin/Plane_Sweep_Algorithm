import heapq
from bintrees.avltree import AVLTree
from GeometricAux import *


class EventType(Enum):
    START_POINT = 0
    INTERSECTION = 1
    END_POINT = 2


class EventQueueItem(object):
    def __init__(self, point, pointType, segList):
        self.point = point
        self.pointType = pointType
        self.segList = segList

    def __lt__(self, other):
        return self.point.x < other.point.x

    def getData(self):
        return self.point, self.pointType, self.segList


class EventQueue(object):
    def __init__(self, segmentsSet):
        self.heap = [EventQueueItem(seg.getStartPoint(), EventType.START_POINT, [seg]) for seg in
                     segmentsSet] + [EventQueueItem(seg.getEndPoint(), EventType.END_POINT, [seg]) for seg in
                                     segmentsSet]
        heapq.heapify(self.heap)

    def popEvent(self):
        return heapq.heappop(self.heap)

    def isEmpty(self):
        return len(self.heap) == 0

    def pushIntersectionEvent(self, point, upperSeg, lowerSeg):
        heapq.heappush(self.heap, EventQueueItem(point, EventType.INTERSECTION, [upperSeg, lowerSeg]))


class LineStatus(object):
    def __init__(self):
        self.container = AVLTree()

    def insert(self, seg):
        self.container.insert(seg.compareRank(), seg)

    def remove(self, seg):
        self.container.remove(seg.compareRank())

    def adjIntersections(self, seg):
        rank = seg.compareRank()
        try:
            (_, nextSeg) = self.container.succ_item(rank)
        except KeyError:
            nextSeg = None

        try:
            (_, prevSeg) = self.container.prev_item(rank)
        except KeyError:
            prevSeg = None

        if nextSeg is not None:
            interNext = seg.intersectsWith(nextSeg)
        else:
            interNext = None

        if prevSeg is not None:
            interPrev = seg.intersectsWith(prevSeg)
        else:
            interPrev = None

        return (interPrev, prevSeg), (interNext, nextSeg)


class LineSweep(object):
    def __init__(self, segmentsSet):
        self.eventsQueue = EventQueue(segmentsSet)
        self.lineStatus = LineStatus()
        self.numOfIntersections = 0

    def run(self):
        while not self.eventsQueue.isEmpty():
            (point, eventType, segList) = self.eventsQueue.popEvent().getData()
            if eventType == EventType.START_POINT:
                [seg] = segList
                self.lineStatus.insert(seg)
                ((intersectionPrev, prevSeg), (intersectionNext, nextSeg)) = self.lineStatus.adjIntersections(seg)

                if intersectionPrev is not None:
                    self.eventsQueue.pushIntersectionEvent(intersectionPrev, prevSeg, seg)

                if intersectionNext is not None:
                    self.eventsQueue.pushIntersectionEvent(intersectionNext, seg, nextSeg)

            elif eventType == EventType.END_POINT:
                [seg] = segList
                self.lineStatus.remove(seg)
            elif eventType == EventType.INTERSECTION:
                self.numOfIntersections += 1
                [upperSeg, lowerSeg] = segList
                self.lineStatus.remove(upperSeg)
                self.lineStatus.remove(lowerSeg)
                upperSeg.setLastVisitedPoint(point)
                lowerSeg.setLastVisitedPoint(point)
                self.lineStatus.insert(upperSeg)
                self.lineStatus.insert(lowerSeg)

                ((intersectionPrev, prevSeg), (intersectionNext, nextSeg)) = self.lineStatus.adjIntersections(upperSeg)

                if intersectionPrev is not None and point < intersectionPrev:
                    self.eventsQueue.pushIntersectionEvent(intersectionPrev, prevSeg, upperSeg)

                if intersectionNext is not None and point < intersectionNext:
                    self.eventsQueue.pushIntersectionEvent(intersectionNext, upperSeg, nextSeg)

                ((intersectionPrev, prevSeg), (intersectionNext, nextSeg)) = self.lineStatus.adjIntersections(lowerSeg)

                if intersectionPrev is not None and point < intersectionPrev:
                    self.eventsQueue.pushIntersectionEvent(intersectionPrev, prevSeg, lowerSeg)

                if intersectionNext is not None and point < intersectionNext:
                    self.eventsQueue.pushIntersectionEvent(intersectionNext, lowerSeg, nextSeg)

                    # not good need to check explicitly if already in heap


if __name__ == "__main__":
    s1 = Segment(Point(1, 1), Point(4, 4))
    s2 = Segment(Point(2, 2), Point(3, 1.5))

    LineSweep({s1, s2}).run()

# if eventType == EventType.START_POINT:
#     seg = seg[0]
#     self.lineStatus.insert((seg.getStartPoint().getY(), seg), seg)
#
#     try:
#         (_, nextSeg) = self.lineStatus.succ_item((seg.getStartPoint().getY(), seg))
#     except:
#         nextSeg = None
#
#     try:
#         (_, prevSeg) = self.lineStatus.prev_item((seg.getStartPoint().getY(), seg))
#     except:
#         prevSeg = None
#
#     if nextSeg is not None:
#         inter = seg.intersectsWith(nextSeg)
#         if inter is not None:
#             heapq.heappush(self.eventsQueue, (inter, [seg, nextSeg], EventType.INTERSECTION))
#
#     if prevSeg is not None:
#         inter = seg.intersectsWith(prevSeg)
#         if inter is not None:
#             heapq.heappush(self.eventsQueue, (inter, [seg, prevSeg], EventType.INTERSECTION))
#
# elif eventType == EventType.END_POINT:
#     seg = seg[0]
#
#     try:
#         (_, nextSeg) = self.lineStatus.succ_item((seg.getStartPoint().getY(), seg))
#     except:
#         nextSeg = None
#
#     try:
#         (_, prevSeg) = self.lineStatus.prev_item((seg.getStartPoint().getY(), seg))
#     except:
#         prevSeg = None
#
#     if nextSeg is not None:
#         inter = seg.intersectsWith(nextSeg)
#         if inter is not None:
#             heapq.heappush(self.eventsQueue, (inter, [seg, nextSeg], EventType.INTERSECTION))
#
#     if prevSeg is not None:
#         inter = seg.intersectsWith(prevSeg)
#         if inter is not None:
#             heapq.heappush(self.eventsQueue, (inter, [seg, prevSeg], EventType.INTERSECTION))
#
#     self.lineStatus.remove((seg.getStartPoint().getY(), seg))
#
# elif eventType == EventType.INTERSECTION:
#     self.numOfIntersections += 1
