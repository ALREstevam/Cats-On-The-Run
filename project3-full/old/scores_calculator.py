from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
from pprint import pprint
from pprint import pformat
import math
from cats.catshelper.DistanceCalculator import DistanceTypes
from cats.CatFather import Solution
import operator
from cats.catshelper.DistanceCalculator import Distance2DCalculator
import sys
import random


class Log:
    def __init__(self):
        self.file = 'log1.txt'
    def write(self, str, end='\n'):
        with open(self.file, 'a') as file:
            file.write('{}{}'.format(str, end))
    def space(self,):
        with open(self.file, 'a') as file:
            file.write('\n\n\n')
    def sep(self):
        with open(self.file, 'a') as file:
            file.write('\n\n' + '-' * 30 + '\n\n')


class Log:
    def __init__(self):
        self.file = 'log1.txt'
    def write(self, str, end='\n'):
        pass
    def space(self,):
        pass
    def sep(self):
        pass
log = Log()

class GridHelper:
    @staticmethod
    def direction_to(from_cell, to_cell):
        pos1 = from_cell.pos
        pos2 = to_cell.pos

        ns = ''
        eo = ''

        if pos1[0] > pos2[0]:
            ns = 'S'
        if pos1[0] < pos2[0]:
            ns = 'N'
        if pos1[1] > pos2[1]:
            eo = 'E'
        if pos1[1] < pos2[1]:
            eo = 'W'

        # NS EO
        if ns != '' and eo != '':
            return [ns+eo]
        # NS
        if ns != '' and eo == '':
            return ['NE', 'NW', 'SE', 'SW']
        # EO
        if ns == '' and eo != '':
            return [eo]
        # NONE
        if ns == '' and eo == '':
            return []

    @staticmethod
    def direction_is_valid(walls, cat, direction):
        pos = GridHelper.get_position_by_direction(cat, direction)
        return pos not in walls and pos != cat and pos[0] >= 0 and pos[0] <= 10 and pos[1] >= 0 and pos[1] <= 10


    @staticmethod
    def get_position_by_direction(cat, direction):
        all_directions = {
            "NW": [(cat[0] - 1, cat[1] - 1), (cat[0] - 1, cat[1])][cat[0] % 2 == 1],
            "NE": [(cat[0] - 1, cat[1]), (cat[0] - 1, cat[1] + 1)][cat[0] % 2 == 1],
            "W": (cat[0], cat[1] - 1),
            "E": (cat[0], cat[1] + 1),
            "SW": [(cat[0] + 1, cat[1] - 1), (cat[0] + 1, cat[1])][cat[0] % 2 == 1],
            "SE": [(cat[0] + 1, cat[1]), (cat[0] + 1, cat[1] + 1)][cat[0] % 2 == 1],
        }
        if direction not in all_directions:
            raise ValueError('Invalid direction ' + str(direction))
        return all_directions[direction]

    @staticmethod
    def combine_directions(first, second, walls, cat):
        combine_dict = {
            ('N', 'S')  : [['NW', 'NE', 'SW', 'SE']]    ,
            ('N', 'E')  : [['NE'], ['E']]               ,
            ('N', 'W')  : [['NW'], ['W']]               ,
            ('N', 'NW') : [['NW'], ['W']]               ,
            ('N', 'NE') : [['NE'], ['E']]               ,
            ('N', 'SW') : [['W', 'NE'], ['SW']]         ,
            ('N', 'SE') : [['NE', 'E']]                 ,
            ('S', 'E')  : [['SE'], ['E']]               ,
            ('S', 'W')  : [['SW'], ['W']]               ,
            ('S', 'NW') : [['W', 'SW'], ['NW']]         ,
            ('S', 'NE') : [['E', 'SE'], ['NE'], ['E']]  ,
            ('S', 'SW') : [['SW'], ['W']]               ,
            ('S', 'SE') : [['SE'], ['E']]               ,
            ('E', 'W')  : [['E', 'W']]                  ,
            ('E', 'NW') : [['NE'], ['E', 'NW']]         ,
            ('E', 'NE') : [['E'], ['NE']]               ,
            ('E', 'SW') : [['SE'], ['E', 'SW']]         ,
            ('E', 'SE') : [['E'], ['SE']]               ,
            ('W', 'NW') : [['W'], ['NW']]               ,
            ('W', 'NE') : [['NW'], ['W', 'NE']]         ,
            ('W', 'SW') : [['W'], ['SW']]               ,
            ('W', 'SE') : [['SW'], ['W', 'SE']]         ,
            ('NW', 'NE'): [['NW, NE']]                  ,
            ('NW', 'SW'): [['W'], ['NW', 'SW']]         ,
            ('NW', 'SE'): [['NW', 'SE']]                ,
            ('NE', 'SW'): [['NE', 'SW']]                ,
            ('NE', 'SE'): [['E'], ['NE', 'SE']]         ,
            ('SW', 'SE'): [['SW', 'SE']]                ,
            ('N','N')   : [['NW', 'NW']]                ,
            ('S', 'S')  : [['SW', 'SE']]                ,
            ('E', 'E')  : [['E'], ['NE', 'SE']]         ,
            ('W', 'W')  : [['W'], ['NW', 'SW']]         ,
            ('NE', 'NE'): [['NE'], ['E'], ['NW']]       ,
            ('SE', 'SE'): [['SE'], ['E'], ['SW']]       ,
            ('NW', 'NW'): [['NW'], ['W'], ['NE']]       ,
            ('SW', 'SW'): [['SW'], ['W'], ['SE']]       ,

        }
        dirs = None

        if (first, second) in combine_dict:
            dirs = combine_dict[(first, second)]
        elif (second, first) in combine_dict:
            dirs = combine_dict[(second, first)]

        else:
            raise ValueError('Invalid direction combination {}'.format((first, second)))

        if dirs is None:
            raise ValueError('Invalid direction combination {}'.format((first, second)))

        answer = None
        for directions_arr in dirs:
            if len(directions_arr) == 1:
                if GridHelper.direction_is_valid(walls, cat, directions_arr[0]):
                    return directions_arr[0]
            else:
                random.shuffle(directions_arr)

                for elem in directions_arr:
                    if GridHelper.direction_is_valid(walls, cat, elem):
                        return elem
        return answer


