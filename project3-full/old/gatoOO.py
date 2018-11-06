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


class GatoFujao():
    def __init__(self, cat, walls, goals, is_debug = False):
        self.cat = cat
        self.walls = walls
        self.goals = goals

        self.grid = None

        self.DEBUG = is_debug

        self.rows = 11
        self.cols = 11

    @staticmethod
    def average(data_arr):
        if len(data_arr) == 0:
            raise ZeroDivisionError
        return sum(data_arr) / len(data_arr)

    @staticmethod
    def standard_deviation(data_arr):
        if len(data_arr) == 0:
            raise ValueError

        avg = GatoFujao.average(data_arr)

        return math.sqrt(
            (sum([((value - avg) ** 2) for value in data_arr])) / len(data_arr)
        )

    @staticmethod
    def count(highstack, needles):
        counts = 0
        needles = set(needles)
        for elem in highstack:
            if elem in needles:
                counts += 1
        return counts

    @staticmethod
    def get_position_by_direction(pos, direction):
        all_directions = {
            "NW": [(pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1])][pos[0] % 2 == 1],
            "NE": [(pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] + 1)][pos[0] % 2 == 1],
            "W": (pos[0], pos[1] - 1),
            "E": (pos[0], pos[1] + 1),
            "SW": [(pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1])][pos[0] % 2 == 1],
            "SE": [(pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + 1)][pos[0] % 2 == 1],
        }
        if direction not in all_directions:
            raise ValueError
        return all_directions[direction]

    def validate_position(self, pos):
        r = pos[0]
        c = pos[1]
        return r >= 0 and r <= self.rows-1 and c >= 0 and c <= self.cols-1 and (r, c) not in self.walls and (r, c) != self.cat

    def validate_direction(self, direction):
        try:
            postition = self.get_position_by_direction(self.cat, direction)
            return self.validate_position(postition)
        except:
            raise ValueError

    def walk_to_random(self):
        directions = ['NW', 'NE', 'W', 'E', 'SW', 'SE']
        shuffle(directions)

        for direction in directions:
            if self.validate_direction(direction=direction):
                return direction
        return None

    def create_grid(self):
        self.grid = Grid(self.goals, self.walls, self.cat, rows=self.rows, cols=self.cols)

    def is_cat_trapped(self, cat_cell):
        return len([valid_neib for valid_neib in cat_cell.neighbors if not valid_neib.is_wall]) == 0

    def go_for_it(self, cat_cell):
        for neib in cat_cell.neighbors:
            if neib.is_goal and not neib.is_wall:
                return True, cat_cell.neighbors[neib]
        return False, None

    def go_for_it_2(self, cat_cell):
        goal_counter = {}
        for cat_neib in cat_cell.neighbors:
            if not cat_neib.is_wall:
                goal_counter[cat_neib] = 0
                for neib_neib in [neib for neib in cat_neib.neighbors if not neib.is_wall]:
                    if neib_neib.is_goal:
                        goal_counter[cat_neib] += 1

        neib_exit_sum = 0
        for neib, value in goal_counter.items():
            if value >= 2:
                neib_exit_sum += value
            if value >= 5:
                return True, cat_cell.neighbors[neib]

        if neib_exit_sum >= 4:
            neib = max(goal_counter.items(), key=operator.itemgetter(1))[0]
            return True, cat_cell.neighbors[neib]
        return False, None

    def create_cats(self):
        dist = DistanceTypes.HEX
        astar_cat = AstarCat(
            max_iterations=200,
            grid=self.grid,
            gWeight=1,
            hWeight=1,
            fWeight=1,
            distanceType=dist
        )
        best_first_cat = BestFirstSearchCat(
            grid=self.grid,
            distance_type=dist
        )
        bfs_cat = BreadthFirstSearchCat(
            grid=self.grid
        )

        return [astar_cat, best_first_cat, bfs_cat]

    def evaluate_all_paths(self, cats):
        # Getting paths - (for each cat (for each goal))
        evaluations = []

        for goal in [goal for goal in self.goals if goal not in self.walls]:
            for catInstance in cats:
                catInstance.reset()  # reseting the cat
                answer = catInstance.find_path(start_cell=self.cat, end_cell=goal)  # Finding the path to the goal

                if answer is Solution.NO_SOLUTION:
                    self.walls.add(goal)

                # Adding solution data to evaluation array
                evaluations.append(
                    self.evaluate_a_path(path=catInstance.path)
                )
        return evaluations

    def evaluate_a_path(self, path):
        if path is None:
            raise ValueError

        if len(path.get_directions()) == 0:
            sys.exit()

        answer = {
            'path_len': path.get_distance(),
            'next_step': path.get_directions()[0],
            'next_pos': path.get_positions()[0],
            'path_cost': sum([self.grid.get_cell(pos=pos).difficulty for pos in path.get_positions()])
        }
        return answer

    def get_info_table(self, hits):
        table = ''
        table += '\ndir | hits  |  len | cost | score | min_len | max_len | min_len_hit  |\n'
        table += '----+-------+------+------+-------+---------+---------+--------------|\n'
        for direction, hit in hits.items():
            table += ('{:3s} | {:5.2f} | {:.2f} | {:.2f} | {:5.2f} | {:7} | {:7} | {:12} |\n'.format(
                direction,
                hit['hits'] / len(self.goals) if hit['hits'] > 0 else 0,
                1 / hit['avgLen'] if hit['avgLen'] > 0 else 0,
                1 / hit['avgCost'] if hit['avgCost'] > 0 else 0,
                hit['score'],
                hit['min_len'],
                hit['max_len'],
                hit['min_len_hit']
            )
        )
        return table

    def calc_score(self, path_evaluation, amount_cats):
        #Contador de hits (soma de: para todos os caminhos, para qual direção vai o primeiro passo?)
        hit_counter = {'NW': 0, 'NE': 0, 'W': 0, 'E': 0, 'SW': 0,'SE': 0}

        #Contando os hits
        for evaluation in path_evaluation:
            if evaluation['next_step'] in hit_counter:
                hit_counter[evaluation['next_step']] += 1

        next_directions_data = {
            'NW': {'hits': hit_counter['NW'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list': [],'min_len': 0, 'max_len': 0, 'min_len_hit': 0, 'perfect_goal_hit': 0},
            'NE': {'hits': hit_counter['NE'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list': [],'min_len': 0, 'max_len': 0, 'min_len_hit': 0, 'perfect_goal_hit': 0},
            'W':  {'hits': hit_counter['W'],  'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list': [],'min_len': 0, 'max_len': 0, 'min_len_hit': 0, 'perfect_goal_hit': 0},
            'E':  {'hits': hit_counter['E'],  'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list': [],'min_len': 0, 'max_len': 0, 'min_len_hit': 0, 'perfect_goal_hit': 0},
            'SW': {'hits': hit_counter['SW'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list': [],'min_len': 0, 'max_len': 0, 'min_len_hit': 0, 'perfect_goal_hit': 0},
            'SE': {'hits': hit_counter['SE'], 'avgCost': 0, 'avgLen': 0, 'totalCost': 0, 'totalLen': 0, 'len_list': [],'min_len': 0, 'max_len': 0, 'min_len_hit': 0, 'perfect_goal_hit': 0},
        }

        # Removendo direções inválidas
        for direction in ['NW', 'NE', 'W', 'E', 'SW', 'SE']:
            if not self.validate_direction(direction):
                del next_directions_data[direction]

        #Preenchendo dados de `next_directions_data`
        for evaluation in path_evaluation:
            if evaluation['next_step'] in hit_counter:
                evaluation['hits'] = hit_counter[evaluation['next_step']]
            if evaluation['next_step'] in next_directions_data:
                next_step = next_directions_data[evaluation['next_step']]
                next_step['totalCost'] += evaluation['path_cost']
                next_step['totalLen'] += evaluation['path_len']
                next_step['len_list'].append(evaluation['path_len'])
                next_step['min_len'] = min(next_step['len_list'])
                next_step['max_len'] = max(next_step['len_list'])
                next_step['min_len_hit'] = GatoFujao.count(next_step['len_list'], [next_step['min_len']])
                next_step['perfect_goal_hit'] = GatoFujao.count(next_step['len_list'],[next_step['min_len'] + 2, next_step['min_len'] + 3])

        elems_to_remove = set()

        # Preenchendo dados de `next_directions_data` e calculando scores
        for key, hit_result in next_directions_data.items():
            if hit_result['totalLen'] > 0:
                hit_result['avgCost'] = float(hit_result['totalCost']) / float(hit_result['hits'])
            if hit_result['totalLen'] > 0:
                hit_result['avgLen'] = sorted(hit_result['len_list'])[len(hit_result['len_list']) // 2]


            #Peso dos elementos que compõe a score
            path_len_mult = 1
            difficulty_mult = 0.1
            hits_mult = 0
            min_hit_mult = 2
            perfect_goal_hit_mult = 0


            # Score calculation
            goals = self.goals
            p1 = (1 / hit_result['avgLen'] if hit_result['avgLen'] > 0 else 0) * path_len_mult
            p2 = (1 / hit_result['avgCost'] if hit_result['avgCost'] > 0 else 0) * difficulty_mult
            p3 = (hit_result['hits'] / (len(goals) * amount_cats) if len(goals) > 0 else 0) * hits_mult
            p4 = (hit_result['min_len_hit'] / len(goals) if len(goals) > 0 else 0) * min_hit_mult
            p5 = (hit_result['perfect_goal_hit'] / len(goals) if len(goals) > 0 else 0) * perfect_goal_hit_mult

            score = p1 + p2 + p3 + p4 + p5

            if self.DEBUG:
                print(hit_result['avgLen'])
                print(
                    'len: {:.2f} | cost {:.2f} | hits {:.2f} | min_len {:.2f} | perfect_dist {:.2f}| SUM {:.2f}'.format(
                        p1, p2, p3, p4, p5, score))

            hit_result['score'] = score

            #Removendo elementos que tem score 0
            #if hit_result['score'] == 0:
            #    elems_to_remove.add(key)

        #for key in elems_to_remove:
        #    pass
        #    next_directions_data.pop(key)

        return next_directions_data


    def choose_direction_by_score(self, scores):
        return max(list(scores.items()), key=lambda item: float(item[1]['score']))[0]

    def escape(self):
        self.create_grid()
        cat_cell = self.grid.get_cell(self.cat)


        # Cat is trapped
        if self.is_cat_trapped(cat_cell):
            sys.exit()

        #Go for it
        goforit = self.go_for_it(cat_cell)
        if goforit[0]:
            print(goforit[1])
            return

        # Go for it II
        goforit2 = self.go_for_it_2(cat_cell)
        if goforit2[0]:
            print(goforit2[1])
            return

        self.grid.assign_difficulty(3)

        if self.DEBUG:
            print(self.grid.show_difficulties())

        #Creating cats
        cats = self.create_cats()

        #Evaluating all paths
        evaluations = self.evaluate_all_paths(cats)


        # Calculating score and score data
        hits = self.calc_score(evaluations, len(cats))


        #Choosing the direction with best score
        #if len(list(hits.items())) == 0:

        walk_to = self.choose_direction_by_score(hits)
        print(walk_to)


cat = eval(sys.argv[1])
walls = set(eval(sys.argv[2]))
goals = set(eval(sys.argv[3]))

cat = GatoFujao(cat=cat, walls=walls, goals=goals)
cat.escape()

