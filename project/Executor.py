from cats.CatFather import CatFather
from Grid import Grid
from cats.catshelper.DistanceCalculator import DistanceTypes, Distance2DCalculator
from operator import attrgetter

class Pathfind:
    def __init__(self, cats : [CatFather], grid : Grid, minimum, stop_if_minimum = False):
        self.cats = cats
        self.grid = grid
        self.minimum = minimum
        self.stop_if_minimum = stop_if_minimum

        # cat     = [5, 5]
        # blocks  = [ (1,1), (1,5), (2,5), (4,5), (5,1), (5, 4), (6, 5), (8, 2) ]
        # exits   = [ (0,0), (6, 10), (9, 10), (10, 1) ]
        # minimum = 5

        self.start_cell = grid.get_start_cell()
        self.exit_cells = grid.get_exit_cells()
        self.exit_cells = sorted(self.exit_cells, key=lambda x : Distance2DCalculator(DistanceTypes.HEX).distCell(self.start_cell, x),
                            reverse=False)

    def executePrinting(self):
        for cat in self.cats:
            print('-' * 100)
            print('CAT: {}'.format(cat))
            print('MINIMUM PATH SIZE: {}'.format(self.minimum))

            dirs=[]
            exit_counter = 0

            for exit_cell in self.exit_cells:
                cat.end = exit_cell
                cat.reset()
                cat.find_path()
                dirs.append(cat.path)

                print('PATH SIZE: {}'.format(cat.path.distance))
                print(self.grid.show(cat))
                print('DIRECTIONS')
                print(cat.path.get_directions_str().replace('\n', ' '))
                exit_counter += 1
            print('-')
            print(min(dirs, key=attrgetter('distance')).get_directions_str())
            print('-')


