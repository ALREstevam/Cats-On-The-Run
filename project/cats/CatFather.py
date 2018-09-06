from cats.catshelper.Path import Path
from enum import Enum


class Solution(Enum):
    CONTINUE = 'continue'
    NO_SOLUTION = 'no_solution'
    FINDED = 'finded'


class CatFather:
    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell' , grid):
        self.x = start_cell.xpos
        self.y = start_cell.ypos
        self.open_set = set()
        self.closed_set = set()
        self.end = objective_cell
        self.start = start_cell
        self.path = None
        self.grid = grid




    #def fill_path(self, current, from_start = False):
    #    # Preenchendo a lista de nós do caminho
    #    self.path = []
    #    temp = current
    #    self.path.append(temp)
    #
    #    while temp.previous is not None:
    #        self.path.append(temp.previous)
    #        temp = temp.previous
    #    return


    def fill_path(self, current, current_is_end = False):
        #print(self.path)
        self.path = Path(current, current_is_end)
        #print('LEN: {}'.format(self.path.distance))
        #print(self.grid.show(self))

    def reset(self):
        self.open_set = set()
        self.closed_set = set()
        self.path = None
        self.open_set.add(self.start)

    def find_path(self):
        pass


