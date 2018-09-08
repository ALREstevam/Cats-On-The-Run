from collections import deque
from random import shuffle, sample
from cats.CatFather import CatFather, Solution

class BreadthFirstSearchCat(CatFather):

    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell' , grid):
        super().__init__(start_cell, objective_cell, grid)
        print('STARTING')
        self.reset()


    def reset(self):
        print('RESETING')
        super().reset()
        self.open_set = deque([self.start])

    def find_path(self):
        while len(self.open_set) > 0:
            current = self.open_set.popleft()
            #Se o nó atual for o destino
            if current is self.end:
                self.fill_path(current, True)
                return Solution.FINDED

            #Se o nó corrente for uma parede ou já tiver sido explorado
            #if current.is_wall or current in self.closed_set:
            #    continue

            neighbors = [elem for elem in
                         list(current.neighbors.keys())
                         if not elem.is_wall
                            and
                         elem not in self.closed_set
                         ]

            for neighbor in neighbors:
                neighbor.previous = current

            self.closed_set.add(current)

            if neighbors is not None:
                self.open_set.extend( neighbors )
            self.fill_path(current, True)
        return Solution.NO_SOLUTION



