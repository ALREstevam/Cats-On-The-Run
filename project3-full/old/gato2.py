from PIL import Image, ImageDraw
from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
from pprint import pprint
import math
from cats.catshelper.DistanceCalculator import DistanceTypes
from cats.CatFather import Solution
from cats.catshelper.DistanceCalculator import Distance2DCalculator
import sys



### TODO: DELETE
file = open('log.txt', 'a+')
### DELETE


cat = eval(sys.argv[1])
walls = set(eval(sys.argv[2]))
goals = set(eval(sys.argv[3]))

#cat    = (5,5)
#walls = set([(2, 8), (2, 1), (4, 6), (7, 7), (4,7), (6,5)])
#goals  = set([(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)])


def count(highstack, needles):
    counts = 0
    needles = set(needles)
    for elem in highstack:
        if elem in needles:
            counts += 1
    return counts

def normalize(elem, orig_min, orig_max, reverse=False):
    if reverse:
        orig_min, orig_max = orig_max, orig_min
    divisor = 0.00001
    if not orig_max - orig_min == 0:
        divisor = (orig_max - orig_min)
    return (elem - orig_min)/divisor



grid = Grid(goals, walls, cat, rows=11, cols=11)
grid.assign_difficulty(2)

dist = DistanceTypes.HEX
astar_cat = AstarCat(
    max_iterations=200,
    grid=grid,
    gWeight=1,
    hWeight=1,
    fWeight=1,
    distanceType=dist
)
#best_first_cat = BestFirstSearchCat(grid=grid,distance_type=dist)
#bfs_cat = BreadthFirstSearchCat(grid=grid)


cat_cell = grid.get_cell(cat)
cat_neibs_pos = [neib.pos for neib in cat_cell.neighbors if not neib.is_wall]

## TODO: DELETE
#file.write('CAT NEIBS\n')
#file.write('{}\n'.format(cat_neibs_pos))
#for elem in cat_neibs_pos:
#    file.write('{} is wall: {}\n'.format(elem, elem in walls))


file.write('WALLS\n')
file.write('{}\n'.format(walls))
file.write('FREE GOALS\n')
file.write('{}\n'.format([goal for goal in goals if goal not in walls]))

## DELETE

path_distances = {}
hex_distances = {}

dc = Distance2DCalculator()

for el in cat_neibs_pos:
    for goal in [goal for goal in goals if goal not in walls]:
        #Path Distance
        cat_obj = astar_cat
        cat_obj.reset()  # reseting the cat
        answer = cat_obj.find_path(start_cell=el, end_cell=goal)  # Finding the path to the goal
        path_len = 0
        if answer is not Solution.NO_SOLUTION:
            path_len = cat_obj.path.get_distance()

        if el not in path_distances:
            path_distances[el] = [{'goal': goal, 'len': path_len}]
        else:
            path_distances[el].append({'goal': goal, 'len': path_len})

path_dist_min_hits = {}
path_distances_values = []
path_distances_min_hits_values = []


#Path
for key, elem in path_distances.items():
    min_dist = min(elem, key=lambda cont : cont['len'])
    local_path_dist_values = []
    for subelem in elem:
        path_distances_values.append(subelem['len'])
        local_path_dist_values.append(subelem['len'])

    hits = count(local_path_dist_values,[min_dist['len']])
    path_distances_min_hits_values.append(hits)
    path_dist_min_hits[key] = {'len' : min_dist['len'], 'hits' : hits, 'min': min(local_path_dist_values), 'max': max(local_path_dist_values)}




# Calculate score
scores = {}
for key, elem in path_dist_min_hits.items():
    el = key
    difficulties = grid.get_difficulties()
    p1 = normalize(grid.get_cell(el).difficulty, min(difficulties), max(difficulties), reverse=False)
    p2 = normalize(elem['len'], min(path_distances_values), max(path_distances_values), reverse=True)
    p3 = normalize(elem['hits'], min(path_distances_min_hits_values), max(path_distances_min_hits_values), reverse=False)

    #score = ((p3 * 2) + p2) - p1
    score = p2 + (p3 * 3)

    if key in goals:
        score += 5

    scores[key]=score


valid_scores = [score for score in scores if score in cat_neibs_pos]

if len(valid_scores) == 0:
    sys.exit()
else:
    choosed_neib_pos = min(valid_scores, key=lambda elem : scores[elem])

    #print(cat_cell.neighbors)
    #print(neibs)
    #print(valid_scores)
    #print(choosed_neib_pos)

    print(cat_cell.neighbors[grid.get_cell(choosed_neib_pos)])



### TODO: DELETE
file.close()