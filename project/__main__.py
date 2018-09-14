import importlib
import sys
from Grid import Grid
from cats.astarcat2.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
from cats.dfscat.DepthFirstSearchCat import DepthFirstSearchCat
from cats.simplecat.SimpleCat import SimpleCat
from pprint import pprint

from cats.catshelper.DistanceCalculator import DistanceTypes
from Executor import Pathfind

filename = sys.argv[1]
#filename = 'confs.conf74' #comentar essa linha para ativar a entrada por linha de comando
mod = importlib.import_module(filename)


def create_grid(mod):
    return Grid(mod.exits, mod.blocks, mod.cat, rows=11, cols=11)

def create_astarcat(grid):
    return AstarCat(
        start_cell=grid.get_start_cell(),
        objective_cell=grid.get_exit_cells()[0],
        max_iterations=200,
        grid=grid,
        gWeight=1,
        hWeight=1,
        fWeight=1,
        distanceType=DistanceTypes.HEX
    )


def create_bfs_cat(grid):
   return BreadthFirstSearchCat(
        start_cell=grid.get_start_cell(),
        objective_cell=grid.get_exit_cells()[0],
        grid=grid,
    )

def create_best_first_cat(grid):
    return BestFirstSearchCat(
        start_cell=grid.get_start_cell(),
        objective_cell=grid.get_exit_cells()[0],
        grid=grid,
        distance_type=DistanceTypes.HEX
    )


def create_depth_first_cat(grid):
    return DepthFirstSearchCat(
        start_cell=grid.get_start_cell(),
        objective_cell=grid.get_exit_cells()[0],
        grid=grid,
    )



grid = create_grid(mod)
astar_cat = create_astarcat(grid)
best_first_cat = create_best_first_cat(grid)
bfs_cat = create_bfs_cat(grid)
dfs_cat = create_depth_first_cat(grid)

pathfind = Pathfind([best_first_cat, astar_cat, bfs_cat], grid, mod.minimum)

run_str = pathfind.get_best_run()['path_str']
print(run_str)

def all_to_csv():
    with open('testing.csv', 'w') as file:
        for i in range(1,100):
            filename = 'confs.conf{:02}'.format(i)  # comentar essa linha para ativar a entrada por linha de comando
            mod = importlib.import_module(filename)

            grid = create_grid(mod)
            astar_cat = create_astarcat(grid)
            best_first_cat = create_best_first_cat(grid)
            bfs_cat = create_bfs_cat(grid)
            dfs_cat = create_depth_first_cat(grid)


            line = Pathfind([best_first_cat, astar_cat, bfs_cat, dfs_cat], grid, mod.minimum).compare_cats()
            file.write(line)

