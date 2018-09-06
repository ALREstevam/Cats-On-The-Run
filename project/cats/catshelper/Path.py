from Cell import Cell

class Path:
    def __init__(self, begin_cell : Cell, reversed_direction = False):
        pass
        self.instructions = []
        temp = begin_cell
        self.add_node(begin_cell, reversed_direction)

        while temp.previous is not None:
            self.add_node(temp.previous, reversed_direction)
            temp = temp.previous

        self.distance = len(self.instructions) - 1


    def get_positions(self):
        return list(map(lambda instruction: instruction[0], self.instructions))

    def get_directions(self):
        return list(map(lambda instruction : instruction[1], self.instructions))[1:]

    def get_directions_str(self):
        return '\n'.join(self.get_directions())


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