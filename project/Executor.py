from cats.CatFather import CatFather
from Grid import Grid
from cats.catshelper.DistanceCalculator import DistanceTypes, Distance2DCalculator
from operator import attrgetter
from cats.CatFather import Solution

class Pathfind:
    def __init__(self, cats : [CatFather], grid : Grid, minimum):
        self.cats = cats
        self.grid = grid
        self.minimum = minimum
        self.best_cases = []
        self.start_cell = grid.get_start_cell()
        self.exit_cells = grid.get_exit_cells()
        self.exit_cells = sorted(self.exit_cells, key=lambda x : Distance2DCalculator(DistanceTypes.HEX).distCell(self.start_cell, x),
                            reverse=False)

    def get_all_runs(self):
        answer = {}
        for cat in self.cats: #Para cada um dos gatos (na ordem em que foram enviados)
            for goal in self.exit_cells: #Para cada saída no labirinto
                cat.end = goal
                cat.reset()
                result = cat.find_path()

                answer['{} -> ({}x{})'.format(cat, goal.xpos, goal.ypos)] = {
                    'cat':cat,
                    'cat_name':str(cat),
                    'path':cat.path,
                    'path_len': cat.path.distance,
                    'path_str': cat.path.get_directions_str(),
                    'path_chars': cat.path.get_directions(),
                    'result':result,
                    'exit':(goal.xpos, goal.ypos)
                }
        return answer

    def get_best_run(self):
        answer = {}
        for cat in self.cats:  # Para cada um dos gatos (na ordem em que foram enviados)
            for goal in self.exit_cells:  # Para cada saída no labirinto
                cat.end = goal
                cat.reset()
                result = cat.find_path()
                if result == Solution.FINDED:
                    if cat.path.distance == self.minimum:

                        #Retornará a primeiro resultado mínimo
                        return {
                                    'cat': cat,
                                    'cat_name': str(cat),
                                    'path': cat.path,
                                    'path_len': cat.path.distance,
                                    'path_str': cat.path.get_directions_str(),
                                    'path_chars': cat.path.get_directions(),
                                    'result': result,
                                    'exit': (goal.xpos, goal.ypos)
                                }

                    else:
                        answer['{} -> ({}x{})'.format(cat, goal.xpos, goal.ypos)] = {
                                    'cat': cat,
                                    'cat_name': str(cat),
                                    'path': cat.path,
                                    'path_len': cat.path.distance,
                                    'path_str': cat.path.get_directions_str(),
                                    'path_chars': cat.path.get_directions(),
                                    'result': result,
                                    'exit': (goal.xpos, goal.ypos)
                                }

        return min(answer, key=lambda elem : elem['path_len'])

    def execute_printing(self):
        for cat in self.cats:
            print('-' * 100)
            print('CAT: {}'.format(cat))
            print('MINIMUM PATH SIZE: {}'.format(self.minimum))

            dirs=[]
            exit_counter = 0

            for exit_cell in self.exit_cells:
                cat.end = exit_cell
                cat.reset()
                cat.find_path()
                dirs.append(cat.path)

                print('....')
                print(cat)
                print('PATH SIZE: {}'.format(cat.path.distance))
                print(self.grid.show(cat))
                print('DIRECTIONS')
                print(cat.path.get_directions_str().replace('\n', ' '))
                exit_counter += 1
            print('-' * 50 + ' [BEST DIRECTIONS] ' + '-' * 50)

            min_distance = min(dirs, key=attrgetter('distance')).get_distance()
            min_directions = min(dirs, key=attrgetter('distance')).get_directions_str()

            print(min_directions.replace('\n', ' '))
            print('Size: {}'.format(min_distance))

            self.best_cases.append((cat, min_distance))

            print('-' * 100)
        print('BEST CASES')
        print(self.best_cases)

    def compare_cats(self):
        for cat in self.cats:
            dirs=[]
            for exit_cell in self.exit_cells:
                cat.end = exit_cell
                cat.reset()
                result = cat.find_path()

                if result == Solution.FINDED:
                    dirs.append(cat.path)

            min_distance = min(dirs, key=attrgetter('distance')).get_distance()
            self.best_cases.append((cat, min_distance))

        answer = []
        for cat, dist in self.best_cases:
            answer.append('{},{},'.format(str(cat), dist))
        answer.append('min,{}\n'.format(self.minimum))
        return ''.join(answer)
