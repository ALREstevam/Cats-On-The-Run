import sys
import sys
from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
from pprint import pprint
import math
from cats.catshelper.DistanceCalculator import DistanceTypes
import random
from cats.CatFather import Solution
import operator
import json

DEBUG = False

if not DEBUG:
    cat    = eval(sys.argv[1])
    walls = set(eval(sys.argv[2]))
    goals  = set(eval(sys.argv[3]))
else:
    cat    = (3,8)
    walls = set([(2, 8), (2, 1), (4, 6), (7, 7), (4,7), (6,5)])
    goals  = set([(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)])




def average(data_arr):
    if len(data_arr) == 0:
        raise ZeroDivisionError
    return sum(data_arr) / len(data_arr)


def standard_deviation(data_arr):
    if len(data_arr) == 0:
        raise ValueError

    avg = average(data_arr)

    return math.sqrt(
        (sum([ ((value - avg)**2) for value in data_arr])) /  len(data_arr)
    )





def validade_position(pos, walls, cat):
    r = pos[0]
    c = pos[1]
    return r >= 0 and r <= 10 and c >=0 and c <= 10 and (r,c) not in walls and (r,c) != cat


def get_position_by_direction(cat, direction):
    all_directions = {
        "NW": [(cat[0] - 1, cat[1] - 1),    (cat[0] - 1, cat[1])]       [cat[0] % 2 == 1],
        "NE": [(cat[0] - 1, cat[1]),        (cat[0] - 1, cat[1] + 1)]   [cat[0] % 2 == 1],
        "W": (cat[0], cat[1] - 1),
        "E": (cat[0], cat[1] + 1),
        "SW": [(cat[0] + 1, cat[1] - 1),    (cat[0] + 1, cat[1])]       [cat[0] % 2 == 1],
        "SE": [(cat[0] + 1, cat[1]),        (cat[0] + 1, cat[1] + 1)]   [cat[0] % 2 == 1],
    }
    if direction not in all_directions:
        raise ValueError
    return all_directions[direction]


def validate_direction(cat, direction, walls):
        try:
            postition = get_position_by_direction(cat, direction)
            return validade_position(postition, walls=walls, cat=cat)
        except:
            raise ValueError


def walk_to_random(cat, walls):
    directions = ['NW', 'NE', 'W', 'E', 'SW', 'SE']
    random.shuffle(directions)

    for direction in directions:
        if validate_direction(cat=cat, direction=direction, walls=walls):
            return direction
    return None





def count(highstack, needles):
    counts = 0
    needles = set(needles)
    for elem in highstack:
        if elem in needles:
            counts += 1
    return counts





def evaluate_path(path, grid):
    if path is None:
        raise ValueError

    if len(path.get_directions()) == 0:
        sys.exit()

    answer = {
        'path_len':path.get_distance(),
        'next_step':path.get_directions()[0],
        'next_pos':path.get_positions()[0],
        'path_cost': sum([grid.get_cell(pos=pos).difficulty for pos in path.get_positions()])
    }

    return answer

