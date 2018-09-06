from Directions import Directions

class Cell:

    # Referência estática para o grid (necessário para calcular os vizinhos apenas quando for necessário)
    static_grid_ref = None

    # Construtor
    def __init__(self, x, y, grid :'Grid.Grid', is_wall=False, difficulty=0.1):
        '''
        Object that represents a cell of a hexagonal grid

        :param x: column of the cell
        :param y:  row of the cell
        :param grid:  reference of the grid
        :param is_wall:  True if the cell is a barrier
        :param difficulty: Difficulty associated to the cell
        '''
        self.xpos = x
        self.ypos = y
        self.is_wall = is_wall
        self.difficulty = difficulty #dificuldade para dar suporte a algoritmos como A*

        self.__neighbors  =   None

        #self.f          =   None
        #self.g          =   None
        #self.h          =   None

        self.vars = {}

        #TODO: o desempenho disso pode ser melhorado
        #TODO: não faz sentido uma célula saber o caminho, isso é trabalho do tabuleiro
        self.previous   =   None #Referência para o nó anterior (seguindo como uma lista ligada para encontrar o melhor caminho)

        #Setando a variável estática caso não tenha sido setada ainda
        if self.static_grid_ref is None:
            self.static_grid_ref = grid

    #Sobrescrevendo o operador `.` quando se está acessando um atributo
    def __getattr__(self, item):
        if item == 'neighbors':#se for feito algo como `cell.neibors`
            if self.__neighbors is None: #Caso os vizinhos da célula não tenham sido calculados
                self.add_neighbors(self.static_grid_ref)#Calcule os viznhos
            return self.__neighbors #Retorne os vizinhos
        else:
            raise AttributeError('no type {}'.format(item))

    def position_is_valid(self, grid:'Grid.Grid', row, col):
        '''
        Defines if a position (row, col) is valid within the grid

        :param grid: a reference to :'Grid.Grid'
        :param row: row number (starting from 0)
        :param col: col number (starting from 0)
        :return: True only if the row, col position exists in the grid
        '''
        rows = grid.rows
        cols = grid.cols
        ## Linha e coluna tem que ser maior ou igual a zero e menor que o tamanho do grid
        return (row < rows) and (col < cols) and (row >= 0) and (col >= 0)

    def add_neighbors(self, grid):
        '''
        Fills the cell with references for its neighbors

        :param grid: the grid where the cell is
        :return: True if the cell type is even, False if it's odd
        '''


        #Referências mais curtas
        r = self.xpos
        c = self.ypos

        self.__neighbors = {}

        """
        a variáveç `local_nodes` é um dicionário que deve ser preenchido da seguinte forma:

        '<DIREÇÃO>' : (row_num, col_num),

        por exemplo, se a célula estiver em (5,3) a direção Leste (East) deve ser a seguinte
        'E':(6,3)
        """


        line_type = r % 2

        # Direita e esquerda independem do tipo de célula
        # Escolha das diagonais depende da linha ser par ou ímpar
        local_nodes = {
            Directions.E :(r, c+1)                             ,
            Directions.W :(r, c-1)                             ,
            Directions.NW :[(r-1, c - 1), (r-1, c)]  [line_type],
            Directions.NE :[(r-1, c)    , (r-1, c+1)][line_type],
            Directions.SW :[(r+1, c - 1), (r+1, c)]  [line_type],
            Directions.SE :[(r+1, c)    , (r+1, c+1)][line_type],
        }

        # para cada conjunto DIREÇÃO, COORDENADA
        for node_direction, node_pos  in local_nodes.items():

            # se as coordenadas forem válidas
            if self.position_is_valid(grid, node_pos[0], node_pos[1]):
                # Adicione uma referência para a célula nesta cooredenada na lista de vizinhos
                self.__neighbors[grid.get_cell(node_pos)] = node_direction
        return line_type == 0

    def show(self):
        '''
        Generates a representation of the cell
        considering the difficulty and if the cell is a wall
        :return: a char representing the cell
        '''

        #Obs: a dificuldade de cada célula deve ser um número de 0 a 1

        if self.is_wall: return '█' # Parede
        if self.difficulty < 0.25: return ' ' # dificuldades a baixo de .25
        if self.difficulty < 0.25 * 2: return '░' # dificuldades a baixo de .5
        if self.difficulty < 0.25 * 3: return '▒' #dificuldades a baixo de .75
        if self.difficulty < 0.25 * 3.999: return '▓' #dificuldades a baixo de .999...
        else: return '▲'

    def __str__(self):
        #Representação da célula como string
        return '<:Cell ({},{}); wall:{}; {}>'\
            .format(
                self.xpos,
                self.ypos,
                'T' if self.is_wall else 'F',
                self.difficulty,
                self.vars,
        )

    def directionFrom(self, to):
        if self is to:
            return None

        walk_direction = ''
        # North
        if self.xpos < to.xpos:
            walk_direction += 'N'
        # South
        elif  self.xpos >  to.xpos:
            walk_direction += 'S'
        # East
        if  self.ypos > to.ypos:
            walk_direction += 'E'
        # West
        elif self.ypos[1] < to.ypos[1]:
            walk_direction += 'W'

        return Directions.from_str(walk_direction)

    def __repr__(self):
        return self.__str__()