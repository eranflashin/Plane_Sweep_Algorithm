from Parser import Parser
from LineSweep import LineSweep
import os

if __name__ == "__main__":

    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".in"):
            testCases = Parser(filename).getResult()

            actual = ""
            expected = open("test{0}.out".format(filename.split("test")[1].split(".")[0])).read()

            for (_, segmentSet) in testCases.items():
                result = LineSweep(segmentSet).run().getResult()
                actual += "{0}\n".format(result)

            if actual == expected:
                print("{0} passed!".format(filename))
            else:
                print("{0} failed!".format(filename))

        else:
            continue
