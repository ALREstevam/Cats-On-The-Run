from cats.CatFather import CatFather
from Cell import Cell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class Grid:
    def __init__(self, exits, blocks, start, rows=10, cols=10):

        self.rows = rows
        self.cols = cols
        self.grid = [[None] * cols for _ in range(rows)]
        self.exits = exits
        self.walls = blocks
        self.start = start

        self.forEachCell(
            lambda row_index, col_index, args : self.assign_cell_condensed(
                row_index, col_index
            ))

        #self.setNeibors()
        #self.setDiff()

    def assignCell(self, row : int, col : int):
        is_wall = (row, col) in self.walls
        cell = Cell(row, col, self, is_wall)
        self.grid[row][col] = cell


    def assign_cell_condensed(self, row : int, col : int):
        self.grid[row][col] = Cell(row, col, self, ((row, col) in self.walls) )


    def __str__(self):
        answ = ''
        colCount = 0
        for row in self.grid:
            rowCount = 0
            for elem in row:
                answ += ('{}'.format(elem))
                rowCount += 1
            colCount += 1
            answ += ('\n')
        return answ


    def get_cell(self, pos: (int, int)) -> 'Cell.Cell':
        return self.get_cell_at(pos[0], pos[1])

    def get_cell_at(self, row : int, col: int) -> 'Cell.Cell':
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        else:
            raise IndexError('Invalid index [{}][{}]'.format(row, col))

    def get_start_cell(self) -> 'Cell.Cell':
        return self.grid[self.start[0]][self.start[1]]

    def get_exit_cells(self) -> ['Cell.Cell']:
        return list(map(lambda pos: self.get_cell(pos), self.exits))

    def get_wall_cells(self) -> ['Cell.Cell']:
        return list(map(lambda pos: self.get_cell(pos), self.walls))

    #Executa uma função (passada como parâmetro) para todas as células
    def forEachCell(self, function = None, dictArg = ()):
        if function is not None:
            for col_index in range(self.cols):
                for row_index in range(self.rows):
                    function(row_index, col_index, dictArg)

    #def setNeibors(self):
    #    self.forEachCell(lambda row_index, col_index, args : self.grid[row_index][col_index].add_neighbors(self))

    #Gera uma visualização do labirinto no estado atual
    def show(self, cat : CatFather = None):

        catChar = '[╳]'
        startChar = bcolors.OKBLUE + '[🐈]' + bcolors.ENDC
        endChar = bcolors.OKGREEN + '[★]' + bcolors.ENDC
        pathChar = bcolors.OKBLUE + '[●]' + bcolors.ENDC
        openSetChar = bcolors.FAIL + '[O]' + bcolors.ENDC
        closedSetChar = bcolors.WARNING + '[ ]' + bcolors.ENDC

        pathCoordinates = None
        openSetCoordinates = None
        closedSetCoordinates = None

        if cat is not None:
            #pathCoordinates = list(map(lambda cell : (cell.xpos, cell.ypos), cat.path))
            #pathCoordinates = list(map(lambda pos: (cat.path[0][0], cat.path[0][1]), cat.path))
            pathCoordinates = cat.path.get_positions()
            openSetCoordinates = list(map(lambda cell: (cell.xpos, cell.ypos), cat.open_set))
            closedSetCoordinates = list(map(lambda cell: (cell.xpos, cell.ypos), cat.closed_set))

        exitsList = self.exits


        answ = []

        answ.append('GRID\n')
        for row_index in range(self.rows):

            if not row_index % 2 == 0:
                answ.append(' ')

            for col_index in range(self.cols):
                #Start
                if row_index == self.start[0] and col_index == self.start[1]:
                    answ.append(startChar)
                #End
                elif exitsList is not None and (row_index, col_index) in exitsList:
                    answ.append(endChar)
                #Cat
                elif cat is not None and row_index == cat.x and col_index == cat.y:
                    answ.append(catChar)
                #Path
                elif pathCoordinates is not None and (row_index, col_index) in pathCoordinates:
                    answ.append(pathChar)
                #Open set
                elif openSetCoordinates is not None and (row_index, col_index) in openSetCoordinates:
                    answ.append(openSetChar)
                #ClosedSet
                elif closedSetCoordinates is not None and (row_index, col_index) in closedSetCoordinates:
                    answ.append(closedSetChar)
                #Wall | No Wall | Difficulty
                else:
                    answ.append('['+self.grid[row_index][col_index].show()+']')

            answ.append('\n')
        return ''.join(answ)


    # Cálculo de de dificuldade para as células (quanto mais paredes próximais maior a dificuldade)
    # def setDiff(self):
    #    for line in self.grid:
    #        for elem in line:
    #            if elem.isWall:
    #                for neibour in elem.neibors:
    #                    neibour.difficulty += (neibour.difficulty * 0.2)

    # Criação de uma célula com propabilidade aleatória de ser parede
    # def createCell(self, x, y) -> Cell:
    #    return Cell(
    #                x, y,
    #                grid=self,
    #                is_wall=(randrange(0, 100) > 80),
    #                difficulty=0.1,
    #                )

    # difficulty = uniform(0, 0.9) #use for random difficulty
    # Popula o grid com células
    # def assignCell(self, row, col):
    #    self.grid[row][col] = self.createCell(row, col)


    #Geração de de uma view do grid que possa ser interpretada por um outro método
    #def showAsArray(self, cat : Cat):
    #    pathCoordinates = list(map(lambda cell : (cell.xpos, cell.ypos), cat.path))
    #    openSetCoordinates = list(map(lambda cell: (cell.xpos, cell.ypos), cat.openSet))
    #    closedSetCoordinates = list(map(lambda cell: (cell.xpos, cell.ypos), cat.closedSet))
    #    answ = [[None] * self.cols for _ in range(self.rows)]
    #    for row_index in range(self.rows):
    #        for col_index in range(self.cols):
    #            tmp = {
    #                'x' : row_index,
    #                'y' : col_index,
    #                'isStart' : False,
    #                'isEnd' : False,
    #                'isCat' : False,
    #                'isPath' : False,
    #                'onOpenSet' : False,
    #                'onClosedSet' : False,
    #                'isWall' : False,
    #                'difficulty' : None
    #            }
    #            #Start
    #            if row_index == self.start[0] and col_index == self.start[1]:
    #                tmp['isStart'] = True
    #            #End
    #            if row_index == self.end[0] and col_index == self.end[1]:
    #                tmp['isEnd'] = True
    #                #Cat
    #            if row_index == cat.x and col_index == cat.y:
    #                tmp['isCat'] = True
    #                #Path
    #            if pathCoordinates is not None and (row_index, col_index) in pathCoordinates:
    #                tmp['isPath'] = True
    #                #Open set
    #            if openSetCoordinates is not None and (row_index, col_index) in openSetCoordinates:
    #                tmp['onOpenSet'] = True
    #                #Wall | No Wall | Difficulty
    #            if closedSetCoordinates is not None and (row_index, col_index) in closedSetCoordinates:
    #                tmp['onClosedSet'] = True
    #                #Wall | No Wall | Difficulty
    #            if self.grid[row_index][col_index].isWall:
    #                tmp['isWall'] = True
    #            tmp['difficulty'] =(self.grid[row_index][col_index].difficulty)
    #            answ[row_index][col_index] = tmp
    #    return answ

from Cell import Cell

