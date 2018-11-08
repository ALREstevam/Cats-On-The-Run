from cats.catshelper.Path import Path
from enum import Enum


class Solution(Enum):
    CONTINUE = 'continue'
    NO_SOLUTION = 'no_solution'
    FINDED = 'finded'


class CatFather:
    def __init__(self, grid):
        self.x      =  None
        self.y      =  None
        self.end    =  None
        self.start  =  None
        self.start_cell_pos = None
        self.goal_cell_pos = None

        self.disallowed_cells = set()

        self.open_set = set()
        self.closed_set = set()

        self.path = None
        self.grid = grid

    def set_cells(self, start_cell, objective_cell):

        self.start_cell_pos = start_cell
        self.goal_cell_pos = objective_cell

        self.start = self.grid.get_cell(start_cell)
        self.end = self.grid.get_cell(objective_cell)

        self.x      = start_cell[0]
        self.y      = start_cell[1]

        self.disallowed_cells = [cell for cell in self.grid.goals if cell != objective_cell and cell != start_cell]



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
        del self.path
        self.path = None
        self.grid.reset_previous()

    def find_path(self, start_cell, end_cell) -> Solution:
        pass


    def __str__(self):
        return str(self.__class__.__name__)

    def __repr__(self):
        return str(self.__class__.__name__)

