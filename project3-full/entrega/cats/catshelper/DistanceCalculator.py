from enum import Enum
from math import sqrt

D = 1 #Minimum cost to move in straight line
D2 = sqrt(2) #Minimum cost to move diagonally

def dx(x0, x1):
    return abs(x0 - x1)

def dy(y0, y1):
    return abs(y0 - y1)

#DIAGONAL DISTANCE - FOR 8 DIRECTION MOVEMENT
def diagonal(x0, y0, x1, y1):
    _dx = dx(x0, x1)
    _dy = dy(y0, y1)
    return D * (_dx + _dy) + (D2 - 2 * D) * min(_dx, _dy)

#MANHATTAN DISTANCE / MAXIMUM DISTANCE - FOR 4 DIRECTION MOVEMENT (NO DIAGONALS)
def manhattan(x0, y0, x1, y1):
    _dx = dx(x0, x1)
    _dy = dy(y0, y1)
    return D * (_dx + _dy)

def maximum(x0, y0, x1, y1):
    return manhattan(x0, y0, x1, y1)

#EUCLIDEAN DISTANCE - FOR 8 OR MORE DIRECTION MOVEMENT (GRAPHS)
def euclidean(x0, y0, x1, y1):
    _dx = dx(x0, x1)
    _dy = dy(y0, y1)
    return D * sqrt((_dx ** 2) + (_dy ** 2))


#CHEBYSHEV DISTANCE - FOR 8 DIRECTION MOVEMENT (?)
#TODO: FOR 8 DIRECTION MOVEMENT?
def chebyshev(x0, y0, x1, y1):
    _dx = dx(x0, x1)
    _dy = dy(y0, y1)
    return D * max(_dx, _dy)



#q é col


def cube_distance(ax, ay, az, bx, by, bz):
    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2

def axial_to_cube(q, r):
    x = r
    z = q
    y = -x - z
    return (x, y, z)

#HEXAGONAL DISTANCE - FOR HEXAGONAL TILES
def hex_distance(x0, y0, x1, y1):
    first = axial_to_cube(x0, y0)
    second =axial_to_cube(x1, y1)
    return cube_distance(first[0], first[1], first[2], second[0], second[1], second[2])


#def cube_distance2(a, b):
#    return max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z))
#
#def hex_distance2(a, b):
#    ac = axial_to_cube(a)
#    bc = axial_to_cube(b)
#    return cube_distance(ac, bc)
#
#
#def hex_distance3(a, b):
#    return (abs(a.q - b.q)
#          + abs(a.q + a.r - b.q - b.r)
#          + abs(a.r - b.r)) / 2
#
#def offset_distance(a, b):
#    ac = offset_to_cube(a)
#    bc = offset_to_cube(b)
#    return cube_distance(ac, bc)
#
#def cube_to_axial(cube):
#    q = cube.x
#    r = cube.z
#    return (q, r)



#Distance Types
class DistanceTypes(Enum):
    MANHATTAN = lambda ax, ay, bx, by   : manhattan   (ax, ay, bx, by)
    EUCLIDEAN = lambda ax, ay, bx, by   : euclidean   (ax, ay, bx, by)
    DIAGONAL  = lambda ax, ay, bx, by   : diagonal    (ax, ay, bx, by)
    MAXIMUM   = lambda ax, ay, bx, by   : maximum     (ax, ay, bx, by)
    CHEBYSHEV = lambda ax, ay, bx, by   : chebyshev   (ax, ay, bx, by)
    HEX       = lambda ax, ay, bx, by   : hex_distance (ax, ay, bx, by)

#Distance Calculator
class Distance2DCalculator:
    def __init__(self, method: DistanceTypes = DistanceTypes.EUCLIDEAN):
        self.method = method

    def distCoords(self, ax, ay, bx, by):
        return self.method(ax, ay, bx, by)

    def distCell(self, firstCell, secondCell):
        return self.method(firstCell.xpos, firstCell.ypos, secondCell.xpos, secondCell.ypos)
