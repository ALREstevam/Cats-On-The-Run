from operator import attrgetter
from cats.CatFather import CatFather
from cats.astarcat.HeuristicValuesCalculator import HeuristicValuesCalculator
from cats.catshelper.DistanceCalculator import DistanceTypes
from cats.CatFather import Solution


class AstarCat(CatFather):
    def __init__(self,
                 start_cell : 'Cell.Cell',
                 objective_cell : 'Cell.Cell',
                 grid : 'Grid.Grid',
                 distanceType : DistanceTypes = DistanceTypes.EUCLIDEAN,
                 gWeight = 1,
                 hWeight = 1,
                 fWeight = 1,
                 max_iterations = None,

                 ):
        super().__init__(start_cell, objective_cell, grid)

        self.heuristics = HeuristicValuesCalculator(gWeight, hWeight, fWeight, distanceType)
        self.reset()
        self.max_iterations = max_iterations

    def reset(self):
        super().reset()

        self.start.vars['g'] = 0
        self.start.vars['h'] = self.heuristics.h(self.start, self.end)
        self.start.vars['f'] = self.heuristics.f(self.start)

        #self.start.g = 0
        #self.start.h = self.heuristics.h(self.start, self.end)
        #self.start.f = self.heuristics.f(self.start)


    def find_path(self):
        solve_status = Solution.CONTINUE
        iteration_counter = 0

        while solve_status not in [Solution.FINDED, Solution.NO_SOLUTION] and iteration_counter != self.max_iterations:
            iteration_counter += 1
            end_node = self.end
            if len(self.open_set) > 0:
                # Buscar enquanto houverem nós na lista de nós abertos
                #current = min(self.open_set, key=attrgetter('f'))
                current = min(self.open_set, key=lambda item : item.vars['f'])

                # Se o nó de menor custo não for o objetivo
                if current is not self.end:
                    # Removendo o nó de menor custo da lista de nós abertos, já que ele será acesssado
                    self.open_set.remove(current)
                    # Colocando o nó na lista de nós fechados
                    self.closed_set.add(current)

                # Caso o nó aberto de menor custo seja o nó final
                elif current is self.end:
                    lowerCell2 = min(self.open_set, key=lambda cell: cell.vars['f'] if cell != self.end else 2000)

                    # Se o custo desse nó for menor que o custo do nó final pode ser que exista um caminho ainda melhor
                    # e então devo continuar procurando, o nó final é mantido na lista de nós abertos

                    if lowerCell2.vars['f'] >= current.vars['f']:
                        # A lista com o caminho será gerada apenas quando o caminho for encontrado
                        solve_status = Solution.FINDED
                        self.fill_path(current, True)
                        break

                # HEURÍSTICA
                for neighbor in set(current.neighbors.keys()):
                    hasNewPath = False

                    # Caso o vizinho em questão não esteja fechado e não seja uma barreira então deve ser levado em consideração
                    if not neighbor in self.closed_set and not neighbor.is_wall:
                        # Cálculo de um g(n) temporário para o vizinho em questão
                        tempg = self.heuristics.g(current, neighbor)

                        # Obs.: o vizinho pode ser um nó já aberto, portanto tem um valor de g ou um nó não aberto e tem que
                        # receber um valor de g

                        # Se o vizinho estiver na lista de nós abertos
                        if neighbor in self.open_set:
                            # O g dele deve ser trocado apenas se o que foi calculado (tempg) for menor

                            # Trocar o g do nó se o novo caminho for melhor
                            if tempg < neighbor.vars['g']:
                                neighbor.vars['g'] = tempg  # O vizinho recebe um novo g
                                hasNewPath = True  # O caminho mudou (uma flag)
                        # O nó não foi aberto ainda e será agora
                        else:
                            neighbor.vars['g'] = tempg  # definindo o g do nó
                            self.open_set.add(neighbor)  # colocando o nó na lista de abertos
                            hasNewPath = True  # O caminho mudou (uma flag)

                        # Se o caminho mudou
                        if hasNewPath:
                            # Cálculo da heurística
                            neighbor.vars['h'] = self.heuristics.h(neighbor, end_node)  # cálculo do h
                            neighbor.vars['f'] = self.heuristics.f(neighbor)
                            # g já foi caculado!
                            neighbor.previous = current  # dizendo para o nó quem é seu antecessor (assim é possível recuperar o caminho)
                solve_status = Solution.CONTINUE
                self.fill_path(current, True)
            else:
                solve_status = Solution.NO_SOLUTION

        return solve_status
