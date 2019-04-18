class Parser(object):
    def __init__(self, fileDir):
        lines = list()
        with open(fileDir) as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        self.numOfSets = lines[0]




if __name__ == "__main__":
    Parser("../tests/test1.in")