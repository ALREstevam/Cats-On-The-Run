import importlib
import sys
from Grid import Grid
from cats.astarcat2.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat

from cats.catshelper.DistanceCalculator import DistanceTypes
from Executor import Pathfind

#filename = sys.argv[1]
filename = 'conf01'
mod = importlib.import_module(filename)



grid = Grid(mod.exits, mod.blocks, mod.cat, rows=11, cols=11)
print(grid.show())

cat1 = AstarCat(
    start_cell=grid.get_start_cell(),
    objective_cell=grid.get_exit_cells()[0],
    max_iterations=200,
    grid=grid,
    gWeight=1,
    hWeight=1,
    fWeight=1,
    distanceType=DistanceTypes.HEX
)


cat2 = BreadthFirstSearchCat(
    start_cell=grid.get_start_cell(),
    objective_cell=grid.get_exit_cells()[0],
    grid=grid,
)

cat3 = BestFirstSearchCat(
    start_cell=grid.get_start_cell(),
    objective_cell=grid.get_exit_cells()[0],
    grid=grid,
    distance_type=DistanceTypes.HEX
)

Pathfind(cat3, grid, mod.minimum)



