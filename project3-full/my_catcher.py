import sys
import random
from collections import deque
import math
from util.HexDistance import Distance


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




class DumbLogger:
    def __init__(self):
        self.file_name = 'catcher.html'
        self.isDumb = not RECORD_LOG

    def log(self, str, end = '<br>\n'):
        if not self.isDumb:
            with open(self.file_name, 'a', encoding='utf-8') as file:
                file.write('{}{}'.format(str, end))

    def sep(self):
        if not self.isDumb:
            with open(self.file_name, 'a', encoding='utf-8') as file:
                file.write('<br>\n' + '-' * 70 + '<br>\n')
                file.write('<script>window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);</script>')

dlog = DumbLogger()



class Catcher:
    def __init__(self, cat_pos, walls : [], goals : []):
        self.cat_pos = tuple(cat_pos)
        self.walls = set(walls)
        self.goals = set(goals)

        self.valid_goals =  [goal for goal in goals if goal not in self.walls]
        self.goal_count = len(self.valid_goals)
        self.wall_count = len(walls)

    @property
    def directions(self):
        direcs = ["NW", "NE", "W" , "E" , "SW", "SE"]
        random.shuffle(direcs)
        return direcs

    def catch_them_all(self):
        solutions = list()

        #Lista de métodos com diferentes formas de capturar o gato, executados na ordem que aparecem na lista
        #Caso retorne None ou lance exceção, passa para o próximo método da lista

        solutions.append([self.first_move,                      'first_move'])
        solutions.append([self.catch_trapped_cat,               'catchTrapped'])

        #solutions.append([self.corner_closer,                   'corner_closer'])
        #solutions.append([self.danger_pos_closer,               'danger_pos_closer'])

        solutions.append([self.close_cat_is_near_exit_pathdist, 'catNearExitPathDist'])

        solutions.append([self.block_cat_path,                  'block_cat_path'])

        solutions.append([self.block_cat_before_goal_0,         'block_cat_before_goal_0'])
        solutions.append([self.block_exit_neib,                 'block_exit_neib'])
        #solutions.append([self.make_cat_decide,                 'make_cat_decide'])
        #solutions.append([self.catch_almost_trapped_cat,        'catchAlmostTrapped'])
        #solutions.append([self.mess_with_cat,                   'mess_with_cat'])
        #solutions.append([self.close_stategic,                  'close_stategic'])
        #solutions.append([self.heuristic_closer,                'heuristicCloser'])

        solutions.append([self.close_around_cat2,               'close_around_cat'])
        solutions.append([self.close_around_cat,                'close_around_cat'])
        solutions.append([self.close_cat_is_near_exit,          'catNearExit'])
        solutions.append([self.close_nearest_exit,              'closeNearestExit'])
        solutions.append([self.generate_random_around_cat,      'randomAroundCat'])

        solutions.append([self.generate_random_position,        'closeRandom'])


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
                     'is_goal': (j, i) in self.goals,
                     'is_border': i in [0, 10] or j in [0, 10],
                     'cant_close': (j, i) in self.walls or (j, i) == self.cat_pos,
                     'score': 0
                     }
                    for i in range(11)] for j in range(11)]

    def danger_pos_closer(self):

        #for neib in self.get_neibours_position(self.cat_pos, True):
        #    if neib in self.valid_goals:
        #        return None

        candidates = [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (9, 1), (1, 9), (3, 9), (5, 9), (7, 9), (9, 9), (1, 3), (1, 5), (1, 7), (9, 3), (9, 5), (9, 7)]

        positions = {
        }

        for canditate in candidates:
            if canditate not in self.walls and canditate != self.cat_pos:
                positions[canditate] = {'importance': (1 if canditate in [(1, 3), (1, 5), (1, 7), (9, 3), (9, 5), (9, 7)] else 2)}

        if len(positions) == 0:
            return None

        for pos, data in  positions.items():
            data['goalsAround'] = len([neib for neib in self.get_neibours_position(pos, True) if neib not in self.walls])
            data['distToCat'] = self.path_distance(pos, self.cat_pos, 50)


        max_importance =    positions[max(positions, key=lambda x: positions[x]['importance'])]['importance']
        min_importance =    positions[min(positions, key=lambda x: positions[x]['importance'])]['importance']
        max_dist =          positions[max(positions, key=lambda x: positions[x]['distToCat'])]['distToCat']
        min_dist =          positions[min(positions, key=lambda x: positions[x]['distToCat'])]['distToCat']
        max_goals =         positions[max(positions, key=lambda x: positions[x]['goalsAround'])]['goalsAround']
        min_goals =         positions[min(positions, key=lambda x: positions[x]['goalsAround'])]['goalsAround']

        for pos, data in positions.items():
            a = self.normalize(data['importance'], min_importance, max_importance,False)
            b = self.normalize(data['distToCat'], min_dist,max_dist, True)
            c = self.normalize(data['goalsAround'], min_goals,max_goals, False)
            data['score'] = a/2 + (3 * b) + c

        better_pos = max(positions, key=lambda x: positions[x]['score'])
        #print(positions[better_pos]['score'])
        if positions[better_pos]['score'] >= 4.0:
            return better_pos
        return None


    def first_move(self):
        if self.cat_pos == (5,5):
            return self.danger_pos_closer()
            #return self.close_around_cat2()


    def corner_closer(self):
        close_pattern = [
            {'close':(1,9) , 'cat_on':(1,8), 'is_open':[(0,10), (1,10), (2,10)],  'is_close':[(0,8), (0,9)]},
            {'close':(1,9) , 'cat_on':(2,9), 'is_open':[(0,9), (0,10), (1,10)],   'is_close':[(2,10)]},
            {'close':(9,9) , 'cat_on':(8,9), 'is_open':[(9,10), (10,10), (10,9)], 'is_close':[(8,10)]},
            {'close':(9,9) , 'cat_on':(9,8), 'is_open':[(8,10), (9,10), (10,10)], 'is_close':[(10,8), (10,9)]},
        ]

        for pattern in close_pattern:

            if cat == pattern['cat_on']:

                open_count = 0
                for cell in pattern['is_open']:
                    if cell not in self.walls:
                        open_count += 1

                if open_count == 1:
                    continue

                is_close_ok = True
                for cell in pattern['is_close']:
                    if cell not in self.walls:
                        is_close_ok = False
                        break

                if not is_close_ok:
                    continue

                return close_pattern['close']
        return None


    def block_exit_neib(self):

        for neib in self.get_neibours_position(self.cat_pos, True):
            if neib in self.valid_goals:
                return None

        scores = {}

        for goal in self.valid_goals:
            neibs = self.get_neibours_position(goal)

            for neib in neibs:
                if neib in self.valid_goals:
                    continue
                else:
                    if neib not in scores:
                        scores[neib] = {}
                        scores[neib]['goals'] = 1
                        scores[neib]['cat_dist'] = self.path_distance(neib, self.cat_pos)
                    else:
                        scores[neib]['goals'] += 1

        if len(scores) == 0:
            return None

        min_cat_dist = scores[min(scores, key=lambda x: scores[x]['cat_dist'])]['cat_dist']
        max_cat_dist = scores[max(scores, key=lambda x: scores[x]['cat_dist'])]['cat_dist']

        min_goals = scores[min(scores, key=lambda x: scores[x]['goals'])]['goals']
        max_goals = scores[max(scores, key=lambda x: scores[x]['goals'])]['goals']

        for pos, score_data in scores.items():
            scores[pos]['norm_dist'] = \
                Catcher.normalize(
                    scores[pos]['cat_dist'],
                    min_cat_dist,
                    max_cat_dist,
                    reversed=True)

            scores[pos]['norm_goals'] = \
                Catcher.normalize(
                    scores[pos]['goals'],
                    min_goals,
                    max_goals,
                    reversed=False)

            scores[pos]['score']  = (scores[pos]['norm_goals']) * 0.3 + scores[pos]['norm_dist']

        best_score = scores[max(scores, key=lambda x : scores[x]['score'])]['score']

        best_elements = []

        if best_score < .8:
            return None

        for pos, elem in scores.items():
            if Catcher.is_between(elem['score'], best_score - 0.1, best_score + 0.1):
                best_elements.append(pos)

        if len(best_elements) == 0:
            return None

        return random.choice(best_elements)


    def block_cat_path(self):
        better_path = None
        better_dist = 10000
        better_lead_to_goals = 0

        for goal in self.valid_goals:
            data = self.path(self.cat_pos, goal)
            dist = data['dist']


            if dist == 1 or dist == math.inf:
                continue
            lead_to_goals = 0

            for neib in self.get_neibours_position(data['path'][-1]):
                if neib in self.goals:
                    lead_to_goals += 1

            if dist < better_dist and lead_to_goals >= better_lead_to_goals:
                better_dist = dist
                better_path = data['path']
                better_lead_to_goals = lead_to_goals

            if dist == better_dist and lead_to_goals > better_lead_to_goals:
                better_dist = dist
                better_path = data['path']
                better_lead_to_goals = lead_to_goals

        if better_dist > 5 or better_dist < 2:
            return None

        return random.choice(better_path[1:min(2, len(better_path))])


    def block_cat_before_goal_0(self):
        '''
        Em alguns casos é melhor fechar uma célula que bloqueie o gato de chegar em um nó com duas ou mais saídas
        ao redor (sairá de qualquer forma)

        Exemplo:
        * = GOAL
        c = GATO
        + = MELHOR CÉLULA A SER FECHADA

            (*)(*)(x)(x)(x)(x)(x)
             (*)(+)(c)()( )( )( )
            (*)( )(x)( )( )( )( )
             (*)( )( )( )( )( )( )
            (*)( )( )( )( )( )( )

        Notar que:

        A distância entre o gato e o goal mais próximo é 2
        O goal mais próximo tem 3 vizinhos que também são goals
        2 goals estão na distância mínima

        Se o próximo passo for fechar um dos goals mais próximos o gato conseguirá sair
        Fechando o nó com o `+` o caminho do gato para o goal mais próximo vai para 4
        A ditância é dobrada com um movimento apenas

        Algoritmo:

        Para cada vizinho de CAT conte quantos vizinhos que são GOALS estão ao redor dele
        Do maior até goal == 3:
            Faça a interseção dos nós vizinhos de GATO e do NÓ ESCOLHIDO
            Sempre serão dois nós
            Se ambos forem WALLS
            Feche o NÓ ESCOLHIDO
        '''

        aux = {
        }

        cells_to_process = set()

        for neib in self.get_neibours_position(self.cat_pos, exclude_non_walkable=True):
            if neib in self.valid_goals:
                dlog.log('A NEIB IS GOAL')
                return None


        for cat_neib in self.get_neibours_position(self.cat_pos, exclude_non_walkable=True):
            if cat_neib not in self.walls and cat_neib != self.cat_pos:
                cells_to_process.add(cat_neib)
            #for neib_neib in self.get_neibours_position(cat_neib, exclude_non_walkable=True):
            #    if neib_neib not in cells_to_process and neib_neib not in self.walls and neib_neib != self.cat_pos:
            #        cells_to_process.add(neib_neib)


        can_close = []

        # Testando se CELL pode ser fechada
        for cell in cells_to_process:

            #Se a célula não estiver já fechada ou ocupada pelo gato
            if cell in self.walls or cell == self.cat_pos:
                continue

            block_count = 0
            for neib in self.get_neibours_position(cell, False):
                if neib in self.walls:
                    block_count += 1

            if block_count > 2:
                continue

            for direction in self.directions:#Para a célula, testando todas as direções
                point_to = self.position_from_direction(cell, direction, walkable_only=False)

                if point_to is None:
                    continue

                #Se na direção escolhida tiver uma wall, posso continuar
                if not point_to in self.walls:
                    continue

                #Testo se numa das direções opostas também tem uma paede
                opposites = self.get_all_opposites_pos(pos=cell, direction=direction, walkable_only = False)

                if opposites is None:
                    continue

                #Se for uma parede adiciono a célula na lista dos pontos que podem ser fechados
                for opposite in opposites:
                    if opposite in self.walls:
                        if self.rotation_position(cell, direction, 'CW') in self.walls or self.rotation_position(cell, direction, 'CW') in self.walls:
                            continue

                        can_close.append(cell)

                if len(can_close) >= 1:
                    return random.choice(can_close)

            return None


    def make_cat_decide(self):
        '''
        Este método avalia todos os nós ao redor do gato que estão abertos
        Para cada nó é feita a distância em path para cada goal e armazenada numa lista dist
        Para cada nó min é a distância mínima
        Para cada nó é contado quatas vezes min se repete em dist, esse valor é a quantidade de hits
        uma posição com maior valor em hits tem maior potencial de confundir o pegador, fazendo com que
        feche um goal em uma lateral para a qual o gato não vai andar

        Fechando esse nó o gato é obrigado a escolher uma direção que confunda menos o pegador
        '''


        neibs = self.get_neibours_position(self.cat_pos, exclude_non_walkable=True)

        if len(neibs) == 0:
            return None

        for neib in neibs:
            if neib in self.valid_goals:
                return None

        dists = {}
        goal_count = self.goal_count

        for neib in neibs:
            dists[neib] = {'dist_lst':[], 'min':None, 'hits':0, 'hits_normalized':0}

            for goal in self.valid_goals:
                path_distance = self.path_distance(neib, goal)
                dists[neib]['dist_lst'].append(path_distance)

            dists[neib]['min'] = min(dists[neib]['dist_lst'])

            if dists[neib]['min'] <= 2:
                return None

            min_hits = Catcher.count(dists[neib]['dist_lst'], [dists[neib]['min']])
            dists[neib]['hits'] = min_hits
            min_hits_normalized = Catcher.normalize(dists[neib]['hits'], 0, goal_count)
            dists[neib]['hits_normalized'] = min_hits_normalized
        maximum = max(dists, key=lambda el : dists[el]['hits_normalized'])
        threshold = 0.15

        if dists[maximum]['hits_normalized'] > threshold:
            return maximum
        else:
            return None

    def close_cat_is_near_exit_pathdist(self):
        '''
        Fecha saídas em que o gato está próximo (usando path distance)

        Algoritmo:

        Calcule a distância em path do gato para cada uma das saídas

        Ao encontrar uma saída em que a distância for <= 4
            Feche a saída
        Ao encontrar uma saída em que a distância
        '''
        if self.goal_count > 0:
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

            if nearest['dist'] <= 4:
                return nearest['pos']
            elif nearest['dist'] <= 7:
                goals_count = self.get_valid_goal_neibours(nearest['pos'])
                if goals_count >= 4:
                    return nearest['pos']
            else:
                return None

    def close_stategic(self):
        '''
        Fecha nós que tem muitas saídas ao seu redor
        '''
        cat_neibours = self.get_valid_goal_neibours(self.cat_pos)



        for i in range(11):
            for j in range(11):
                elem = (j,i)

                if elem in self.walls or elem == self.cat_pos:
                    continue

                goal_count = self.get_valid_goal_neibours(elem)
                distance_to_cat = self.path_distance(elem, self.cat_pos)

                if goal_count >= 4 \
                        and Catcher.is_between(distance_to_cat, 1, 3):
                    return elem

                if goal_count >= 2 \
                        and Catcher.is_between(distance_to_cat, 1, 3):
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

        if self.goal_count > 0:
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


            if nearest['dist'] <= 3:
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
        if len(neibours) <= 3: # Se houverem 3 ou menos vizinhos
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
                    valid_goals = self.valid_goals

                    for goal in valid_goals:
                        distance = self.path_distance(goal, (elem['row'], elem['col']))
                        distances.append(distance)

                    if len(distances) > 0 and distances[0] != 0:
                        distances.sort(reverse=False)
                        inverse_goal_path_dist += (1 / (sum(distances[0:len(distances)//5])/len(distances) + 0.01) * 10)
                        score += inverse_goal_path_dist

                    #Antigo código para fechar a diagonal (fechar onde x + y for 10 ou 11
                    #if elem['row'] + elem['col'] in [10,11]:
                    #    score += 10 * inverse_goal_path_dist



                    # Faz o X nas diagonais
                    diag1 = set([
                         (10,0), (9,0), (9,1), (8,2), (7,2), (7,3), (6,4), (5,4),
                         (5,5),(4,6),(4,7),(3,7),(2,8),(1,8),(1,9), (0,10)
                    ])
                    diag2 = set([
                        (0,0), (0,1), (1,1), (2,2), (3,2), (3,3), (4,4), (5,4),
                        (5,5), (6,6), (6,7), (7,7), (8,8), (9,8), (9,9), (10,10),
                    ])

                    if (elem['row'], elem['col']) in diag1.intersection(diag2):
                        score += 10 * inverse_goal_path_dist

                    # Alguns fechamentos estratégicos
                    goal_neibs = set([
                        (1,1), (1,3), (1,5), (1,7), (1,9), (3,9), (5,9), (7,9), (9,9),
                        (9,7), (9,5),(9,3), (9,1), (7,1), (5,1), (3,1), (1,1),
                    ])

                    if (elem['row'], elem['col']) in goal_neibs:
                        score += 5

                    #Fechar células com saídas próximas
                    score += goals_around * 50

                    #Fechar uma a cada três linhas
                    if elem['row'] %3 == 0:
                        score += 15

                    #Fechar uma a cada duas colunas
                    if elem['col'] %3 == 0:
                        score += 15

                    if not elem['is_goal']:# Se o elemento for uma saída
                        score += goals_around * 2 # Adicione ao score quantos de seus vizinhos são goals também
                    #else:
                    #    #Se o elemento não for saída mas estiver a uma distância do gato <= 5 e tiver >= 3 goals ao redor
                    #    if self.path_distance((elem['row'], elem['col']), self.cat_pos) <= 5:
                    #        if goals_around >= 3:
                    #            score += goals_around * 2
                    #        if goals_around >= 2 and (elem['row'], elem['col'] in ( (1,1), (9,1)) ):
                    #            score += (goals_around+1) * 2




                    cat_distance = self.path_distance( (elem['row'], elem['col']), self.cat_pos, max_dist=20)
                    inverse_cat_distance = (1/(cat_distance + 0.1) ) * 15
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
                        score /= 5
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

    def close_around_cat2(self):
        cat_neibs = self.get_neibours_position(self.cat_pos, exclude_non_walkable=True)

        if len(cat_neibs) <= 1:
            return None

        evaluation_set = set(cat_neibs)

        for neib in cat_neibs:
            evaluation_set.union(set(
                    self.get_neibours_position(neib, exclude_non_walkable=True)
                )
            )

        win_distance = 0
        win_neib = cat_neibs[0]

        for neib in evaluation_set:
            dist = 0
            lowest_distance = math.inf

            neibs_neibs = self.get_neibours_position(neib, exclude_non_walkable=True)

            for aux_neib in neibs_neibs:
                if aux_neib in self.valid_goals:
                    dist -= 10

            for goal in self.valid_goals:
                dist += self.path_distance(neib, goal)

                if dist < lowest_distance:
                    lowest_distance = dist

                if dist == lowest_distance and random.randint(0,1) == 0:
                    lowest_distance = dist

            if lowest_distance < win_distance:
                win_distance = lowest_distance
                win_neib = neib

            if lowest_distance == win_distance and random.randint(0,1) == 0:
                win_distance = lowest_distance
                win_neib = neib

        return win_neib

    def close_around_cat(self):
        '''
        Fecha casas imediatamente ao redor do gato, dando prioridade a casas que já não estão cercadas por paredes        
        '''
        cat = self.cat_pos
        cat_neibs = self.get_neibours_position(cat, exclude_non_walkable=True)

        if len(cat_neibs) <= 1:
            return None

        win_distance = 0
        win_neib = cat_neibs[0]

        for neib in cat_neibs:
            lowest_distance = math.inf

            for goal in self.valid_goals:
                dist = self.path_distance(neib, goal)

                if dist < lowest_distance:
                    lowest_distance = dist

            if lowest_distance < win_distance:
                win_distance = lowest_distance
                win_neib = neib

        if win_distance > 4:
            return None
        return win_neib




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
        for goal in self.valid_goals:
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
        for goal in self.valid_goals:
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

    def get_neibours_position(self, rowcol, exclude_non_walkable = True) -> list:
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


    def get_middle_cel(self, center, pos1, pos2):

        candidates = {
            [(center[0] - 1, center[1] - 1), (center[0] - 1, center[1])][center[0] % 2] : "NW",
            [(center[0] - 1, center[1]), (center[0] - 1, center[1] + 1)][center[0] % 2] : "NE",
            [(center[0], center[1] - 1), (center[0], center[1] - 1)][center[0] % 2] : "W" ,
            [(center[0], center[1] + 1), (center[0], center[1] + 1)][center[0] % 2] : "E" ,
            [(center[0] + 1, center[1] - 1), (center[0] + 1, center[1])		][center[0] % 2] : "SW",
            [(center[0] + 1, center[1]	) ,	 (center[0] + 1, center[1] + 1)	    ][center[0] % 2] : "SE",
        }

        dir1 = None
        dir2 = None

        if pos1 in candidates:
            dir1 = candidates[pos1]

        if pos2 in candidates:
            dir2 = candidates[pos2]

        if dir1 is None or dir2 is None:
            return None



        middle_direction = {
            ('NW', 'SW') : 'W',
            ('W', 'SE'): 'SW',
            ('SW', 'E'): 'SE',
            ('SE', 'NE'): 'E',
            ('NE', 'W'): 'NW',
            ('E', 'NW'): 'NE',
        }

        choosed_dir = None

        if (dir1, dir2) in middle_direction:
            choosed_dir =  middle_direction[ (dir1, dir2) ]

        if (dir2, dir1) in middle_direction:
            choosed_dir = middle_direction[ (dir2, dir1) ]

        if choosed_dir is None:
            return None

        return self.position_from_direction(center, choosed_dir, walkable_only=False)


    def get_all_opposites_pos(self, pos, direction, walkable_only = True):
        opposites = {
            "NW":   ['NE'   ,   'W'     , 'SE'  ],
            "NE":   ['NW'   ,   'E'     , 'SW'  ],
            "E":    ['NE'   ,   'SE'    , 'W'   ],
            "SE":   ['E'    ,   'SW'    , 'NW'  ],
            "SW":   ['SE'   ,   'W'     , 'NE'  ],
            "W":    ['SW'   ,   'NW'    , 'E'   ],
        }

        if direction not in opposites:
            return None

        opposites_direction = opposites[direction]
        opposites_position = []


        for op_direc in opposites_direction:
            pos = self.position_from_direction(pos, op_direc, walkable_only=walkable_only)

            if pos is not None:
                opposites_position.append(pos)

        if len(opposites_position) == 0:
            return None
        else:
            return opposites_position



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
        return  self.path(pos1=pos1, pos2=pos2, max_dist=max_dist)['dist']

    def path(self, pos1, pos2, max_dist = math.inf):
        pos1, pos2 = pos2, pos1
        nodes = []
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
                nodes.append((temp['row'], temp['col']))
                while temp['previous'] is not None:
                    temp = temp['previous']
                    nodes.append( (temp['row'], temp['col']) )
                    size_counter += 1

                return {'dist' : size_counter, 'path' : nodes}

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
        return {'dist' : max_dist, 'path' : []}


    def rotation_position(self, center, direction, rotation_direction):
        if rotation_direction not in ['CW', 'ACW']:
            return None

        cw_rotaton = {
            "NW"    :'NE',
            "NE"    :'E',
            "W"     :'NW',
            "E"     :'SE',
            "SW"    :'W',
            "SE"    :'SW',
        }

        acw_rotaton = {
            "NW":   'W',
            "NE":   'NW',
            "W":    'SW',
            "E":    'NE',
            "SW":   'SE',
            "SE":   'E',
        }

        if rotation_direction == 'CW':
            rotator = cw_rotaton
        else:
            rotator = acw_rotaton

        if direction not in rotator:
            return None

        new_direction = rotator[direction]

        return self.position_from_direction(center, new_direction, walkable_only=False)

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
    def is_between(value, min_fence, max_fence, inclusive_min = True, inclusive_max = False):
        up_min = False
        down_max = False
        if inclusive_min and value >= min_fence:
            up_min = True
        if not inclusive_min and value > min_fence:
            up_min = True
        if inclusive_max and value <= max_fence:
            down_max = True
        if not inclusive_max and value < max_fence:
            down_max = True
        return up_min and down_max

c = Catcher(walls=blocks, goals=exits, cat_pos=cat)
result = c.catch_them_all()
print(result)



