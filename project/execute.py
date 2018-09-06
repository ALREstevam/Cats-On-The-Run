from cats.CatFather import CatFather
from Grid import Grid
from cats.catshelper.DistanceCalculator import DistanceTypes, Distance2DCalculator
from operator import attrgetter

class Pathfind:
    def __init__(self, cat : CatFather, grid : Grid, minimum):
        self.cat = cat
        self.grid = grid
        self.minimum = minimum

        # cat     = [5, 5]
        # blocks  = [ (1,1), (1,5), (2,5), (4,5), (5,1), (5, 4), (6, 5), (8, 2) ]
        # exits   = [ (0,0), (6, 10), (9, 10), (10, 1) ]
        # minimum = 5

        start_cell = grid.get_start_cell()

        exit_cells = grid.get_exit_cells()

        print(exit_cells)

        exit_cells = sorted(exit_cells, key=lambda x : Distance2DCalculator(DistanceTypes.HEX).distCell(start_cell, x),
                            reverse=False)

        print(exit_cells)
        dirs=[]
        for exit_cell in exit_cells:
            cat.end = exit_cell
            cat.reset()
            cat.find_path()
            dirs.append(cat.path)

            print(grid.show(cat))
            print('Size: {}'.format(cat.path.distance))

            if cat.path.distance == self.minimum:
                break

        print('-')
        print(min(dirs, key=attrgetter('distance')).get_directions_str())
        print('-')


