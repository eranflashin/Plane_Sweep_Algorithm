class Parser(object):
    def __init__(self,fileDir):
        self.segm

        with open(fileDir) as file:
            self.numOfSets = int(file.readline().strip(' '))
            for _ in range(self.numOfSets):
                numOfSeg=int(file.readline().strip(' '))
                for _ in range(numOfSeg):
                    points=[float(num) for num in file.readline().split(' ')]
                    self.


if __name__ == "__main__":
    Parser("tests/test1.in")
