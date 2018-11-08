from grid.Cell import Cell

class Path:
    def __init__(self, begin_cell : Cell, reversed_direction = False):
        self.instructions = []
        self.distance = 0
        self.difficulty = 0

        temp = begin_cell
        if begin_cell is not None:
            self.add_node(begin_cell, reversed_direction)
            self.difficulty = begin_cell.difficulty
        else:
            raise ValueError('Begin cell must not be None')


        if temp.previous is None or temp.previous == temp:
            return


        while temp.previous is not None:
            self.add_node(temp.previous, reversed_direction)
            self.difficulty += temp.difficulty

            #Do not put anything after this!!! (temp will be None at some point)
            temp = temp.previous
        self.distance = len(self.instructions) - 1

    def get_distance(self):
        return self.distance

    def get_positions(self):
        return list(map(lambda instruction: instruction[0], self.instructions))

    def get_directions(self):
        return list(map(lambda instruction : instruction[1], self.instructions))[1:]

    def get_directions_str(self):
        return '\n'.join(self.get_directions())

    def get_difficulty(self):
        return self.difficulty


    def add_node(self, cell:Cell, inReverse):
        direction = None
        if cell.previous is not None:
            if inReverse:
                direction = cell.neighbors[cell.previous].invert()
            else:
                direction = cell.neighbors[cell.previous]

        value = ( (cell.xpos, cell.ypos), str(direction) )

        if inReverse:
            self.instructions = [value] + self.instructions
        else:
            self.instructions.append(value)

    def __str__(self):
        return str(self.instructions)

