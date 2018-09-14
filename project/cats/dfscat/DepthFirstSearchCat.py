from collections import deque
from random import shuffle, sample
from cats.CatFather import CatFather, Solution

class DepthFirstSearchCat(CatFather):

    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell' , grid):
        super().__init__(start_cell, objective_cell, grid)
        self.reset()


    def reset(self):
        super().reset()
        self.open_set = deque([self.start])

    def find_path(self):
        while len(self.open_set) > 0:
            current = self.open_set.pop()

            if current is self.end:
                self.fill_path(current, True)
                return Solution.FINDED

            all_neighbors = list(current.neighbors.keys())

            valid_neighbors = [elem for elem in all_neighbors if not elem.is_wall and elem not in self.closed_set and elem not in self.open_set]

            self.closed_set.add(current)


            for neighbor in valid_neighbors:
                neighbor.previous = current

            if valid_neighbors is not None:
                self.open_set.extend( valid_neighbors )
            self.fill_path(current, True)
        return Solution.NO_SOLUTION

#1  procedure DFS-iterative(G,v):
#2      let S be a stack
#3      S.push(v)
#4      while S is not empty
#5          v = S.pop()
#6          if v is not labeled as discovered:
#7              label v as discovered
#8              for all edges from v to w in G.adjacentEdges(v) do
#9                  S.push(w)

