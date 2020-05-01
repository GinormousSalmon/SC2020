import pandas as pd
from io import StringIO
from os import walk
from datetime import datetime


def float(data):
    return float(data.replace(',', '.'))


class Data:
    def __init__(self):
        self.data = []
        self.str_data = ""

    @staticmethod
    def read_from_dir(direct):
        directs = []
        for (_, _, filenames) in walk(direct):
            for file in filenames:
                directs.append(direct + "\\" + file)
        return directs

    @staticmethod
    def lines_read(file, skip=2):
        with open(file) as txt:
            lines = txt.readlines()[skip:]
            txt.close()
        return lines

    def str_read(self, lines, float_replace=False):
        if float_replace:
            for i, word in enumerate(lines):
                if ',' in word:
                    lines[i] = word.replace(',', '.')
        self.str_data += "".join(lines)

    def read(self, cols, index=None, sort_index=None, sep="\s+"):
        if index is None:
            index = []
        self.data = pd.read_csv(StringIO(self.str_data), sep=sep, index_col=index, names=cols)
        if not sort_index is None:
            self.data = self.data.sort_values(sort_index)
