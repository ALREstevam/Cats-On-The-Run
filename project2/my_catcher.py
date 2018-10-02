import sys
import random
from collections import deque
import math
from HexDistance import Distance


cat = eval(sys.argv[1])
blocks = eval(sys.argv[2])
exits = eval(sys.argv[3])

class Catcher:
    def __init__(self, cat_pos, walls : [], goals : []):
        self.cat_pos = tuple(cat_pos)
        self.walls = set(walls)
        self.goals = set(goals)

    def catch_them_all(self):
        solutions = []

        #Lista de métodos com diferentes formas de capturar o gato, executados na ordem que aparecem na lista
        #Caso retorne None ou lance exceção, passa para o próximo método da lista


        solutions.append([self.catch_trapped_cat,                       'catchTrapped'])
        solutions.append([self.close_stategic,                          'close_stategic'])
        solutions.append([self.close_cat_is_near_exit_pathdist,         'catNearExitPathDist'])
        solutions.append([self.catch_almost_trapped_cat,                'catchAlmostTrapped'])
        solutions.append([self.mess_with_cat,                           'mess_with_cat'])
        solutions.append([self.heuristic_closer,                        'heuristicCloser'])
        solutions.append([self.close_cat_is_near_exit,                  'catNearExit'])
        solutions.append([self.close_nearest_exit,                      'closeNearestExit'])
        solutions.append([self.close_around_cat,                        'close_around_cat'])
        solutions.append([self.generate_random_around_cat,              'randomAroundCat'])
        solutions.append([self.close_path_nearest_exit,                 'closePathNearestExit'])
        solutions.append([self.generate_random_position,                'closeRandom'])


        for solution in solutions:
            try:
                res = solution[0]()
                if self.evaluate_solution(res, solution[1]):
                    return res

            except Exception as ex:
                pass

    def evaluate_solution(self, solution, solution_name = 'NoNameSolution'):
        '''
        Método para avaliar a qualidade de uma solução (uma segunda camada se segurança para conferir se a posição é válida)
        '''
        return solution is not None

    def close_cat_is_near_exit_pathdist(self):
        '''
        Fecha saídas em que o gato está próximo (usando path distance)
        '''
        if len([elem for elem in self.goals if elem not in self.walls]) > 0:
            nearest_exits = self.get_exits_path_dist()

            if nearest_exits is None:
                return None

            nearest_exits.sort(key=lambda elem: elem['dist'])
            nearest_dist = nearest_exits[0]['dist']

            near_goals = []

            for goal in nearest_exits:
                if goal['dist'] == nearest_dist:
                    near_goals.append(goal)

            nearest = random.choice(near_goals)

            if nearest['dist'] <= 4.9:
                return nearest['pos']
            elif nearest['dist'] <= 7:
                goals_count = self.get_valid_goal_neibours(nearest['pos'])
                if goals_count >= 3:
                    return nearest['pos']
            else:
                return None

    def close_stategic(self):
        '''
        Fecha nós que tem muitas saídas ao seu redor
        '''
        for i in range(11):
            for j in range(11):
                elem = (j,i)
                goal_count = self.get_valid_goal_neibours(elem)
                cat_neibours = self.get_valid_goal_neibours(self.cat_pos)
                if goal_count >= 4 and self.path_distance(elem, self.cat_pos) > 4 and elem not in self.walls and elem != self.cat_pos:
                    return elem
                if goal_count >= 2 and self.path_distance(elem, self.cat_pos) == 2\
                        and len(cat_neibours) == 0 and elem not in self.walls and elem != self.cat_pos:
                    return elem
        return None




    def mess_with_cat(self):
        '''
        Fecha posíveis saídas ao redor do gato
        '''
        cat = self.cat_pos

        cat_neib = self.get_neibours_position(cat, exclude_non_walkable=True)

        #Se algum dos vizinhos do gato for uma saída, não tente fechar o gato e sim a saída
        for neib in cat_neib:
            if neib in self.goals:
                return None

        r = cat[0]
        c = cat[1]

        candidates = {}
        if r % 2 == 0:
            candidates = {
                (r, c + 1): [(r - 1, c + 1), (r + 1, c + 1)],
                (r - 1, c): [(r - 1, c + 1), (r, c + 1)],
                (r + 1, c + 1): [(r + 1, c + 1), (r, c + 1)],
                (r - 1, c + 1): [(r, c + 1), (r - 1, c)],
                (r + 1, c + 1): [(r, c + 1), (r + 1, c + 1)],
                (r, c + 1): [(r - 1, c), (r + 1, c + 1)],
            }
        else:
            candidates = {
                (r, c + 1): [(r - 1, c), (r + 1, c)],
                (r - 1, c + 1): [(r - 1, c), (r, c + 1)],
                (r + 1, c + 1): [(r + 1, c), (r, c + 1)],
                (r - 1, c): [(r, c + 1), (r - 1, c + 1)],
                (r + 1, c): [(r, c + 1), (r + 1, c + 1)],
                (r, c + 1): [(r + 1, c + 1), (r - 1, c + 1)],
            }


        possibilities = []
        for to_close, match in candidates.items():
            el1 = match[0]
            el2 = match[1]

            fisrt_match = el1 in self.walls  or el1[0] < 0 or el1[1] < 0 or el1[0] > 10 or el1[1] > 10
            second_match = el2 in self.walls or el2[0] < 0 or el2[1] < 0 or el2[0] > 10 or el2[1] > 10

            to_close_neibours = self.get_neibours_position(to_close, exclude_non_walkable=True)

            if fisrt_match and second_match \
                    and to_close[0] >= 0 and to_close[1] >= 0 and to_close[0] <= 10 and to_close[1] <= 10\
                    and to_close not in self.walls\
                    and to_close != self.cat_pos\
                    and len(to_close_neibours) >= 1:
                possibilities.append(to_close)
        if len(possibilities) == 0:
            return None
        else:
            return random.choice(possibilities)



    def close_cat_is_near_exit(self):
        """
        Fecha as células de saída caso o gato esteja próximo delas
        """

        if len([elem for elem in self.goals if elem not in self.walls]) > 0:
            #nearest_exits = self.get_exits_path_dist()
            nearest_exits = self.get_exits_dist()

            if nearest_exits is None:
                return None

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

            #Contando ao redor
            for neibour in neibours:
                goals_around += 1 if neibour in self.goals and neibour not in self.walls else 0
                walls_around += 1 if neibour in self.walls else 0


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
                    goals_around = 0
                    
                    for direction in ["NW", "NE", "W" , "E" , "SW", "SE"]:
                        opposite = self.get_opposite(grid, (elem['row'], elem['col']), direction)
                        if opposite is not None and opposite['is_wall']:
                            opposites_positives += 1
                        elif opposite is None:
                            opposites_positives += 1

                    for neibour in neibours:
                        if neibour['is_wall']: walls_around += 1
                        if neibour['is_border']: borders_around += 1
                        if neibour['is_goal'] and not neibour['is_wall']: goals_around += 1


                    if walls_around >= len(neibours):
                        continue

                    inverse_goal_path_dist = 1
                    distances = []
                    valid_goals = [goal for goal in self.goals if goal not in self.walls]
                    for goal in valid_goals:
                        distance = self.path_distance(goal, (elem['row'], elem['col']))
                        distances.append(distance)
                    if len(distances) > 0 and distances[0] != 0:
                        distances.sort(reverse=False)
                        inverse_goal_path_dist += (1 / (sum(distances[0:len(distances)//5])/len(distances) + 0.01) * 10)
                        score += inverse_goal_path_dist

                    if elem['row'] + elem['col'] in [10,11]:
                        score += 10 * inverse_goal_path_dist

                    score += goals_around * 50

                    if elem['row'] %2 == 0:
                        score += 15

                    if elem['col'] %3 == 0:
                        score += 15

                    if not elem['is_goal']:
                        score += goals_around
                    else:
                        if self.path_distance((elem['row'], elem['col']), self.cat_pos) <= 5 and goals_around >= 3:
                            score += goals_around * 2



                    cat_distance = self.path_distance( (elem['row'], elem['col']), self.cat_pos, max_dist=20)
                    inverse_cat_distance = (1/(cat_distance + 0.1) ) * 100
                    score += inverse_cat_distance

                    #inverse_walls_around = (1 /(walls_around + 0.1)) * 10
                    #score += inverse_walls_around


                    #score += 10 if opposites_positives < 4 else 0

                    if cat_distance == 3:
                        score += 15 * 2
                    if cat_distance == 2:
                        score += 30 * 3
                    if cat_distance == 1:
                        score += 20


                    if elem['is_goal']:
                        score = score/5
                    elem['score'] = score

                    if elem['score'] > grater_score or (elem['score'] == grater_score and random.randint(0,5) == 0)\
                            and elem['score'] > 0:
                        grater_score = elem['score']
                        grater_score_element = elem


        #count = 1
        #for row in grid:
        #    if count == -1:
        #        log.write('   ')
        #    for elem in row:
        #        count *= -1
        #        log.write('[{:^2}]'.format(int(elem['score'])))
        #    log.write('\n')
        #log.write('\n')

        if grater_score_element is None:
            return None
        else:
            return grater_score_element['row'], grater_score_element['col']

    def generate_random_position(self):
        '''
        Fecha uma posição aleatória no tabuleiro
        '''
        used = self.get_used_set()
        candidate = (random.randint(0, 10), random.randint(0, 10))
        while candidate in used:
            candidate = (random.randint(0, 10), random.randint(0, 10))
        return candidate


    def generate_random_around_cat(self):
        '''
        Fecha casas imediatamente ao redor do gato, de maneira aleatória
        '''
        cat = self.cat_pos
        candidates = self.get_neibours_position(cat, exclude_non_walkable=True)
        candidate = random.choice(candidates)
        return candidate


    def close_around_cat(self):
        '''
        Fecha casas imediatamente ao redor do gato, dando prioridade a casas que já não estão cercadas por paredes        
        '''
        cat = self.cat_pos
        candidates = self.get_neibours_position(cat, exclude_non_walkable=True)

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
            answer.append({'pos': goal, 'dist': distance})
        return answer


    def get_valid_goal_neibours(self, rowcol):
        neibours = self.get_neibours_position(rowcol=rowcol, exclude_non_walkable=True)
        goal_count = 0
        for neib in neibours:
            if neib in self.goals:
                goal_count += 1
        return goal_count


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
            used = self.get_used_set()
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
            used = self.get_used_set()
            candidates = [grid[elem[0]][elem[1]] for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10 and elem not in used]
        else:
            candidates = [grid[elem[0]][elem[1]] for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10]

        return candidates

    def get_used_set(self):
        used = self.walls.copy()
        used.add(cat)
        return used

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
                used = self.get_used_set()
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
                    for i in range(11)]
                for j in range(11)]

        open_set = deque([pos1])
        closed_set = set()

        while len(open_set) > 0:
            current = open_set.popleft()

            if current == pos2:
                size_counter = 0

                temp = grid[current[0]][current[1]]
                while temp['previous'] is not None:
                    temp = temp['previous']
                    size_counter += 1

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

c = Catcher(walls=blocks, goals=exits, cat_pos=cat)
result = c.catch_them_all()
print(result)



