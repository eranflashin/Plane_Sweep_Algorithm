import heapq
from GeometricAux import *
from AVL import AVL

class EventType(Enum):
    START_POINT = 0
    INTERSECTION = 1
    END_POINT = 2

    def __le__(self, other):
        return self.value <= other.value


class EventQueueItem(object):
    def __init__(self, point, pointType, segList):
        self.point = point
        self.pointType = pointType
        self.segList = segList

    def __lt__(self, other):
        if self.point.x < other.point.x:
            return True
        elif self.point.x == other.point.x:
            return self.pointType <= other.pointType
        else:
            return False

    def getData(self):
        return self.point, self.pointType, self.segList


class EventQueue(object):
    def __init__(self, segmentsSet):
        self.heap = [EventQueueItem(seg.startPoint, EventType.START_POINT, [seg]) for seg in
                     segmentsSet] + [EventQueueItem(seg.endPoint, EventType.END_POINT, [seg]) for seg in
                                     segmentsSet]
        heapq.heapify(self.heap)

    def popEvent(self):
        return heapq.heappop(self.heap)

    def isEmpty(self):
        return len(self.heap) == 0

    def pushIntersectionEvent(self, point, upperSeg, lowerSeg):
        heapq.heappush(self.heap, EventQueueItem(point, EventType.INTERSECTION, [lowerSeg, upperSeg]))


class LineStatus(object):
    def __init__(self):
        self.container = AVL()

    def insert(self, seg):
        self.container.insert(seg)

    def remove(self, seg):
        self.container.delete(seg)

    def adjSeg(self, seg):

        nextSeg = self.container.next_larger(seg)

        prevSeg = self.container.prev_smaller(seg)

        if nextSeg is not None:
            nextSeg = nextSeg.key

        if prevSeg is not None:
            prevSeg = prevSeg.key

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
        self.foundIntersections = AVL()

    def processAdjIntersections(self, seg):
        ((intersectionPrev, prevSeg), (intersectionNext, nextSeg)) = self.lineStatus.adjIntersections(seg)
        if intersectionPrev is not None and self.foundIntersections.find(intersectionPrev) is None:
            self.eventsQueue.pushIntersectionEvent(intersectionPrev, lowerSeg=prevSeg, upperSeg=seg)
            self.foundIntersections.insert(intersectionPrev)
        if intersectionNext is not None and self.foundIntersections.find(intersectionNext) is None:
            self.eventsQueue.pushIntersectionEvent(intersectionNext, upperSeg=seg, lowerSeg=nextSeg)
            self.foundIntersections.insert(intersectionNext)

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
                    if intersection is not None and self.foundIntersections.find(intersection) is None:
                        self.eventsQueue.pushIntersectionEvent(intersection, nextSeg, prevSeg)
                        self.foundIntersections.insert(intersection)

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