class Helper:
    @staticmethod
    def valid_goals(goals, walls, cat_pos):
        return [goal for goal in goals if goal not in walls and goal != cat_pos]

    @staticmethod
    def count(highstack, needles):
        counts = 0
        needles = set(needles)
        for elem in highstack:
            if elem in needles:
                counts += 1
        return counts

    @staticmethod
    def normalize(elem, orig_min, orig_max, reverse=False):
        if reverse:
            orig_min, orig_max = orig_max, orig_min
        if (orig_max - orig_min) == 0: return 1
        return (elem - orig_min) / (orig_max - orig_min)

    @staticmethod
    def average(lst):
        return sum(lst) / float(len(lst))

class ScoreCalculator:

    def __init__(self, goals, walls, grid_difficulty_spread = 3):
        self.grid = Grid(goals, walls, (5,5), rows=11, cols=11)
        self.grid.assign_difficulty(grid_difficulty_spread)
        self.grid_difficulty_spread = grid_difficulty_spread
        self.score_range = (0,1)
        self.dist = DistanceTypes.HEX

        astar_cat = AstarCat(
            max_iterations=200,
            grid=self.grid,
            gWeight=1,
            hWeight=1,
            fWeight=1,
            distanceType=self.dist
        )

        best_first_cat = BestFirstSearchCat(
            grid=self.grid,
            distance_type=self.dist
        )
        bfs_cat = BreadthFirstSearchCat(
            grid=self.grid
        )

        self.cat_obj = astar_cat
        self.normalization = None


    def reset(self, walls, goals, cat_pos):
        self.cat_obj.reset()

        self.grid.redesign_reset_grid(walls=walls, goals=goals, start=cat_pos)

        self.grid.assign_difficulty(self.grid_difficulty_spread)



    def normalization_data(self, cell_set, goals, walls, cat_pos):
        goals = set(Helper.valid_goals(walls, goals, cat_pos))
        self.reset(walls, goals, cat_pos)

        dif_lst = []
        len_lst = []
        min_len_list = []

        log.write(pformat(cell_set))

        for cell in cell_set:

            if cell.is_wall:
                continue
            local_len = []

            for goal in goals:

                log.write('{}'.format(goal in walls))

                #if goal in walls:
                #    continue

                result = self.cat_obj.find_path(start_cell=cell.pos, end_cell=goal)

                log.write(result)

                if self.cat_obj.path is None:
                    continue
                else:
                    distance = self.cat_obj.path.get_distance()
                    difficulty = self.cat_obj.path.get_difficulty()

                    log.write('distance : {}'.format(distance))

                local_len.append(distance)
                len_lst.append(distance)
                dif_lst.append(difficulty)
            min_len_list.append(min(local_len))


        result = {
            'norm_dmin': min(dif_lst),
            'norm_dmax': max(dif_lst),
            'norm_lmin': min(len_lst),
            'norm_lmax': max(len_lst),
            'norm_min_min_len': min(len_lst),
            'norm_min_max_len': max(len_lst),
        }

        log.write('LEN LIST: {}'.format(len_lst))


        self.cat_obj.reset()  # resets the cat
        self.normalization = result

        return result

    def calculate(self, pos, walls, goals, cat_pos, full_result = False):
        if self.normalization is None:
            self.normalization_data(
                cell_set=self.grid.as_list(),
                goals=goals,
                walls=walls,
                cat_pos=cat_pos
            )

        goals = set(Helper.valid_goals(walls, goals, cat_pos))

        len_list = []
        difficulty_list = []

        for goal in goals:
            self.cat_obj.find_path(start_cell = pos, end_cell= goal)

            if self.cat_obj is None or self.cat_obj.path is None:
                distance = 50
                difficulty = 50
            else:
                distance =  self.cat_obj.path.get_distance()
                difficulty = self.cat_obj.path.get_difficulty()

            len_list.append(distance)
            difficulty_list.append(difficulty)
            self.cat_obj.reset() #resets the cat

        # PATH LENGHT

        len_list.sort()
        difficulty_list.sort()

        llen = 0
        if len(len_list) == 0:
            llen = 10
        else:
            for i in range(min([len(len_list), 3])):
                llen += len_list[i]
            llen /= min([len(len_list), 3])


        # MIN LEN HITS
        min_len_hits = Helper.count(highstack=len_list, needles=[len_list[0]])


        # DIFFICULTY
        dif = 0
        if len(difficulty_list) == 0:
            dif = 10
        else:
            for i in range(min([ len(difficulty_list), 3] )):
                dif += difficulty_list[i]
            dif /= min([len(difficulty_list), 3])


        # CALCULATING SCORE
        return self.score(
            {'goal_len' : llen, 'mhits': min_len_hits},
            {'dif' : dif},
            self.normalization,
            pos,
            full_result
        )

    def score(self, len_data, dif_data, norm_data, pos, all_arguments = False):
        # Path len
        p1 = Helper.normalize(
            len_data['goal_len'],
            norm_data['norm_lmin'],
            norm_data['norm_lmax'],
            reverse=True
        )

        # MinHits
        p2 = Helper.normalize(
            len_data['mhits'],
            norm_data['norm_min_min_len'],
            norm_data['norm_min_max_len'],
            reverse=False
        )

        log.write('HITS: {} | MIN: {} | MAX: {}'.format(
            len_data['mhits'],
            norm_data['norm_min_min_len'],
            norm_data['norm_min_max_len']
            )
        )

        log.sep()



        #Path Difficulty
        a1 = Helper.normalize(
            dif_data['dif'],
            norm_data['norm_dmin'],
            norm_data['norm_dmax'],
            reverse=True
        )



        #Local Difficulty
        self.grid.assign_difficulty(self.grid_difficulty_spread)
        difficulties = self.grid.get_difficulties()
        a2 = Helper.normalize(
            self.grid.get_cell(pos).difficulty,
            min(difficulties),
            max(difficulties),
            reverse=True
        )



        score =   p2
        self.grid.get_cell(pos).score = score
        self.score_range = (0,5)


        if all_arguments:
            return {'score' : score, 'p1': p1, 'p2': p2, 'a1':a1, 'a2':a2}
        return score

    def scores(self, walls, goals, cat_pos):
        self.reset(walls=walls, goals=goals, cat_pos=cat_pos)

        self.normalization_data(
            cell_set=self.grid.as_list(),
            goals=goals,
            walls=walls,
            cat_pos=cat_pos)

        scores_dict = {}
        for i in range(11):
            for j in range(11):
                el = (i, j)

                if el in walls:
                    score = {'score' : 0, 'p1': 0, 'p2': 0, 'a1':0, 'a2':0}
                else:
                    score = self.calculate(el, walls, goals, cat_pos, full_result=True)
                self.grid.get_cell(el).score = score['score']

                scores_dict[el] = score
        return scores_dict