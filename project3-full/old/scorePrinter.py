import sys
import random
import subprocess
from PIL import Image, ImageDraw
from grid.Grid import Grid
import json
import sys
import sys


#############################################################################
from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
from pprint import pprint
import math
from cats.catshelper.DistanceCalculator import DistanceTypes
from cats.CatFather import Solution
import operator
from cats.catshelper.DistanceCalculator import Distance2DCalculator
#############################################################################

cat    = (7,7)
blocks = set([(2, 8), (2, 1), (4, 6), (7, 7), (4,7), (6,5)])
blocks = set([])
exits  = set([(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)])


#################################################################
#                      INSERTED CODE
#################################################################
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
    if (orig_max-orig_min) == 0: return 1
    return (elem - orig_min)/(orig_max-orig_min)

def translate_1(value, in_from, in_to, out_from, out_to):
    out_range = out_to - out_from
    in_range = in_to - in_from
    in_val = value - in_from
    val = (float(in_val) / in_range) * out_range
    out_val = out_from + val
    return out_val


def translate(value, in_from, in_to, out_from, out_to):
    answer = translate_1(value, in_from, in_to, out_from, out_to)
    return answer if answer >= 0 else 0


goals = exits
walls = blocks

grid = Grid(goals,walls, cat, rows=11, cols=11)
grid.assign_difficulty(3)

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

path_distances = {}
hex_distances = {}

dc = Distance2DCalculator()

for i in range(11):
    for j in range(11):

        el = (j, i)

        goal_count = 0
        for goal in [goal for goal in goals if goal not in walls]:
            goal_count += 1


            if el != goal:

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


                #Hex Distance

                path_len = dc.distCoordsTuple(el, goal)

                if el not in hex_distances:
                    hex_distances[el] = [{'goal': goal, 'len': math.ceil(path_len)}]
                else:
                    hex_distances[el].append({'goal': goal, 'len': math.ceil(path_len)})


#pprint(path_distances)
#pprint(hex_distances)

path_dist_min_hits = {}
hex_dist_min_hits = {}

path_distances_values = []
hex_distances_values = []

path_distances_min_hits_values = []
hex_distances_min_hits_values = []


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

#Hex
for key, elem in hex_distances.items():
    min_dist = min(elem, key=lambda cont : cont['len'])
    for subelem in elem:
        hex_distances_values.append(subelem['len'])
    hits = count(hex_distances_values,[min_dist['len']])
    hex_distances_min_hits_values.append(hits)
    hex_dist_min_hits[key] = {'len' : min_dist['len'], 'hits' : hits}

#########################################################################

def compute_image(cat, blocks, exits):
    im = Image.open("tabuleiros/tabuleiro.jpg")
    draw = ImageDraw.Draw(im, 'RGBA')


    #######################################################################
    #                       INSERTED CODE
    #######################################################################
    #Score
    for key, elem in path_dist_min_hits.items():
        el = key
        shrink = 5

        difficulties = grid.get_difficulties()
        p1 = normalize(grid.get_cell(el).difficulty, min(difficulties), max(difficulties), reverse=False)
        p2 = normalize(elem['len'], min(path_distances_values), max(path_distances_values), reverse=True)
        p3 = normalize(elem['hits'], min(path_distances_min_hits_values), max(path_distances_min_hits_values),
                       reverse=False)
        #dist = ((p3 * 2) + p2) - p1
        dist = p2 + p3
        if key in goals:
            dist += 5
        print('{} : {}'.format(el, dist))

        color = 'hsl(' + str(int(translate(dist, 0, 2, 100, 0))) + ', 100%, 50%)'

        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink
        draw.ellipse([init_x, init_y, end_x, end_y], fill=color)
    #####################################################################

    # Goals
    for el in exits:
        shrink = 10

        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink
        draw.ellipse([init_x, init_y, end_x, end_y], fill="rgba(0, 0, 255, 200)")

    # Blocks
    for el in blocks:
        shift = el[0] % 2 * 25
        init_x = shift + el[1] * 50 + el[1] * 5
        end_x = shift + (el[1] + 1) * 50 + el[1] * 5
        init_y = el[0] * 49
        end_y = (el[0] + 1) * 49
        draw.line([init_x + 10, init_y + 10, end_x - 10, end_y - 10], fill="red", width=6)
        draw.line([init_x + 10, end_y - 10, end_x - 10, init_y + 10], fill="red", width=6)

    # Cat
    for el in [cat]:
        shrink = 10

        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink

        draw.ellipse([init_x, init_y, end_x, end_y], fill="#808080")

        draw.point((init_x, init_y), fill='red')

        draw.polygon([(init_x, init_y + shrink), (init_x + 5, init_y - 10), (init_x + 15, init_y + 5)], fill="#808080")
        draw.polygon([(init_x + 30, init_y + shrink), (init_x + 25, init_y - 10), (init_x + 15, init_y + 5)],
                     fill="#808080")

        draw.ellipse([init_x + 6, init_y + 6, init_x + 11, init_y + 11], fill="black")
        draw.ellipse([init_x + 8 + 10, init_y + 6, init_x + 13 + 10, init_y + 11], fill="black")
        draw.polygon([(init_x + 12, init_y + 15), (init_x + 18, init_y + 15), (init_x + 15, init_y + 18)], fill="black")

    del draw
    return im



images = list()
images.append(compute_image(cat, blocks, exits))
images[0].save('testing/test.gif',
                   save_all=True,
                   append_images=images[1:],
                   duration=350,
                   loop=0)


