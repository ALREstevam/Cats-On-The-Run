from enum import Enum
from operator import attrgetter

from Cell import Cell
from cats.CatFather import CatFather
from cats.astarcat.HeuristicValuesCalculator import HeuristicValuesCalculator
from cats.catshelper.DistanceCalculator import DistanceTypes


class Solution(Enum):
    CONTINUE = 'continue'
    NO_SOLUTION = 'no_solution'
    FINDED = 'finded'

class AstarCat(CatFather):
    def __init__(self, start_cell : Cell, objective_cell : Cell, distanceType : DistanceTypes = DistanceTypes.EUCLIDEAN, gWeight = 1, hWeight = 1, fWeight = 1, enableStepByStepPath = False):
        super(start_cell, objective_cell)
        self.heuristics = HeuristicValuesCalculator(gWeight, hWeight, fWeight, distanceType)
        self.pathIndex = 0
        self.enableView = enableStepByStepPath
        self.reset()

    def reset(self):
        super().reset()
        self.start.g = 0
        self.start.h = self.heuristics.h(self.start, self.end)
        self.start.f = self.heuristics.f(self.start)

    def findPathTo(self, endNode : Cell = None):
        self.reset()
        while True:
            answer = self.pathFindStep(endNode)
            if answer is not Solution.CONTINUE:
                #print('STEP : {}'.format(answer))
                return (answer, self.path)

    def pathFindStep(self, endNode : Cell = None):
        if endNode is None:
            endNode = self.end

        if len(self.open_set) > 0:
            #Buscar enquanto houverem nós na lista de nós abertos
            current = min(self.open_set, key=attrgetter('f'))

            #Se o nó de menor custo não for o objetivo
            if current is not self.end:
                # Removendo o nó de menor custo da lista de nós abertos, já que ele será acesssado
                self.open_set.remove(current)
                # Colocando o nó na lista de nós fechados
                self.closed_set.add(current)

            #Caso o nó aberto de menor custo seja o nó final
            elif current is self.end:
                lowerCell2 = min(self.open_set, key=lambda cell : cell.f if cell != self.end else 500)

                #Se o custo desse nó for menor que o custo do nó final pode ser que exista um caminho ainda melhor
                #e então devo continuar procurando, o nó final é mantido na lista de nós abertos

                if lowerCell2.f >= current.f:
                    #A lista com o caminho será gerada apenas quando o caminho for encontrado
                    self.fill_path(current)
                    return Solution.FINDED

            # HEURÍSTICA
            for neibor in current.neibors:
                hasNewPath = False

                #Caso o vizinho em questão não esteja fechado e não seja uma barreira então deve ser levado em consideração
                if not neibor in self.closed_set and not neibor.isWall:
                    #Cálculo de um g(n) temporário para o vizinho em questão
                    tempg = self.heuristics.g(current, neibor)

                    #Obs.: o vizinho pode ser um nó já aberto, portanto tem um valor de g ou um nó não aberto e tem que
                    #receber um valor de g

                    #Se o vizinho estiver na lista de nós abertos
                    if neibor in self.open_set:
                        #O g dele deve ser trocado apenas se o que foi calculado (tempg) for menor

                        # Trocar o g do nó se o novo caminho for melhor
                        if tempg < neibor.g:
                            neibor.g = tempg # O vizinho recebe um novo g
                            hasNewPath = True # O caminho mudou (uma flag)
                    # O nó não foi aberto ainda e será agora
                    else:
                        neibor.g = tempg #definindo o g do nó
                        self.open_set.add(neibor)#colocando o nó na lista de abertos
                        hasNewPath = True # O caminho mudou (uma flag)

                    #Se o caminho mudou
                    if hasNewPath:
                        #Cálculo da heurística
                        neibor.h = self.heuristics.h(neibor, endNode) #cálculo do h
                        neibor.f = self.heuristics.f(neibor)
                        #g já foi caculado!
                        neibor.previous = current #dizendo para o nó quem é seu antecessor (assim é possível recuperar o caminho)

            #Comente para aumentar a performance
            if self.enableView:
                self.fill_path(current) #depois do for
            return Solution.CONTINUE
        else:
            return Solution.NO_SOLUTION

    def nextStep(self):
        index = (len(self.path)-1) - self.pathIndex
        if self.pathIndex < len(self.path):
            self.x = self.path[index].xpos
            self.y = self.path[index].ypos
            self.pathIndex += 1
            return True
        else:
            return False



