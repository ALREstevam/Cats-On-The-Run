from cats.catshelper.DistanceCalculator import Distance2DCalculator, DistanceTypes

class HeuristicValuesCalculator:

    def __init__(self, gWeight = 1, hWeight = 1, fWeight = 1, distanceType : DistanceTypes = DistanceTypes.EUCLIDEAN):
        self.gWeight = gWeight
        self.hWeight = hWeight
        self.fWeight = fWeight
        self.distanceCalculator = Distance2DCalculator(distanceType)

    def g(self, previousNode : 'Cell.Cell', nextNode : 'Cell.Cell'):
        g = previousNode.vars['g'] + \
            (self.gWeight * nextNode.difficulty) + \
            self.distanceCalculator.distCell(previousNode, nextNode)
        return g


    def h(self, nextNode: 'Cell.Cell', endNode: 'Cell.Cell'):
        h = self.hWeight * self.distanceCalculator.distCell(nextNode, endNode)
        return h

    def f(self, nextNode: 'Cell.Cell'):
        f = (self.fWeight * nextNode.vars['g']) + nextNode.vars['h']
        return f

    def calculate(self, previousNode: 'Cell.Cell', nextNode: 'Cell.Cell', endNode: 'Cell.Cell'):
        g = self.g(previousNode, nextNode)
        nextNode.vars['g'] = g

        h = self.h(nextNode, endNode)
        nextNode.vars['h'] = h

        f = self.f(nextNode)
        nextNode.vars['f'] = f

        return {
            'f':f,
            'g':g,
            'h':h
        }