def calc_score(path_evaluation, amount_cats, cat_pos, walls, goals):
    hit_counter = {
        'NW' : 0,
        'NE' : 0,
        'W'  : 0,
        'E'  : 0,
        'SW' : 0,
        'SE' : 0,
    }

    for evaluation in path_evaluation:
        if evaluation['next_step'] in hit_counter:
            hit_counter[evaluation['next_step']] += 1

    all_hits = {
        'NW': {'hits': hit_counter['NW'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list' : [], 'min_len':0, 'max_len':0, 'min_len_hit': 0 , 'perfect_goal_hit': 0},
        'NE': {'hits': hit_counter['NE'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list' : [], 'min_len':0, 'max_len':0, 'min_len_hit': 0 , 'perfect_goal_hit': 0},
        'W':  {'hits': hit_counter['W'],  'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list' : [], 'min_len':0, 'max_len':0, 'min_len_hit': 0 , 'perfect_goal_hit': 0},
        'E':  {'hits': hit_counter['E'],  'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list' : [], 'min_len':0, 'max_len':0, 'min_len_hit': 0 , 'perfect_goal_hit': 0},
        'SW': {'hits': hit_counter['SW'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list' : [], 'min_len':0, 'max_len':0, 'min_len_hit': 0 , 'perfect_goal_hit': 0},
        'SE': {'hits': hit_counter['SE'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list' : [], 'min_len':0, 'max_len':0, 'min_len_hit': 0 , 'perfect_goal_hit': 0},
    }

    for direction in ['NW', 'NE', 'W', 'E', 'SW', 'SE']:
        if DEBUG:
            print('TESING DIRECTION: ' + direction)
        if not validate_direction(cat_pos, direction, walls):
            if DEBUG:
                print('INVALID!')
            del all_hits[direction]


    for evaluation in path_evaluation:
        if evaluation['next_step'] in hit_counter:
            evaluation['hits'] = hit_counter[evaluation['next_step']]

        if evaluation['next_step'] in all_hits:
            next_step = all_hits[evaluation['next_step']]

            next_step['totalCost'] += evaluation['path_cost']
            next_step['totalLen'] += evaluation['path_len']

            next_step['len_list'].append(evaluation['path_len'])

            next_step['min_len'] = min(next_step['len_list'])
            next_step['max_len'] = max(next_step['len_list'])
            next_step['min_len_hit'] = count(next_step['len_list'], [next_step['min_len']])
            next_step['perfect_goal_hit'] = count(next_step['len_list'], [next_step['min_len'] + 2,next_step['min_len'] + 3])

    elems_to_remove = set()
    for key, hit_result in all_hits.items():
        if hit_result['totalLen'] > 0:
            hit_result['avgCost'] = float(hit_result['totalCost']) / float(hit_result['hits'])

        if hit_result['totalLen'] > 0:
            hit_result['avgLen'] = sorted(hit_result['len_list'])[len(hit_result['len_list'])//2]
            #hit_result['avgLen'] = float(hit_result['totalLen']) / float(hit_result['hits'])


        path_len_mult = 1
        difficulty_mult = 0
        hits_mult = 0
        min_hit_mult = 2
        perfect_goal_hit_mult = 0

        with open('log.txt', 'a+') as file:
            file.write('{}\n'.format(hit_result))

        if len([avaliable for avaliable in goals if avaliable not in walls]) == 0:
            difficulty_mult = 5

        #Score calculation
        p1 = ( 1 / hit_result['avgLen'] if hit_result['avgLen']              > 0 else 0 ) * path_len_mult
        p2 = ( 1 / hit_result['avgCost'] if hit_result['avgCost']            > 0 else 0 ) * difficulty_mult
        p3 = ( hit_result['hits'] / (len(goals) * amount_cats) if len(goals) > 0 else 0 ) * hits_mult
        p4 = ( hit_result['min_len_hit'] / len(goals) if len(goals)          > 0 else 0 ) * min_hit_mult
        p5 = ( hit_result['perfect_goal_hit']  / len(goals) if len(goals)    > 0 else 0 ) * perfect_goal_hit_mult

        score = p1 + p2 + p3 + p4 + p5


        if DEBUG:
            print(hit_result['avgLen'])
            print('len: {:.2f} | cost {:.2f} | hits {:.2f} | min_len {:.2f} | perfect_dist {:.2f}| SUM {:.2f}'.format(p1, p2, p3, p4, p5, score))

        hit_result['score'] = score

        if hit_result['score'] == 0:
            elems_to_remove.add(key)

        '''
        data = []
        with open('result.json') as json_data:
            data = json.load(json_data)

        with open('result.json', 'w') as file:
            pos = get_position_by_direction(cat, key)
            for elem in data:
                if elem['pos'] == pos:
                    data.remove(elem)

            data.append({'pos':pos, 'score':score})
            json.dump(data, file)
        '''

    for key in elems_to_remove:
        all_hits.pop(key)

    return all_hits

def execute_paths(cat_pos, goals, walls):

    #Creatign the grid
    grid = Grid(goals, walls, cat_pos, rows=11, cols=11)
    cat_cell = grid.get_cell(cat_pos)

    if DEBUG:
        pprint(cat_cell.neighbors)

    # Cat is trapped
    if len([valid_neib for valid_neib in cat_cell.neighbors if not valid_neib.is_wall]) == 0:
        if DEBUG:
            print('CAT IS TRAPPED')
        sys.exit()

    #Go for it
    for neib in cat_cell.neighbors:
        if neib.is_goal and not neib.is_wall:
            if DEBUG:
                print('GO FOR IT!')
            print(cat_cell.neighbors[neib])
            return

    # Go for it II
    goal_counter = {}
    for cat_neib in cat_cell.neighbors:
        if not cat_neib.is_wall:
            goal_counter[cat_neib] = 0
            for neib_neib in [neib for neib in cat_neib.neighbors if not neib.is_wall]:
                if neib_neib.is_goal:
                    goal_counter[cat_neib] += 1

    if DEBUG:
        pprint(goal_counter)


    neib_exit_sum = 0
    for neib, value in goal_counter.items():
        if value >= 2:
            neib_exit_sum += value
        if value >= 5:
            if DEBUG:
                print('GO FOR IT II')
            print(cat_cell.neighbors[neib])
            return

    if neib_exit_sum >= 4:
        neib = max(goal_counter.items(), key=operator.itemgetter(1))[0]
        print(cat_cell.neighbors[neib])
        return


    if DEBUG:
        print('GOAL COUNTER')
        pprint(goal_counter)

    grid.assign_difficulty(3)

    if DEBUG:
        print(grid.show_difficulties())

    #Creating cats
    astar_cat = AstarCat( max_iterations=200, grid=grid, gWeight=1, hWeight=1, fWeight=1, distanceType=DistanceTypes.HEX)
    best_first_cat = BestFirstSearchCat( grid=grid, distance_type=DistanceTypes.HEX)
    bfs_cat = BreadthFirstSearchCat(grid=grid)

    cats = [astar_cat, best_first_cat, bfs_cat]

    evaluations = []

    #Getting paths - (for each cat (for each goal))
    for goal in [goal for goal in goals if goal not in walls]:
        for catInstance in cats:
            catInstance.reset() #reseting the cat
            answer = catInstance.find_path(start_cell=cat, end_cell=goal) #Finding the path to the goal

            if answer is Solution.NO_SOLUTION:
                walls.add(goal)

            evaluations.append(evaluate_path(path=catInstance.path, grid=grid)) # Adding solution data to evaluation array
            if DEBUG:
                print(grid.show(catInstance))

    # Calculating score and score data
    hits = calc_score(
        evaluations,
        len(cats),
        cat_pos,
        walls,
        goals,
    )

    if DEBUG:
        print('HITS')
        print(hits)

    #Choosing the direction with best score
    if len(list(hits.items())) == 0:
        walk_to = walk_to_random(cat_pos, walls)
        #sys.exit()
    else:
        walk_to = max(list(hits.items()), key = lambda item : float(item[1]['score']))[0]


    table = ''
    table += '\ndir | hits  |  len | cost | score | min_len | max_len | min_len_hit  |\n'
    table += '----+-------+------+------+-------+---------+---------+--------------|\n'
    for direction, hit in hits.items():
        table += ('{:3s} | {:5.2f} | {:.2f} | {:.2f} | {:5.2f} | {:7} | {:7} | {:12} |\n'.format(
            direction,
             hit['hits'] / len(goals) if hit['hits'] > 0 else 0,
            1 / hit['avgLen'] if hit['avgLen'] > 0 else 0,
            1 / hit['avgCost'] if hit['avgCost'] > 0 else 0,
            hit['score'],
            hit['min_len'],
            hit['max_len'],
            hit['min_len_hit']
            )
        )
    table += 'WALK TO'

    if DEBUG:
        print(table)

    if walk_to is None:
        if DEBUG:
            print('CAT IS GIVING UP')
        sys.exit()

    print(walk_to)

execute_paths(cat_pos=cat, goals=goals, walls=walls)






