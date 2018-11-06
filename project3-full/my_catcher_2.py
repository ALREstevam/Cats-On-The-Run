import sys
import random
from collections import deque
import math
from util.HexDistance import Distance
from Dubm_logger import DumbLogger


SHOW_EXCEPTIONS = True
RECORD_LOG = False
TESTING = False

if TESTING:

    print('YOU ARE IN TESTING MODE!!!', file=sys.stderr)

    cat    = (5,5)
    blocks = [(2, 8), (2, 1), (7, 7), (4, 7), (6, 5), (4, 5)]
    exits  = [(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)]
else:
    cat = eval(sys.argv[1])
    blocks = eval(sys.argv[2])
    exits = eval(sys.argv[3])

dlog = DumbLogger(RECORD_LOG)



class Catcher:
    def __init__(self, cat_pos, walls : [], goals : []):
        self.cat_pos = tuple(cat_pos)
        self.walls = set(walls)
        self.goals = set(goals)

        self.valid_goals =  [goal for goal in goals if goal not in self.walls]
        self.goal_count = len(self.valid_goals)
        self.wall_count = len(walls)

        self.cat_neibs_walkable = self.get_neibours_position(self.cat_pos, True)
        self.cat_neibs_full = self.get_neibours_position(self.cat_pos, False)

    @property
    def directions(self):
        direcs = ["NW", "NE", "W" , "E" , "SW", "SE"]
        random.shuffle(direcs)
        return direcs

    def catch_them_all(self):
        solutions = list()

        # Lista de métodos com diferentes formas de capturar o gato, executados na ordem que aparecem na lista
        # Caso retorne None ou lance exceção, passa para o próximo método da lista

        solutions.append([self.first_move, 'first_move'])
        solutions.append([self.catch_trapped_cat, 'catchTrapped'])

        # solutions.append([self.corner_closer,                   'corner_closer'])
        # solutions.append([self.danger_pos_closer,               'danger_pos_closer'])

        solutions.append([self.close_cat_is_near_exit_pathdist, 'catNearExitPathDist'])

        solutions.append([self.block_cat_path, 'block_cat_path'])

        solutions.append([self.block_cat_before_goal_0, 'block_cat_before_goal_0'])
        solutions.append([self.block_exit_neib, 'block_exit_neib'])
        # solutions.append([self.make_cat_decide,                 'make_cat_decide'])
        # solutions.append([self.catch_almost_trapped_cat,        'catchAlmostTrapped'])
        # solutions.append([self.mess_with_cat,                   'mess_with_cat'])
        # solutions.append([self.close_stategic,                  'close_stategic'])
        # solutions.append([self.heuristic_closer,                'heuristicCloser'])

        solutions.append([self.close_around_cat2, 'close_around_cat'])
        solutions.append([self.close_around_cat, 'close_around_cat'])
        solutions.append([self.close_cat_is_near_exit, 'catNearExit'])
        solutions.append([self.close_nearest_exit, 'closeNearestExit'])
        solutions.append([self.generate_random_around_cat, 'randomAroundCat'])

        solutions.append([self.generate_random_position, 'closeRandom'])

        solutions.append([self.score_closer_2, 'score_closer_2'])

        for solution in solutions:
            dlog.sep()
            dlog.log('USING method [{}]'.format(solution[1]))
            if TESTING:
                print('USING method [{}]'.format(solution[1]), file=sys.stderr)


            if SHOW_EXCEPTIONS:
                res = solution[0]()
                dlog.log('CHOOSED POSITION: [{}]'.format(res))
                if self.evaluate_solution(res, solution[1]):
                    dlog.log('RETURNING: [{}]'.format(res))
                    return res

            else:
                try:
                    res = solution[0]()
                    dlog.log('CHOOSED POSITION: [{}]'.format(res))
                    if self.evaluate_solution(res, solution[1]):
                        dlog.log('RETURNING: [{}]'.format(res))
                        return res
                except Exception as ex:
                    pass


    def evaluate_solution(self, solution, solution_name = 'NoNameSolution'):
        '''
        Método para avaliar a qualidade de uma solução e fazer log

        TODO : (uma segunda camada se segurança para conferir se a posição é válida)
        '''
        return solution is not None





    def score_closer_2(self):
        grid = [[
                    {'row': j, 'col': i,
                     'pos': (j,i),
                     'is_wall': (j, i) in self.walls,
                     'is_cat': (j, i) == self.cat_pos,
                     'is_goal': (j, i) in self.valid_goals,
                     'is_border': i in [0, 10] or j in [0, 10],
                     'cant_close': (j, i) in self.walls or (j, i) == self.cat_pos,

                     'neibs': self.get_neibours_position((j,i), exclude_non_walkable=False),
                     'walkable_neibs': self.get_neibours_position((j,i), exclude_non_walkable=True),
                     'goal_neibs': [neib for neib in self.get_neibours_position((j,i), exclude_non_walkable=True) if neib in self.valid_goals],
                     'wall_neibs': [neib for neib in self.get_neibours_position((j,i), exclude_non_walkable=False) if neib in self.walls],

                     'dist_to_cat' : 20 if
                                            ((j,i) in self.walls or (j,i) == self.cat_pos)
                                            else self.path_distance((j,i), self.cat_pos, 20),
                     'good_walls_around' : self.count_good_walls((j,i)),
                     'score': 0.0
                     }
                    for i in range(11)] for j in range(11)]


        grid_lst = []

        for row in grid:
            grid_lst.extend(row)


        #Calculationg normalization data
        goal_neibs = {
            'min': len(min(grid_lst, key=lambda x : len(x['goal_neibs']))['goal_neibs']),
            'max': len(max(grid_lst, key=lambda x : len(x['goal_neibs']))['goal_neibs'])
        }

        neib_walls = {
            'min': len(min(grid_lst, key=lambda x: len(x['wall_neibs']))['wall_neibs']),
            'max': len(max(grid_lst, key=lambda x: len(x['wall_neibs']))['wall_neibs'])
        }

        is_goal = {
            'min' : 0,
            'max' : 1,
        }

        good_walls_around = {
            'min': min(grid_lst, key= lambda x : x['good_walls_around'])['good_walls_around'],
            'max': min(grid_lst, key= lambda x : x['good_walls_around'])['good_walls_around']
        }

        dist_to_cat = {
            'min' : min(grid_lst, key=lambda x : x['dist_to_cat'])['dist_to_cat'],
            'max' : max(grid_lst, key=lambda x : x['dist_to_cat'])['dist_to_cat']
        }

        #in_danger = {
        #    'min': min(grid_lst, key=lambda x: x['in_danger'])['in_danger'],
        #    'max': max(grid_lst, key=lambda x: x['in_danger'])['in_danger']
        #}

        for cell in grid_lst:


            a = Catcher.normalize(1 if cell['is_goal'] else 0, is_goal['min'], is_goal['max'], False) * (Catcher.normalize(cell['dist_to_cat'], dist_to_cat['min'], dist_to_cat['max'], True)*2)
            b = Catcher.normalize(len(cell['goal_neibs']), goal_neibs['min'], goal_neibs['max'], False)/5
            c = Catcher.normalize(cell['dist_to_cat'], dist_to_cat['min'], dist_to_cat['max'], True) * 2
            d = Catcher.normalize(cell['good_walls_around'], good_walls_around['min'], good_walls_around['max'], False)
            e = 1 if cell['is_goal'] else 0 * Catcher.normalize(len(cell['goal_neibs']), goal_neibs['min'], goal_neibs['max'], False)
            f = self.cell_in_danger(
                pos=cell['pos'],
                dist_to_cat=cell['dist_to_cat'],
                goal_neibs_count=len(cell['goal_neibs']),
                is_goal=cell['is_goal']
            )
            g = self.in_diamond(cell['pos'])

            cell['score'] = f + d + g





        max_score = max(grid_lst, key=lambda x : x['score'])['score']
        best_candidates = []

        for cell in grid_lst:
            if cell['score']  < max_score + 0.01 and cell['score'] > max_score - 0.01 and not cell['is_wall'] and not cell['is_cat']:
                best_candidates.append(cell)

        if len(best_candidates) == 0:
            return 'NO BEST CANDIDATE'


        choosed_cell = random.choice(best_candidates)

        dlog.log('CHOOSED {} WITH SCORE {}'.format(choosed_cell['pos'], choosed_cell['score']))
        return choosed_cell['pos']



    ##################### HELPER METHODS #############################

    def in_diamond(self, pos):
        diamond_cells = (
            (0, 3), (1, 2), (3, 1), (4, 1), (5, 0), (6, 1), (7, 1), (8, 2), (9, 2), (10, 3), (9, 5), (10, 8), (9, 8),
            (8, 9), (7, 9), (6, 10), (5, 9), (4, 10), (3, 9), (2, 9), (1, 8), (0, 8), (1, 5)
        )

        return 1 if pos in diamond_cells else 0


    def count_good_walls(self, pos):
        neibs = self.get_neibours_position(pos, exclude_non_walkable=False)
        neib_walls = [neib for neib in neibs if neib in self.walls]

        wall_count = len(neib_walls)
        wall_count += 1 if pos[0] == 0 or pos[0] == 10 else 0
        wall_count += 1 if pos[1] == 0 or pos[1] == 10 else 0

        if wall_count == 0:
            count_score = .5

        elif wall_count == 1:
            count_score = .8

        elif wall_count == 2:
            count_score = 1

        elif wall_count == 3:
            count_score = .8

        elif wall_count == 4:
            count_score = .3

        elif wall_count == 5:
            count_score = .1

        elif wall_count == 6:
            count_score = 0
        else:
            count_score = 0


        opposite_score = 0

        for wall_cell in neib_walls:
            for wall_cell2 in neib_walls:

                if abs(wall_cell[0] - wall_cell2[0]) == 2 or abs(wall_cell[1] - wall_cell2[1]) == 2:
                    opposite_score = 1

                    return (count_score + opposite_score) / 2
        return (count_score + opposite_score) / 2


    def cell_in_danger(self, pos, dist_to_cat, is_goal, goal_neibs_count):
        #if pos[0] not in [10,9,1,0] and pos[1] not in[10,1,9,0]:
        #    return 0
        a = 0

        if is_goal and dist_to_cat == 1:
            a = 5
        if is_goal and dist_to_cat == 2:
            a = .7
        #if is_goal and dist_to_cat == 3:
        #    a = .5

        b = 0
        #if goal_neibs_count == 0:
        #    b = 0
        if goal_neibs_count == 1 and dist_to_cat <= 2:
            b = .8
        if goal_neibs_count == 2 and dist_to_cat <= 4:
            b = 1
        if goal_neibs_count == 3 and dist_to_cat <= 5:
            b = 1
        if goal_neibs_count >= 3 and dist_to_cat <= 2:
            b = 1
        #if goal_neibs_count == 4 and dist_to_cat <= 5:
        #    b = .7

        return (a+b)/2

    def get_candidate_neibours(self, xy):
        '''
        Obtém as posições dos vizinhos candidados (podem estar fora do grid)
        '''
        return [
            [(xy[0] - 1, xy[1] - 1), (xy[0] - 1, xy[1])][xy[0] % 2],
            [(xy[0] - 1, xy[1]), (xy[0] - 1, xy[1] + 1)][xy[0] % 2],
            [(xy[0], xy[1] - 1), (xy[0], xy[1] - 1)	][xy[0] % 2],
            [(xy[0], xy[1] + 1	),		(xy[0], xy[1] + 1)		][xy[0] % 2],
            [(xy[0] + 1, xy[1] - 1),		(xy[0] + 1, xy[1])		][xy[0] % 2],
            [(xy[0] + 1, xy[1]	),		(xy[0] + 1, xy[1] + 1)	][xy[0] % 2],
        ]

    def get_neibours_position(self, rowcol, exclude_non_walkable = True) -> list:
        '''
        Obtém a posição de vizinhos válidos
        '''
        candidates = self.get_candidate_neibours(rowcol)
        if exclude_non_walkable:

            used = self.walls.copy()
            used.add(cat)

            candidates = [elem for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10 and elem not in used]
        else:
            candidates = [elem for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10]
        return candidates


    def position_from_direction(self, rowcol, direction, walkable_only = True):
        candidates = {
            "NW": [(rowcol[0] - 1, rowcol[1] - 1), (rowcol[0] - 1, rowcol[1])][rowcol[0] % 2],
            "NE": [(rowcol[0] - 1, rowcol[1]), (rowcol[0] - 1, rowcol[1] + 1)][rowcol[0] % 2],
            "W": [(rowcol[0], rowcol[1] - 1), (rowcol[0], rowcol[1] - 1)][rowcol[0] % 2],
            "E": [(rowcol[0], rowcol[1] + 1), (rowcol[0], rowcol[1] + 1)][rowcol[0] % 2],
            "SW": [(rowcol[0] + 1, rowcol[1] - 1), (rowcol[0] + 1, rowcol[1])		][rowcol[0] % 2],
            "SE": [(rowcol[0] + 1, rowcol[1]	) ,	 (rowcol[0] + 1, rowcol[1] + 1)	    ][rowcol[0] % 2],
        }

        if not direction in candidates:
            return None
        pos = candidates[direction]

        if walkable_only:
            if self.position_is_walkable(pos):
                return pos
        else:
            if self.position_is_valid(pos):
                return pos
        return None

    def position_is_valid(self, pos):
        return pos[0] >= 0 and \
               pos[0] <= 10 and \
               pos[1] >= 0 and \
               pos[1] <= 10


    def position_is_walkable(self, pos):
        return self.position_is_valid(pos) and \
               pos not in self.walls and \
               pos != self.cat_pos

    def path_distance(self, pos1, pos2, max_dist=math.inf):
        return self.path(pos1=pos1, pos2=pos2, max_dist=max_dist)['dist']

    def path(self, pos1, pos2, max_dist=math.inf):
        pos1, pos2 = pos2, pos1
        nodes = []
        grid = [[
                    {'row': j, 'col': i,
                     'is_wall': (j, i) in self.walls,
                     'is_cat': (j, i) == self.cat_pos,
                     'is_goal': ( (j, i) in self.goals ) if (i,j) not in [pos1, pos2] else False,
                     'score': 0,
                     'previous': None,
                     'neibours': [elem for elem in [
                         [(j - 1, i - 1), (j - 1, i)][j % 2],
                         [(j - 1, i), (j - 1, i + 1)][j % 2],
                         [(j, i - 1), (j, i - 1)][j % 2],
                         [(j, i + 1), (j, i + 1)][j % 2],
                         [(j + 1, i - 1), (j + 1, i)][j % 2],
                         [(j + 1, i), (j + 1, i + 1)][j % 2],
                     ] if 0 <= elem[0] < 11 and 0 <= elem[1] < 11],
                     }
                    for i in range(11)]
                for j in range(11)]

        open_set = deque([pos1])
        closed_set = set()

        while len(open_set) > 0:
            current = open_set.popleft()

            if current == pos2:
                size_counter = 0

                temp = grid[current[0]][current[1]]
                nodes.append((temp['row'], temp['col']))
                while temp['previous'] is not None:
                    temp = temp['previous']
                    nodes.append((temp['row'], temp['col']))
                    size_counter += 1

                return {'dist': size_counter, 'path': nodes}

            valid_neighbors = [elem for elem in grid[current[0]][current[1]]['neibours']
                               if
                               not grid[elem[0]][elem[1]]['is_wall']
                               and not grid[elem[0]][elem[1]]['is_goal']
                               and elem not in closed_set
                               and elem not in open_set
                               ]

            for neibour in valid_neighbors:
                grid[neibour[0]][neibour[1]]['previous'] = grid[current[0]][current[1]]

            closed_set.add(current)

            if valid_neighbors is not None:
                open_set.extend(valid_neighbors)

        # No solution
        return {'dist': max_dist, 'path': []}

    @staticmethod
    def count(highstack, needles) -> int:
        counts = 0
        needles = set(needles)
        for elem in highstack:
            if elem in needles:
                counts += 1
        return counts

    @staticmethod
    def normalize(elem, orig_min, orig_max, reversed=False) -> float:
        if reversed:
            orig_min, orig_max = orig_max, orig_min
        if (orig_max - orig_min) == 0: return 1
        return (elem - orig_min) / (orig_max - orig_min)

c = Catcher(walls=blocks, goals=exits, cat_pos=cat)
result = c.catch_them_all()
print(result)
