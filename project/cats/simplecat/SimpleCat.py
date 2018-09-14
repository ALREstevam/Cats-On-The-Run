from cats.CatFather import CatFather, Solution
from collections import deque

class SimpleCat(CatFather):

    def __init__(self, start_cell : 'Cell.Cell', objective_cell : 'Cell.Cell' , grid):
        super().__init__(start_cell, objective_cell, grid)
        self.open_set = list()
        self.reset()

    def reset(self):
        super().reset()

    def find_path(self):

        current = self.start


        while len(self.open_set) > 0 :
            d0 = ''
            d1 = ''
            dcmb = ''

            if self.start.xpos < current.xpos:d0 = 'N'
            elif self.start.xpos > current.xpos:d0 = 'S'
            if self.start.ypos > current.ypos:d1 = 'E'
            elif self.start.ypos < current.ypos:d1 = 'W'
            dcmb = d0 + d1

            # direção para a qual quero ir
            # Se preciso ir para NW, posso considerar ir para NW, N, W, (mas N não é válido, ficando [NW, W])
            directions = [elem for elem in [dcmb, d1, d0] if elem not in ['', 'N', 'S']]
            #directions.extend([elem for elem in ["NW", "NE", "W", "E", "SW", "SE"] if elem not in directions])

            #Adicionando os vizinhos do nó atual (se chegar em um local em que não posso me mover vou ter que ir para um deles)
            for neighbor in [elem for elem in current.neighbors if not elem.is_wall and elem not in self.open_set and elem not in self.closed_set]:

                self.open_set.append(neighbor)

            position_changed = False
            for direction in directions:
                if self.position_is_valid(direction): # se a posição é válida, vou pra ela
                    position_changed = True
                    next_node = self.grid.get_cell(direction)
                    self.open_set.remove(current)
                    self.closed_set.add(current)
                    next_node.previous = current
                    break

            if not position_changed:
                self.open_set.remove(current)
                self.closed_set.add(current)
                next_node = self.open_set.pop()
                next_node.previous = current
        self.fill_path(current, True)

    def calc_movement(self, direction, cat):
        return{
            "NW":   [(cat[0] - 1, cat[1] - 1),  (cat[0] - 1, cat[1]) ]      [cat[0] % 2],
            "NE":   [(cat[0] - 1, cat[1]),      (cat[0] - 1, cat[1] + 1)]   [cat[0] % 2],
            "W" :    [(cat[0], cat[1] - 1),     (cat[0], cat[1] - 1)]       [cat[0] % 2],
            "E" :    [(cat[0], cat[1] + 1),     (cat[0], cat[1] + 1)]       [cat[0] % 2],
            "SW":   [(cat[0] + 1, cat[1] - 1),  (cat[0] + 1, cat[1])]       [cat[0] % 2],
            "SE":   [(cat[0] + 1, cat[1]),      (cat[0] + 1, cat[1] + 1)]   [cat[0] % 2],
        }[direction]


    def position_is_valid(self, position):
        return position[0] >= 0 and \
               position[1] >= 0 and \
               position[0] < self.grid.rows and \
               position[1] < self.grid.cols and \
               not self.grid.get_cell(position).is_wall




