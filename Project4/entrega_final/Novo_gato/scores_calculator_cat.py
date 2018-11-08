from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.catshelper.DistanceCalculator import DistanceTypes
from collections import deque


class CalculationHelper:
    @staticmethod
    def valid_goals(goals, walls, cat_pos):
        return [goal for goal in goals if goal not in walls and goal != cat_pos]

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

    @staticmethod
    def average(lst) -> float:
        return sum(lst) / float(len(lst))

    @staticmethod
    def minimum_elements(lst, required_elements=1) -> float:
        lst.sort()
        return lst[0:min([len(lst), required_elements])]

    @staticmethod
    def minimum_average(lst, max_elements=1) -> float:
        true_elems = CalculationHelper.minimum_elements(lst, max_elements)
        if len(true_elems) == 0:
            return 0
        return sum(true_elems) / float(len(true_elems))


class ScoreCalculator:
    def __init__(self, walls, goals, diff_spred_steps = 3, cat_pos = (5,5)):
        self.walls = walls
        self.goals = goals
        self.diff_spread = diff_spred_steps

        self.cat_pos = cat_pos

        self.grid = Grid(goals, walls, cat_pos, rows=11, cols=11)
        self.grid.assign_difficulty(diff_spred_steps)

        self.dist = DistanceTypes.HEX

        astar_cat = AstarCat(
            max_iterations=200,
            grid=self.grid,
            gWeight=1,
            hWeight=1,
            fWeight=1,
            distanceType=self.dist
        )
        self.cat_obj = astar_cat
        self.score_range = (0, 6)


    def positions_around(self, pos):
        cell = self.grid.get_cell(pos)
        answer = []
        for neib in cell.neibs:
            answer.append(neib.pos)
        return answer

    def spread_postions(self, pos, iterations):
        cell = self.grid.get_cell(pos)
        neibs_to_look = deque(cell)
        answer = set()
        iteration = 0

        if iteration < iterations:
            for cell in neibs_to_look.popleft().pos:
                for neib in cell.neibs:
                    if neib not in neibs_to_look:
                        iteration += 1
                        neibs_to_look.append(neib)
                        answer.add(neib)
        return list(answer)

    def all_positions(self):
        return [(i,j) for i in range(0,11) for j in range(0,11)]


    def metadata(self, cell_set = None):

        if cell_set is None:
            cell_set = self.all_positions()
        if cell_set == 'around_cat':
            cell_set = self.positions_around(self.cat_pos)

        process_data = {
        'data':{},
        'normalization':{
            'min_hits_min': 0,
            'min_hits_max': 0,

            'path_len_min': 0,
            'path_len_max': 0,

            'path_diff_min': 0,
            'path_diff_max': 0,

            'local_dif_min': 0,
            'local_dif_max': 0,
            }
        }

        full_diff = []
        full_path = []
        full_min_hits = []
        full_local_diff = []
        full_near_goal = [0]


        for elem in cell_set:

            local_diff = []
            local_path = []

            if elem in self.walls:
                continue
            current_cell = self.grid.get_cell(elem)

            for goal in [goal for goal in self.goals if goal not in self.walls]:
                self.cat_obj.reset()
                #goal_cell = self.grid.get_cell(goal)
                self.cat_obj.find_path(goal, elem)
                if self.cat_obj.path is None:
                    continue
                dist = self.cat_obj.path.get_distance()
                diff = self.cat_obj.path.get_difficulty()
                local_path.append(dist)
                local_diff.append(diff)
            # Aqui local path e diff tem a lista de dados do nó para cada goal
            local_path.sort()
            local_diff.sort()

            if len(local_path) == 0:
                local_path.append(0)
            min_hits_count = CalculationHelper.count(local_path, [min(local_path)])

            if elem not in process_data['data']:
                process_data['data'][elem] = {}

            if 'near_goal' not in process_data['data'][elem]:
                process_data['data'][elem]['near_goal'] = 0

            if current_cell.is_goal:
                process_data['data'][elem]['near_goal'] += 100
                full_near_goal.append(process_data['data'][elem]['near_goal'])

            process_data['data'][elem]['min_hits'] = min_hits_count
            process_data['data'][elem]['path_len'] = CalculationHelper.minimum_average(local_path, 5)
            process_data['data'][elem]['path_diff'] = CalculationHelper.minimum_average(local_diff, 5)
            process_data['data'][elem]['local_dif'] = self.grid.get_cell(elem).difficulty
            full_path.extend( local_path[ 0:min(len(local_path), 3)] )
            full_diff.extend( local_diff[ 0:min(len(local_diff), 3)] )
            full_min_hits.append( min_hits_count )
            full_local_diff.append(self.grid.get_cell(elem).difficulty)

        for position, data in process_data['data'].items():
            cell = self.grid.get_cell(position)
            goals_count = 0
            for neib in cell.neibs:
                if neib.is_goal and not neib.is_wall:
                    goals_count += 1

            data['near_goal'] += goals_count * 10
            full_near_goal.append(data['near_goal'] )


        process_data['normalization']['min_hits_min']  =  min(full_min_hits)
        process_data['normalization']['min_hits_max']  =  max(full_min_hits)

        process_data['normalization']['path_len_min']  =  min(full_path)
        process_data['normalization']['path_len_max']  =  max(full_path)

        process_data['normalization']['path_diff_min'] =  min(full_diff)
        process_data['normalization']['path_diff_max'] =  max(full_diff)

        process_data['normalization']['local_dif_min'] =  min(full_local_diff)
        process_data['normalization']['local_dif_max'] =  max(full_local_diff)

        process_data['normalization']['near_goal_min'] = min(full_near_goal)
        process_data['normalization']['near_goal_max'] = max(full_near_goal)
        return process_data


    def scores(self, reverses = (True, False, True, True, False), score_func = None, score_range = (0,5), cell_set = None):

        md = self.metadata(cell_set)
        self.score_range = score_range


        norm = md['normalization']
        elems = md['data']

        answer = {}

        for elem, data in elems.items():

            s1_pathlen = CalculationHelper.normalize(
                data['path_len'],
                norm['path_len_min'],
                norm['path_len_max'],
                reversed=reverses[0],
            )

            s2_min_hits = CalculationHelper.normalize(
                data['min_hits'],
                norm['min_hits_min'],
                norm['min_hits_max'],
                reversed=reverses[1],
            )

            s3_path_dif = CalculationHelper.normalize(
                data['path_diff'],
                norm['path_diff_min'],
                norm['path_diff_max'],
                reversed=reverses[2],
            )

            s4_local_dif = CalculationHelper.normalize(
                data['local_dif'],
                norm['local_dif_min'],
                norm['local_dif_max'],
                reversed=reverses[3],
            )

            s5_near_goal = CalculationHelper.normalize(
                data['near_goal'],
                norm['near_goal_min'],
                norm['near_goal_max'],
                reversed=reverses[4],
            )


            if score_func is None:
                #Default score calculation
                score = (s5_near_goal * 3) + (s1_pathlen*2) + s2_min_hits
            else:
                #Calculation by the sended lambda/function (not the best option...)
                score = score_func(s1_pathlen, s2_min_hits, s3_path_dif, s4_local_dif, s5_near_goal)

            if elem == (5,5):
                score *= 0.5

            if elem in [(5,4),(4,5),(4,6),(5,6),(6,6),(6,5)]:
                score *= 0.8



            cell = self.grid.get_cell(elem)
            cell.set_score(score)


            answer[(elem, cell)] = {
                's1_pathlen':s1_pathlen,
                's2_min_hits':s2_min_hits,
                's3_path_dif':s3_path_dif,
                's4_local_dif':s4_local_dif,
                'score' : score,
            }

        return answer
