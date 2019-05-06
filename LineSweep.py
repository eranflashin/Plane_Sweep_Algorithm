import heapq
from GeometricAux import *
from Avl.AVL import AVL


class EventType(Enum):
    START_POINT = 0
    INTERSECTION = 1
    END_POINT = 2

    def __le__(self, other):
        """
            defines priority among the event types: Intersection is weaker than start but stronger than
            ending
        """
        return self.value <= other.value


class EventQueueItem(object):
    """
        This class wraps the point with its type and the segment it belongs to
    """

    def __init__(self, point, pointType, segList):
        self.point = point
        self.pointType = pointType
        self.segList = segList

    def __lt__(self, other):
        """
            Definition of < between the event queue items:
            firstly by x, if same x then by type
        """
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
        """
            Given the set of segments, initialize the event queue by inserting two end-points
            per segment
        """
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
    """
        This class represents a sweep line status : AVL tree containing all currently
        intersecting segments
    """

    def __init__(self):
        self.container = AVL()

    def insert(self, seg):
        self.container.insert(seg)

    def remove(self, seg):
        self.container.delete(seg)

    def adjSeg(self, seg):
        """
            given a segment in the self line status, returns both the adjacent segments
        """
        nextSeg = self.container.next_larger(seg)

        prevSeg = self.container.prev_smaller(seg)

        if nextSeg is not None:
            nextSeg = nextSeg.key

        if prevSeg is not None:
            prevSeg = prevSeg.key

        return nextSeg, prevSeg

    def adjIntersections(self, seg):
        """
            Given a segment in self line status, returns the intersections of the segments with
            its adjacent segments (if exist, otherwise None)
        """
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
        """
            given a segment in the line status, inserts into event queue the intersection points of the
            segment with the adjacent segments (if exist)
        """
        ((intersectionPrev, prevSeg), (intersectionNext, nextSeg)) = self.lineStatus.adjIntersections(seg)
        if intersectionPrev is not None and self.foundIntersections.find(intersectionPrev) is None:
            self.eventsQueue.pushIntersectionEvent(intersectionPrev, lowerSeg=prevSeg, upperSeg=seg)
            self.foundIntersections.insert(intersectionPrev)
        if intersectionNext is not None and self.foundIntersections.find(intersectionNext) is None:
            self.eventsQueue.pushIntersectionEvent(intersectionNext, upperSeg=seg, lowerSeg=nextSeg)
            self.foundIntersections.insert(intersectionNext)

    def run(self):
        """
            This method runs the whole algorithm

        """
        while not self.eventsQueue.isEmpty():
            (point, eventType, segList) = self.eventsQueue.popEvent().getData()  # get the next eventQ item

            if eventType == EventType.START_POINT:
                [seg] = segList  # it is a start point so only one segment is relevant
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
                [upperSeg, lowerSeg] = segList  # it is an intersection point so two segments are relevant

                # swap the segments in the line status by removing them, updating their last visited point
                # and inserting them back
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
