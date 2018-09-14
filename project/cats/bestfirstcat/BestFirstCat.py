from collections import deque
from random import shuffle, sample
from cats.CatFather import CatFather, Solution
from cats.catshelper.DistanceCalculator import DistanceTypes, Distance2DCalculator

class BestFirstSearchCat(CatFather):

    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell',  grid, distance_type: DistanceTypes):
        super().__init__(start_cell, objective_cell, grid)
        self.distance_calcutator = Distance2DCalculator(distance_type)
        self.reset()

    def reset(self):
        super().reset()
        self.start.vars['h'] = self.heuristic(self.start)
        self.open_set = deque([self.start])

    def find_path(self):
        while len(self.open_set) > 0:

            current = min(self.open_set, key = lambda elem : elem.vars['h'])

            self.open_set.remove(current)
            #current = self.open_set.popleft()

            if current is self.end:
                self.fill_path(current, True)
                return Solution.FINDED

            neighbors = [elem for elem in
                         list(current.neighbors.keys())
                         if not elem.is_wall
                            and
                         elem not in self.closed_set
                            and
                         elem not in self.open_set
                         ]

            for neighbor in neighbors:
                neighbor.previous = current
                neighbor.vars['h'] = self.heuristic(neighbor)

            self.closed_set.add(current)

            if neighbors is not None:
                self.open_set.extendleft( neighbors )
            self.fill_path(current, True)

        return Solution.NO_SOLUTION


    def heuristic(self, cell : 'Cell.Cell'):
        return self.distance_calcutator.distCell(cell, self.end)





