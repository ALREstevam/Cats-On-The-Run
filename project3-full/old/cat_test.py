from random import shuffle
import sys
from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
import math
from cats.catshelper.DistanceCalculator import DistanceTypes
from cats.CatFather import Solution
import operator


cat    = (5,5)
walls = set([(2, 8), (2, 1), (4, 6), (7, 7), (4,7), (6,5)])
goals  = set([(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)])



grid = Grid(goals, walls, cat, rows=11, cols=11)



dist = DistanceTypes.HEX
astar_cat = AstarCat(
    max_iterations=200,
    grid=grid,
    gWeight=1,
    hWeight=1,
    fWeight=1,
    distanceType=dist
)
best_first_cat = BestFirstSearchCat(
    grid=grid,
    distance_type=dist
)
bfs_cat = BreadthFirstSearchCat(
    grid=grid
)

for goal in goals:
    cat_obj = bfs_cat

    cat_obj.reset()  # reseting the cat
    result = cat_obj.find_path(start_cell=cat, end_cell=goal)  # Finding the path to the goal
    print(grid.show(cat_obj))
    print(result)


