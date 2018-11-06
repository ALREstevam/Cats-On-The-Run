from grid.Cell import Cell

class Path:
    def __init__(self, begin_cell : Cell, reversed_direction = False):
        pass
        self.instructions = []
        self.path = []
        self.is_reversed = reversed_direction
        self.begin = begin_cell


    def get_first_direction(self):
        pass


    def _make_path(self):
        temp = self.begin
        self.path.append(temp)
        while temp.previous is not None:
            self.path.append(temp.previous)
            temp = temp.previous

    def _make_instructions(self):
        if len(self.path) == 0:
            self._make_path()

        for info in self.path:
            self.add_node(info, self.is_reversed)

    def get_distance(self):
        if len(self.path) == 0:
            self._make_path()
        return len(self.path)

    def get_positions(self):
        if len(self.instructions) == 0:
            self._make_instructions()

        return list(map(lambda instruction: instruction[0], self.instructions))

    def get_directions(self):
        if len(self.instructions) == 0:
            self._make_instructions()

        return list(map(lambda instruction : instruction[1], self.instructions))[1:]

    def get_directions_str(self):
        if len(self.instructions) == 0:
            self._make_instructions()

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
        if len(self.instructions) == 0:
            self._make_instructions()
        return str(self.instructions)