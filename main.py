from Parser import Parser
from LineSweep import LineSweep

if __name__ == "__main__":
    testCases = Parser("./tests/test1.in").getResult()
    for (_, segmentSet) in testCases.items():
        result = LineSweep(segmentSet).run().getResult()
        print("{0}".format(result))
