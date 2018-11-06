from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.catshelper.DistanceCalculator import DistanceTypes

from util.Helper import Help

#DO NOT REUSE

class ScoreCalculator:
    def __init__(self, walls, goals, cat):
        self.walls = set(walls)
        self.goals = set(goals)
        self.cat = cat

        self.grid = Grid(goals, walls, (5, 5), rows=11, cols=11)

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


    def all_positions(self):
        return [(i,j) for i in range(0,11) for j in range(0,11)]


    def metadata(self):

        cell_set = self.all_positions()

        process_data = {
        'data':{},
        'normalization':{
            'min_hits_min': 0,
            'min_hits_max': 0,

            'path_len_min': 0,
            'path_len_max': 0,

            'cat_dist_min' : 0,
            'cat_dist_max' : 0,

            'leads_to_goals_min': 0,
            'leads_to_goals_max': 0,

            'in_diamond_min': 0,
            'in_diamond_max': 0,

            'catcher_panic_min': 0,
            'catcher_panic_max': 0,

            'squares_min': 0,
            'squares_max': 0,
            }
        }

        full_path = []
        full_min_hits = []
        full_cat_dist = [1]
        full_lead_to_goal_count = []
        full_is_diamond = [0,1]
        full_catcher_panic = []
        full_squares = []
        full_cat_trapper = [7]
        
        for elem in cell_set:

            local_diff = []
            local_path = []

            if elem in self.walls:
                continue

            for goal in [goal for goal in self.goals if goal not in self.walls]:

                self.cat_obj.reset()
                self.cat_obj.find_path(goal, elem)
                if self.cat_obj.path is None:
                    continue
                dist = self.cat_obj.path.get_distance()
                diff = self.cat_obj.path.get_difficulty()

                if not elem in Help.valid_goals(goals=self.goals, walls=self.walls):
                    local_path.append(dist)

                local_diff.append(diff)



            # Aqui local path e diff tem a lista de dados do nó para cada goal
            #local_path.sort()
            #local_diff.sort()

            if len(local_path) == 0:
                local_path.append(0)

            min_hits_count = Help.count(local_path, [min(local_path)])

            if elem not in process_data['data']:
                process_data['data'][elem] = {}


            process_data['data'][elem]['min_hits'] = min_hits_count
            process_data['data'][elem]['path_len'] = Help.minimum_average(local_path, 5)

            lead_to_goals = Help.count_lead_goals(cell=elem, cat=self.cat, goals=self.goals, walls=self.walls)

            process_data['data'][elem]['leads_to_goals'] = lead_to_goals
            in_diamond=Help.in_diamond(elem)
            process_data['data'][elem]['in_diamond'] = in_diamond

            process_data['data'][elem]['catcher_panic'] = 0

            if elem in Help.valid_goals(goals=self.goals, walls=self.walls) and \
                            self.cat in Help.neibs_pos(elem, self.walls, self.cat, False):
                process_data['data'][elem]['catcher_panic'] = 1

            process_data['data'][elem]['squares'] = 0

            if elem[0] % 3 == 0:
                process_data['data'][elem]['squares'] += 5
            if elem[1] % 3 == 0:
                process_data['data'][elem]['squares'] += 5

            if elem[0] % 2 == 0:
                process_data['data'][elem]['squares'] += 1
            if elem[1] % 2 == 0:
                process_data['data'][elem]['squares'] += 1

            full_squares.append(process_data['data'][elem]['squares'])

            walkables = 0
            n = set(Help.neibs_pos(elem, self.walls, self.cat, exclude_non_walkable = False))

            if self.cat in n:
                exitforcat = len(Help.neibs_pos(self.cat, self.walls, self.cat, exclude_non_walkable=True))

                if exitforcat == 1:
                    walkables = 7

                elif exitforcat == 2:
                    walkables = 2

                elif exitforcat == 3:
                    walkables = 1



            process_data['data'][elem]['cat_trap'] = walkables
            full_cat_trapper.append(walkables)

            full_path.extend( local_path[ 0:min(len(local_path), 3)] )
            full_min_hits.append( min_hits_count )
            full_lead_to_goal_count.append(lead_to_goals)
            full_is_diamond.append(in_diamond)
            full_catcher_panic.append(process_data['data'][elem]['catcher_panic'])

        for position, data in process_data['data'].items():
            self.cat_obj.reset()
            # goal_cell = self.grid.get_cell(goal)
            self.cat_obj.find_path(position, self.cat)

            if self.cat_obj.path is None:
                data['cat_dist'] = 20
                full_cat_dist.append(data['cat_dist'])
                continue

            dist = self.cat_obj.path.get_distance()
            data['cat_dist'] = dist
            full_cat_dist.append(data['cat_dist'])

        process_data['normalization']['min_hits_min']  =  min(full_min_hits)
        process_data['normalization']['min_hits_max']  =  max(full_min_hits)

        process_data['normalization']['path_len_min']  =  min(full_path)
        process_data['normalization']['path_len_max']  =  max(full_path)

        process_data['normalization']['cat_dist_min']  = min(full_cat_dist)
        process_data['normalization']['cat_dist_max']  = max(full_cat_dist)

        process_data['normalization']['leads_to_goals_min'] = min(full_lead_to_goal_count)
        process_data['normalization']['leads_to_goals_max'] = max(full_lead_to_goal_count)

        process_data['normalization']['in_diamond_min'] = min(full_is_diamond)
        process_data['normalization']['in_diamond_max'] = max(full_is_diamond)

        process_data['normalization']['catcher_panic_min'] = min(full_catcher_panic)
        process_data['normalization']['catcher_panic_max'] = max(full_catcher_panic)

        process_data['normalization']['squares_min'] = min(full_squares)
        process_data['normalization']['squares_max'] = max(full_squares)

        process_data['normalization']['cat_trap_min'] = min(full_cat_trapper)
        process_data['normalization']['cat_trap_max'] = max(full_cat_trapper)

        return process_data


    def scores(self, score_range = (0,2)):

        md = self.metadata()
        self.score_range = score_range

        norm = md['normalization']
        elems = md['data']

        answer = {}

        for elem, data in elems.items():

            s1_path_len = Help.normalize(
                data['path_len'],
                norm['path_len_min'],
                norm['path_len_max'],
                reversed=True,
            )

            s2_min_hits = Help.normalize(
                data['min_hits'],
                norm['min_hits_min'],
                norm['min_hits_max'],
                reversed=False,
            )

            s3_cat_dist = Help.normalize(
                data['cat_dist'],
                norm['cat_dist_min'],
                norm['cat_dist_max'],
                reversed=True,
            )

            s4_lead_to_goal = Help.normalize(
                data['leads_to_goals'],
                norm['leads_to_goals_min'],
                norm['leads_to_goals_max'],
                reversed=False,
            )

            s5_in_diamond = Help.normalize(
                data['in_diamond'],
                norm['in_diamond_min'],
                norm['in_diamond_max'],
                reversed=False,
            )

            s6_catcher_panic = Help.normalize(
                data['catcher_panic'],
                norm['catcher_panic_min'],
                norm['catcher_panic_max'],
                reversed=False,
            )

            s7_squares = Help.normalize(
                data['squares'],
                norm['squares_min'],
                norm['squares_max'],
                reversed=False,
            )

            s8_cat_trap = Help.normalize(
                data['cat_trap'],
                norm['cat_trap_min'],
                norm['cat_trap_max'],
                reversed=False,
            )

            score = ( s3_cat_dist       * 0        ) + \
                    ( s2_min_hits       * 0        ) + \
                    ( s4_lead_to_goal   * 0        ) + \
                    ( s5_in_diamond     * 1         ) + \
                    ( s6_catcher_panic  * 0        ) + \
                    ( s7_squares        * 0         ) + \
                    ( s8_cat_trap       * 0         ) + \
                    ( (1+s3_cat_dist*4) * (1+s4_lead_to_goal) * 0 )

            if score == -0.0:
                score = 0.0

            cell = self.grid.get_cell(elem)
            cell.set_score(score)


            answer[(elem, cell)] = {
                's1_path_len':s1_path_len,
                's2_min_hits':s2_min_hits,
                's3_cat_dist':s3_cat_dist,
                'score' : score,
            }

        return answer
