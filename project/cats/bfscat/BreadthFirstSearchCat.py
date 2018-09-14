from collections import deque
from random import shuffle, sample
from cats.CatFather import CatFather, Solution

class BreadthFirstSearchCat(CatFather):

    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell' , grid):
        super().__init__(start_cell, objective_cell, grid)
        self.reset()


    def reset(self):
        super().reset()
        self.open_set = deque([self.start])

    def find_path(self):
        while len(self.open_set) > 0:
            current = self.open_set.popleft() #Obtém o elemento mais a esquerda da lista e o remove dela

            # é o mesmo que fazer um
            # current = self.open_set[0]
            # self.open_set.remove(current)
            # #ou
            # self.open_set = self.open_set[1:]

            #Se o nó atual for o destino
            if current is self.end:
                self.fill_path(current, True)
                return Solution.FINDED

            #Se o nó corrente for uma parede ou já tiver sido explorado
            #if current.is_wall or current in self.closed_set:
            #    continue

            #Pega todos os vizinhos do nó atual
            all_neighbors = list(current.neighbors.keys())

            # Consideramos os vizinhos que
                # Não são paredes
                # Não foram fechados
                # Não estão na lista serem processados
            valid_neighbors = [elem for elem in all_neighbors if not elem.is_wall and elem not in self.closed_set and elem not in self.open_set]


            for neighbor in valid_neighbors:
                neighbor.previous = current

            self.closed_set.add(current)

            if valid_neighbors is not None:
                self.open_set.extend( valid_neighbors )
            self.fill_path(current, True)
        return Solution.NO_SOLUTION



