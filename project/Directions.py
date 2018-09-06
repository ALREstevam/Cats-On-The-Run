from enum import Enum

"""
     NW      NE
        \   /
      W - * - E
        /   \ .
      SW     SE
"""

class Directions(Enum):
    W = 1
    E = -1
    NE = 2
    SW = -2
    NW = 3
    SE = -3

    @staticmethod
    def from_str(string : str):
        for item in Directions:
            if string.strip() == item.name:
                return item
        raise ValueError

    def __str__(self):
        return self.name

    def __neg__(self):
        return Directions(self.value * -1)

    def invert(self):
        return Directions(self.value * -1)

    def __iter__(self):
        return (x for x in Directions)

