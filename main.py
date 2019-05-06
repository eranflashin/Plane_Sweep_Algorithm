from Parser import Parser
from LineSweep import LineSweep


if __name__ == "__main__":

    file = "./tests/test1.in"

    testCases = Parser(file).getResult()
    for (_, segmentSet) in testCases.items():
        result = LineSweep(segmentSet).run().getResult()
        print("{0}".format(result))
