import sys
import random
import math
from random import shuffle
from collections import deque
import math


cat = eval(sys.argv[1])
blocks = eval(sys.argv[2])
exits = eval(sys.argv[3])

class False_log:
    def write(self, str):
        pass

    def close(self):
        pass

log = open('logfile.txt', 'a+')

#log = False_log()

log.write('cat: {}\n'.format(cat))
log.write('blocks: {}\n'.format(blocks))
log.write('exits: {}\n'.format(exits))


class Catcher:
    def __init__(self, cat_pos, walls, goals):
        self.cat_pos = tuple(cat_pos)
        self.walls = walls
        self.goals = goals

        pass

    def catch_them_all(self):
        solutions = []

        #Lista de métodos com diferentes formas de capturar o gato, executados na ordem que aparecem na lista
        #Caso retorne None ou lance exceção, passa para o próximo método da lista
        #O nome colocado vai ser gravado no arquivo de log (ou não)

        solutions.append([self.catch_trapped_cat,           'catchTrapped'])
        #solutions.append([self.close_cat_is_near_exit,      'catNearExit'])
        solutions.append([self.close_cat_is_near_exit_pathdist, 'catNearExitPathDist'])
        solutions.append([self.catch_almost_trapped_cat,    'catchAlmostTrapped'])
        solutions.append([self.heuristic_closer,            'heuristicCloser'])
        solutions.append([self.close_around_cat,            'close_around_cat'])
        solutions.append([self.generate_random_around_cat,  'randomAroundCat'])
        #solutions.append([self.close_nearest_exit,          'closeNearestExit'])
        solutions.append([self.close_path_nearest_exit,          'closePathNearestExit'])
        solutions.append([self.generate_random_position,    'closeRandom'])


        for solution in solutions:
            log.write('WALLS: {}\n'.format(self.walls))

            try:
                result = solution[0]()
                if self.evaluate_solution(result, solution[1]):
                    log.write('\tRETURNING : `{}`\n\n'.format(result))
                    return result
            except Exception as ex:
                log.write('EXCEPTION {}\n'.format(str(ex)))
                pass

    def evaluate_solution(self, solution, solution_name = 'NoNameSolution'):
        '''
        Método para avaliar a qualidade de uma solução (uma segunda camada se segurança para conferir se a posição é válida)
        '''


        log.write('{} CHOOSED xy:`{}`\n'.format(solution_name, str(solution)))
        return solution is not None

    def close_cat_is_near_exit_pathdist(self):
        if len([elem for elem in self.goals if elem not in self.walls]) > 0:
            nearest_exits = self.get_exits_path_dist()

            if nearest_exits is None:
                return None

            nearest_exits.sort(key=lambda elem: elem['dist'])
            nearest = nearest_exits[0]

            log.write('MIN DISTANCES\n')
            log.write(str(nearest_exits))
            log.write('\n')

            if nearest['dist'] <= 4:
                return nearest['pos']
            else:
                return None


    def close_cat_is_near_exit(self):
        """
        Fecha as células de saída caso o gato esteja próximo delas
        """

        if len([elem for elem in self.goals if elem not in self.walls]) > 0:
            #nearest_exits = self.get_exits_path_dist()
            nearest_exits = self.get_exits_dist()

            if nearest_exits is None:
                return None

            #Pegando nearest por MIN
            #nearest = min(nearest_exits, key=lambda elem: elem['dist'])
            #Pegando nearest por SORT
            nearest_exits.sort(key=lambda elem: elem['dist'])
            nearest = nearest_exits[0]
            mins = []

            for near_candidate in nearest_exits:
                if near_candidate['dist'] in [nearest['dist'], nearest['dist'] - 1]:
                    mins.append(near_candidate)
                else:
                    break

            nearest = random.choice(mins)

            #Pegar os vizinhos da saída mais próxima
            neibours = self.get_neibours_position(nearest['pos'], exclude_non_walkable=True)

            goals_around = 0
            walls_around = 0

            #Contando saídas ao redor
            for neibour in neibours:
                goals_around += 1 if neibour in self.goals and neibour not in self.walls else 0
                walls_around += 1 if neibour in self.walls else 0

            #Se a saída já estiver bloqueada, não bloquear
            #if walls_around >= len(neibours):
            #    return None

            if nearest['dist'] <= 5:
                return nearest['pos']
            return None

    def catch_trapped_cat(self):
        '''
        Pega o gato se ele estiver entrando em um ponto sem saída
        '''
        neibours = self.get_neibours_position(self.cat_pos, exclude_non_walkable=True)
        if len(neibours) == 1:  # Se houver apenas um vizinho válido
            return neibours[0]
        return None

    def catch_almost_trapped_cat(self):
        '''
        Pega o gato se ele estiver entrando em um ponto sem saída
        '''
        neibours = self.get_neibours_position(self.cat_pos, exclude_non_walkable=True)
        answer = None
        if len(neibours) <= 3: # Se houverem só dois ou um vizinho válido
            # Feche o vizinho com mais casas abertas ao redor
            max_opened = 0
            neibour_choosed = neibours[0]
            for neibour in neibours:
                neibour_neibours = self.get_neibours_position(neibour, exclude_non_walkable=True)
                if len(neibour_neibours) > max_opened:
                    max_opened = len(neibour_neibours)
                    neibour_choosed = neibour
            return neibour_choosed
        return answer

    def heuristic_closer(self):
        '''
        Fecha células com base em alguma heurística - atribuindo um score para cada célula
        '''

        grid = [[
                    {'row':j, 'col':i,
                     'is_wall': (j,i) in self.walls,
                     'is_cat': (j,i) == self.cat_pos,
                     'is_goal': (j,i) in self.goals,
                     'is_border' : i in [0, 10] or j in [0, 10],
                     'cant_close' : (j,i) in self.walls or (j,i) == self.cat_pos,
                     'score' : 0
                     }
                    for i in range(11)] for j in range(11)]

        # Calculate Score
        #Score maior se:
            #1. perto do gato
            #2. é saída
            #3. vizinho de saída
            #4. perto de outros bloqueios

        grater_score = 1
        grater_score_element = None

        for row in grid:
            for elem in row:

                if not elem['cant_close']:
                    neibours = self.get_neibours(grid, (elem['row'], elem['col']), False)

                    score = 0
                    walls_around = 0
                    borders_around = 0
                    opposites_positives = 0
                    
                    for direction in ["NW", "NE", "W" , "E" , "SW", "SE"]:
                        opposite = self.get_opposite(grid, (elem['row'], elem['col']), direction)
                        if opposite is not None and opposite['is_wall']:
                            opposites_positives += 1
                        elif opposite is None:
                            opposites_positives += 1

                    for neibour in neibours:
                        if neibour['is_wall']: walls_around += 1
                        if neibour['is_border']:borders_around += 1

                    if walls_around >= len(neibours):
                        continue

                    #cat_distance = Distance().hex_distance((elem['row'], elem['col']), self.cat_pos)
                    cat_distance = self.path_distance( (elem['row'], elem['col']), self.cat_pos, max_dist=20)

                    #center_distance = Distance().hex_distance((elem['row'], elem['col']), (5,5)) + 1

                    #if cat_distance == 1:
                    #    cat_distance = 2

                    inverse_cat_distance = (1/(cat_distance + 0.1) ) * 10
                    inverse_walls_around = (1 /(walls_around + 0.1))
                    #center_distance = int((1 / (center_distance + 0.1) ) * 10)
                    # Se preocupa em prender o gato, não de evitar que chegue numa saída


                    #Diagonais
                    #score += 2 if \
                    #    elem['row'] == elem['col'] or \
                    #    elem['row'] == elem['col'] or \
                    #    elem['row'] + elem['col'] == 10 or \
                    #    elem['row'] + elem['col'] == 9 \
                    #else 0


                    #Cruz
                    #score += 2 if \
                    #    elem['row'] == 5 or\
                    #    elem['col'] == 5 \
                    #else 0
                    #
                    #if score == 14: score = 7

                    #score += cat_distance

                    #score += int (center_distance / 3)
                    #score += int(walls_around/3)

                    score += 10 if opposites_positives < 4 else 0

                    if cat_distance == 3:
                        score += 15
                    if cat_distance == 2:
                        score += 30
                    if cat_distance == 1:
                        score += 20

                    score += inverse_cat_distance * 2
                    score += inverse_walls_around


                    elem['score'] = score

                    if elem['score'] > grater_score or (elem['score'] == grater_score and random.randint(0,5) == 0)\
                            and elem['score'] > 0:
                        grater_score = elem['score']
                        grater_score_element = elem


        count = 1
        for row in grid:
            if count == -1:
                log.write('   ')
            for elem in row:
                count *= -1
                log.write('[{:^2}]'.format(int(elem['score'])))
            log.write('\n')
        log.write('\n')

        if grater_score_element is None:
            return None
        else:
            return grater_score_element['row'], grater_score_element['col']

    def generate_random_position(self):
        '''
        Fecha uma posição aleatória no tabuleiro
        '''
        used = self.walls.copy() + [self.cat_pos]
        candidate = (random.randint(0, 10), random.randint(0, 10))
        while candidate in used:
            candidate = (random.randint(0, 10), random.randint(0, 10))
        return candidate


    def generate_random_around_cat(self):
        '''
        Fecha casas imediatamente ao redor do gato, de maneira aleatória
        '''
        cat = self.cat_pos
        candidates = self.get_candidate_neibours(cat)

        used = self.walls.copy()
        used.append(cat)
        candidates = [elem for elem in candidates if elem[0] > 0 and elem[0] <= 10 and elem[1] > 0 and elem[1] <= 10 and elem not in used]
        candidate = random.choice(candidates)
        return candidate


    def close_around_cat(self):
        '''
        Fecha casas imediatamente ao redor do gato, dando prioridade a casas que já não estão cercadas por paredes        
        '''
        cat = self.cat_pos
        candidates = self.get_candidate_neibours(cat)

        used = self.walls.copy()
        used.append(cat)
        candidates = [elem for elem in candidates if elem[0] > 0 and elem[0] <= 10 and elem[1] > 0 and elem[1] <= 10 and elem not in used]

        if len(candidates) == 0:
            return None

        evaluation = {}
        for candidate in candidates:
            evaluation[candidate] = {'score': 0}
            neibors = self.get_neibours_position(rowcol=candidate, exclude_non_walkable=False)
            for neibor in neibors:
                if neibor in self.walls:
                    evaluation[candidate]['score'] += 1

        choice = max(evaluation, key=lambda elem : elem['score'])
        if choice['score'] > 0:
            return list(choice.keys())[0]
        else:
            return random.choice(candidates)

    def close_nearest_exit(self):
        '''
        Fecha sempre a saída mais próxima do gato
        '''
        menor = 10000
        closestExit = self.generate_random_position()
        valid_elems = [elem for elem in self.goals if elem not in self.walls and elem is not self.cat_pos]

        if len(valid_elems) == 0:
            return None

        for exit in valid_elems:
            distance = Distance().hex_distance(exit, self.cat_pos)
            if distance < menor:
                menor = distance
                closestExit = exit
        return closestExit

    def close_path_nearest_exit(self):
        '''
        Fecha sempre a saída mais próxima do gato
        '''
        closestExit = self.generate_random_position()
        valid_elems = [elem for elem in self.goals if elem not in self.walls and elem is not self.cat_pos]

        if len(valid_elems) == 0:
            return None
        menor = 10000
        for goal in valid_elems:
            distance = self.path_distance(goal, self.cat_pos)
            if distance < menor:
                menor = distance
                closestExit = goal
        return closestExit


    # ---  HELPER METHODS ---
    def get_exits_path_dist(self):
        '''
        Obtém as saídas mais próximas do gato        
        '''
        answer = []
        max_distance = 500
        for goal in [elem for elem in self.goals if elem not in self.walls]:
            distance = self.path_distance(goal, self.cat_pos)

            log.write('PATH DISTANCE FROM {} TO {} IS {}\n'.format(goal, self.cat_pos, distance))

            answer.append({'pos': goal, 'dist': distance})
        return answer


    def get_exits_dist(self):
        '''
        Obtém as saídas mais próximas do gato
        '''
        answer = []
        for goal in [elem for elem in self.goals if elem not in self.walls]:
            distance = Distance().hex_distance(goal, self.cat_pos)
            answer.append({'pos': goal, 'dist': distance})
        return answer
    
    
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

    def get_neibours_position(self, rowcol, exclude_non_walkable = True):
        '''
        Obtém a posição de vizinhos válidos
        '''
        candidates = self.get_candidate_neibours(rowcol)
        if exclude_non_walkable:
            used = self.walls.copy()
            used.append(cat)
            candidates = [elem for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10 and elem not in used]
        else:
            candidates = [elem for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10]

        return candidates

    def get_neibours(self, grid, rowcol, exclude_non_walkable = True):
        '''
        Obtém os vizinhos de um elemento do grid
        '''
        candidates = self.get_candidate_neibours(rowcol)
        if exclude_non_walkable:
            used = self.walls.copy()
            used.append(cat)
            candidates = [grid[elem[0]][elem[1]] for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10 and elem not in used]
        else:
            candidates = [grid[elem[0]][elem[1]] for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10]

        return candidates

    def get_opposite_pos(self, rowcol, direction,exclude_non_walkable = True):
        '''
        Recebe uma posição e uma direção e retorna a direção oposta
        '''
        candidates = {
            "NW": [(rowcol[0] - 1, rowcol[1] - 1), (rowcol[0] - 1, rowcol[1])][rowcol[0] % 2],
            "NE": [(rowcol[0] - 1, rowcol[1]), (rowcol[0] - 1, rowcol[1] + 1)][rowcol[0] % 2],
            "W": [(rowcol[0], rowcol[1] - 1), (rowcol[0], rowcol[1] - 1)][rowcol[0] % 2],
            "E": [(rowcol[0], rowcol[1] + 1), (rowcol[0], rowcol[1] + 1)	][rowcol[0] % 2],
            "SW": [(rowcol[0] + 1, rowcol[1] - 1), (rowcol[0] + 1, rowcol[1])		    ][rowcol[0] % 2],
            "SE": [(rowcol[0] + 1, rowcol[1]	) ,	 (rowcol[0] + 1, rowcol[1] + 1)	    ][rowcol[0] % 2],
        }

        opposites = {"NW" : "SE",
                     "NE" : "SW",
                     "W"  : "E",
                     "E"  : "W",
                     "SW" : "NE",
                     "SE" : "NW",
                     }

        candidate = candidates[ opposites[direction] ]

        if candidate[0] >= 0 and candidate[0] <= 10 and candidate[1] >= 0 and candidate[1] <= 10:
            if exclude_non_walkable:
                used = self.walls.copy()
                used.append(cat)
                if candidate not in used:
                    return candidate
            else:
                return candidate
        return None

    def get_opposite(self, grid, rowcol, direction, exclude_non_walkable = True):
        '''
        Recebe uma posição e uma direção e retorna a o elemento do grid na posição oposta
        '''
        opposite_pos = self.get_opposite_pos(rowcol, direction, exclude_non_walkable)

        if opposite_pos is None:
            return None
        else:
            return grid[opposite_pos[0]][opposite_pos[1]]

    def path_distance(self, pos1, pos2, max_dist = math.inf):
        log.write('PATH DISTANCE RECEIVING {} and {}\n'.format(pos1, pos2))

        log.write('\t\tTEST {}\n'.format((5,5) in self.walls))

        grid = [[
                    {'row': j, 'col': i,
                     'is_wall': (j, i) in self.walls,
                     'is_cat': (j, i) == self.cat_pos,
                     'is_goal': (j, i) in self.goals,
                     'is_border': i in [0, 10] or j in [0, 10],
                     'cant_close': (j, i) in self.walls or (j, i) == self.cat_pos,
                     'score': 0,
                     'previous':None,
                     'neibours': [elem for elem in [
                                    [(j - 1, i - 1),  (j - 1, i)      ]         [j % 2],
                                    [(j - 1, i),      (j - 1, i + 1)  ]         [j % 2],
                                    [(j, i - 1),      (j, i - 1)      ]         [j % 2],
                                    [(j, i + 1),      (j, i + 1)      ]         [j % 2],
                                    [(j + 1, i - 1),  (j + 1, i)      ]         [j % 2],
                                    [(j + 1, i),      (j + 1, i + 1)  ]         [j % 2],
                                    ] if 0 <= elem[0] < 11 and 0 <= elem[1] < 11],
                     }
                    for i in range(11)] for j in range(11)]

        open_set = deque([pos1])
        closed_set = set()

        log.write('is wall {}:{} {}:{}\n'.format(pos1, pos1 in self.walls, pos2, pos2 in self.walls))

        log.write('OPENSET LEN = {}\n'.format(len(open_set)))

        while len(open_set) > 0:
            current = open_set.popleft()


            #log.write('current {} x pos2 {}\n'.format(current, pos2))
            if current == pos2:
                size_counter = 0

                temp = grid[current[0]][current[1]]
                while temp['previous'] is not None:
                    temp = temp['previous']
                    size_counter += 1

                log.write('DISTANCE FOUNDED : {}\n'.format(size_counter))
                return size_counter

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

        #No solution
        return max_dist




class Distance:
    '''
    Cálculo de distâncias em um grid hexagonal
    '''

    @staticmethod
    def axial_to_cube(q, r):
        x = r
        z = q
        y = -x - z
        return (x, y, z)

    def hex_distance(self, p0, p1):
        x0, y0 = p0
        x1, y1 = p1
        first = Distance.axial_to_cube(x0, y0)
        second = Distance.axial_to_cube(x1, y1)
        return Distance.cube_distance(first[0], first[1], first[2], second[0], second[1], second[2])

    @staticmethod
    def cube_distance(ax, ay, az, bx, by, bz):
        return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2


c = Catcher(walls=blocks, goals=exits, cat_pos=cat)
print(c.catch_them_all)
#print(c.path_distance((4,10), (5, 5)))
log.close()

