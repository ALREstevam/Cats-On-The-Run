# encoding: utf-8

import sys
import random
import math
from collections import deque
from pprint import pprint
log = open('log.txt', 'a')

random.seed(256)


cat    = eval(sys.argv[1])
walls = set(eval(sys.argv[2]))
goals  = set(eval(sys.argv[3]))

log.write('WALLS: {}\n'.format(walls))

#cat    =(5, 5)
#walls = [(1, 8), (2, 1), (4, 6)]
#goals  =[(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)]

def random_movement(cat) :
    candidates = [
            [(cat[0] - 1, cat[1] - 1 ,     "NW"), (cat[0] - 1 , cat[1]     ,     "NW") ] [cat[0] % 2],
            [(cat[0] - 1, cat[1]     ,     "NE"), (cat[0] - 1 , cat[1] + 1 ,     "NE") ] [cat[0] % 2],
            [(cat[0]    , cat[1] - 1 ,     "W" ), (cat[0]     , cat[1] - 1 ,     "W")  ] [cat[0] % 2],
            [(cat[0]    , cat[1] + 1 ,     "E" ), (cat[0]     , cat[1] + 1 ,     "E")  ] [cat[0] % 2],
            [(cat[0] + 1, cat[1] - 1 ,     "SW"), (cat[0] + 1 , cat[1]     ,     "SW") ] [cat[0] % 2],
            [(cat[0] + 1, cat[1]     ,     "SE"), (cat[0] + 1 , cat[1]+1   ,     "SE") ] [cat[0] % 2],
        ]

    filtered_candidates = [cand for cand in candidates if (cand[0], cand[1]) not in walls]
    log.write('POSSIBLE RANDOMS: {}\n'.format(filtered_candidates))
    return random.choice(filtered_candidates)



def get_direction(pos1, pos2):
    candidates = None

    if pos1[0] % 2 == 0:
        candidates =  {
                  (pos1[0] - 1, pos1[1] - 1) : "NW",
                  (pos1[0] - 1, pos1[1])     : "NE",
                  (pos1[0], pos1[1] - 1)     : "W" ,
                  (pos1[0], pos1[1] + 1)     : "E" ,
                  (pos1[0] + 1, pos1[1] - 1) : "SW",
                  (pos1[0] + 1, pos1[1])     : "SE",
                }
    else:
        candidates = {
                (pos1[0] - 1, pos1[1]): "NW",
                (pos1[0] - 1, pos1[1] + 1): "NE",
                (pos1[0], pos1[1] - 1): "W",
                (pos1[0], pos1[1] + 1): "E",
                (pos1[0] + 1, pos1[1]): "SW",
                (pos1[0] + 1, pos1[1] + 1): "SE",
        }
    return candidates[pos2]

def make_path(cat, goal):
    grid = [[
                {'row': j, 'col': i,
                 'is_wall': (j, i) in walls,
                 'is_cat': (j, i) == cat,
                 'is_goal': (j, i) in goals,
                 'is_border': i in [0, 10] or j in [0, 10],
                 'cant_close': (j, i) in walls or (j, i) == cat,
                 'score': 0,
                 'previous': None,
                 'neibours': [elem for elem in [
                     [  (j - 1, i - 1)  ,     (j - 1, i)]             [j % 2],
                     [  (j - 1, i)      ,     (j - 1, i + 1)]         [j % 2],
                     [  (j, i - 1)      ,     (j, i - 1)]             [j % 2],
                     [  (j, i + 1)      ,     (j, i + 1)]             [j % 2],
                     [  (j + 1, i - 1)  ,     (j + 1, i)]             [j % 2],
                     [  (j + 1, i)      ,     (j + 1, i + 1)]         [j % 2],
                 ] if 0 <= elem[0] < 11 and 0 <= elem[1] < 11],
                 }
                for i in range(11)]
            for j in range(11)]

    open_set = deque([goal])
    closed_set = set()

    while len(open_set) > 0:
        current = open_set.popleft()

        if current == cat:

            path = []
            temp = grid[current[0]][current[1]]
            path.append((temp['row'], temp['col']))

            while temp['previous'] is not None:
                path.append((temp['previous']['row'], temp['previous']['col']))
                temp = temp['previous']

            return path


        valid_neighbors = [elem for elem in grid[current[0]][current[1]]['neibours']
                           if
                           not grid[elem[0]][elem[1]]['is_wall']
                           and elem not in closed_set
                           and elem not in open_set
                           ]

        for neibour in valid_neighbors:
            grid[neibour[0]][neibour[1]]['previous'] = grid[current[0]][current[1]]

        closed_set.add(current)

        if valid_neighbors is not None:
            open_set.extend(valid_neighbors)
    # No solution
    return None


def evaluate_paths():
    directions = []
    for goal in [g for g in goals if g not in walls]:
        path = make_path(cat, goal)

        if path is not None:
            directions.append(get_direction(path[0], path[1]))

    directions.sort()
    log.write('POSSIBLE DIRECTIONS: {}'.format(directions))


    if len(directions) == 0:
        move = random_movement(cat)[2]
        log.write('RANDOM {}\n'.format(move))
        print(move)
    else:
        move = directions[0]
        print(move)
        log.write('PATH {}\n'.format(move))


evaluate_paths()
log.close()