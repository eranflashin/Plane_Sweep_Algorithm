import heapq
from bintrees.avltree import AVLTree
from GeometricAux import *
from Parser import Parser


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

    def adjSeg(self, seg):
        rank = seg.compareRank()
        try:
            (_, nextSeg) = self.container.succ_item(rank)
        except KeyError:
            nextSeg = None
        try:
            (_, prevSeg) = self.container.prev_item(rank)
        except KeyError:
            prevSeg = None
        return nextSeg, prevSeg

    def adjIntersections(self, seg):
        nextSeg, prevSeg = self.adjSeg(seg)

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
        self.foundIntersections = AVLTree()

    def processAdjIntersections(self, seg):
        ((intersectionPrev, prevSeg), (intersectionNext, nextSeg)) = self.lineStatus.adjIntersections(seg)
        if intersectionPrev is not None and self.foundIntersections.get(intersectionPrev) != 0:
            self.eventsQueue.pushIntersectionEvent(intersectionPrev, prevSeg, seg)
            self.foundIntersections.insert(intersectionPrev, 0)
        if intersectionNext is not None and self.foundIntersections.get(intersectionNext) != 0:
            self.eventsQueue.pushIntersectionEvent(intersectionNext, seg, nextSeg)
            self.foundIntersections.insert(intersectionNext, 0)


    def run(self):
        while not self.eventsQueue.isEmpty():
            (point, eventType, segList) = self.eventsQueue.popEvent().getData()
            if eventType == EventType.START_POINT:
                [seg] = segList
                self.lineStatus.insert(seg)
                self.processAdjIntersections(seg)

            elif eventType == EventType.END_POINT:
                [seg] = segList
                nextSeg, prevSeg = self.lineStatus.adjSeg(seg)
                self.lineStatus.remove(seg)
                if nextSeg is not None and prevSeg is not None:
                    intersection = nextSeg.intersectsWith(prevSeg)
                    if intersection is not None and self.foundIntersections.get(intersection) != 0:
                        self.eventsQueue.pushIntersectionEvent(intersection, nextSeg, prevSeg)  # check
                        self.foundIntersections.insert(intersection, 0)

            elif eventType == EventType.INTERSECTION:
                self.numOfIntersections += 1
                [upperSeg, lowerSeg] = segList
                self.lineStatus.remove(upperSeg)
                self.lineStatus.remove(lowerSeg)
                upperSeg.setLastVisitedPoint(point)
                lowerSeg.setLastVisitedPoint(point)
                self.lineStatus.insert(upperSeg)
                self.lineStatus.insert(lowerSeg)

                self.processAdjIntersections(upperSeg)
                self.processAdjIntersections(lowerSeg)

        return self

    def getResult(self):
        return self.numOfIntersections
