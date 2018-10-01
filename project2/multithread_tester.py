import subprocess
from colorama import Fore, Back, Style
from threading import Thread



confs = [
            ["(5, 5)" ,"[(1, 8), (2, 1), (4, 6)]" ,"[(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)]"],["(5, 5)" ,"[(8, 1), (9, 8), (7, 7)]" ,"[(0, 3), (0, 2), (0, 10), (4, 10), (0, 9), (0, 4), (3, 10), (0, 0), (0, 6), (9, 10), (0, 8), (2, 10), (0, 1), (7, 10), (0, 7), (0, 5), (6, 10), (1, 10)]"],["(5, 5)" ,"[(8, 3), (7, 6), (4, 2), (9, 8), (3, 8)]" ,"[(0, 6), (0, 10), (8, 10), (0, 9), (4, 10), (0, 7), (5, 10), (0, 3), (6, 10), (1, 10), (7, 10), (10, 10), (0, 0), (0, 1), (2, 10), (0, 5), (0, 8), (0, 2), (9, 10), (0, 4), (3, 10), (0, 10), (2, 10), (9, 10), (1, 10)]"],["(5, 5)" ,"[(4, 0), (5, 4)]" ,"[(0, 4), (7, 10), (5, 10), (0, 5), (1, 10), (0, 6), (0, 2), (0, 10), (2, 10), (0, 0), (8, 10), (0, 8), (0, 3), (6, 10), (0, 7), (4, 10), (3, 10), (9, 10), (0, 1), (10, 10), (0, 9), (6, 10)]"],["(5, 5)" ,"[(8, 2), (6, 2), (8, 1), (3, 2), (7, 2)]" ,"[(7, 10), (0, 8), (9, 10), (2, 10), (0, 3), (8, 10), (0, 0), (0, 7), (0, 4), (6, 10), (0, 10), (0, 6), (5, 10), (0, 5), (0, 2), (10, 10), (0, 1), (0, 9), (4, 10), (3, 10), (1, 10), (9, 10), (10, 10)]"],["(5, 5)" ,"[(3, 8), (2, 2), (10, 8)]" ,"[(0, 6), (3, 10), (9, 10), (0, 2), (10, 10), (7, 10), (0, 3), (0, 9), (0, 4), (0, 1), (0, 10), (5, 10), (0, 5), (0, 7), (8, 10), (1, 10), (6, 10), (0, 8), (4, 10), (0, 0), (2, 10), (0, 4), (3, 10), (4, 10), (5, 10)]"],["(5, 5)" ,"[(5, 3), (4, 7)]" ,"[(0, 3), (8, 10), (0, 2), (0, 8), (0, 10), (5, 10), (0, 9), (0, 7), (2, 10), (0, 1), (0, 6), (0, 4), (7, 10), (3, 10), (0, 0), (4, 10), (1, 10), (10, 10), (0, 5)]"],["(5, 5)" ,"[(10, 4), (9, 3), (7, 3), (5, 8)]" ,"[(0, 0), (1, 10), (9, 10), (0, 10), (6, 10), (0, 4), (10, 10), (0, 6), (8, 10), (7, 10), (4, 10), (0, 7), (0, 5), (0, 3), (0, 2), (0, 9)]"],["(5, 5)" ,"[(4, 6), (9, 2), (10, 1)]" ,"[(0, 10), (0, 5), (4, 10), (0, 0), (1, 10), (0, 1), (7, 10), (0, 2), (0, 7), (8, 10), (0, 3), (10, 10), (0, 8), (9, 10), (0, 6), (0, 9), (2, 10)]"],["(5, 5)" ,"[(4, 2), (7, 2), (9, 7), (3, 0)]" ,"[(3, 10), (8, 10), (1, 10), (0, 5), (6, 10), (7, 10), (10, 10), (0, 9), (0, 1), (0, 4), (0, 8), (0, 7), (0, 2), (0, 3), (2, 10), (4, 10)]"],["(5, 5)" ,"[(7, 1), (1, 6), (10, 2)]" ,"[(0, 9), (0, 4), (0, 10), (9, 10), (2, 10), (6, 10), (0, 3), (0, 7), (7, 10), (0, 0), (0, 6), (0, 8), (3, 10), (0, 2), (1, 10), (0, 1), (0, 5), (10, 10), (8, 10), (5, 10)]"],["(5, 5)" ,"[(4, 4), (8, 6)]" ,"[(0, 9), (8, 10), (0, 8), (10, 10), (0, 10), (9, 10), (1, 10), (6, 10), (3, 10), (4, 10), (0, 6), (2, 10), (7, 10), (0, 0), (0, 3)]"],["(5, 5)" ,"[(6, 3), (6, 5), (2, 0)]" ,"[(0, 8), (3, 10), (0, 10), (0, 3), (0, 5), (0, 2), (8, 10), (7, 10), (0, 9), (1, 10), (10, 10), (0, 6), (0, 0), (5, 10), (2, 10)]"],["(5, 5)" ,"[(8, 9), (6, 0)]" ,"[(10, 10), (0, 8), (0, 1), (0, 4), (0, 5), (3, 10), (2, 10), (1, 10), (8, 10), (0, 9), (4, 10), (0, 10), (0, 3), (6, 10), (0, 2), (5, 10), (7, 10), (9, 10), (0, 6), (0, 0), (0, 7), (0, 9), (7, 10), (0, 10)]"],["(5, 5)" ,"[(5, 9), (5, 3), (5, 6)]" ,"[(7, 10), (9, 10), (8, 10), (0, 8), (1, 10), (0, 6), (0, 9), (0, 5), (10, 10), (4, 10), (2, 10), (0, 2), (5, 10), (0, 0), (6, 10), (0, 7), (0, 10), (0, 3), (0, 1), (0, 4), (3, 10), (1, 10), (7, 10)]"],["(5, 5)" ,"[(5, 8), (8, 3)]" ,"[(10, 10), (0, 0), (0, 3), (8, 10), (6, 10), (0, 4), (0, 5), (5, 10), (0, 10), (0, 2), (3, 10), (2, 10), (9, 10), (0, 8), (7, 10), (0, 1), (0, 9), (1, 10), (0, 7), (0, 6), (4, 10)]"],["(5, 5)" ,"[(3, 9), (6, 0), (9, 1)]" ,"[(0, 10), (7, 10), (0, 1), (9, 10), (0, 6), (0, 0), (0, 9), (8, 10), (0, 3), (2, 10), (1, 10), (6, 10), (0, 8), (0, 5), (5, 10), (4, 10), (0, 7), (10, 10), (3, 10)]"],["(5, 5)" ,"[(10, 3), (3, 9), (9, 0)]" ,"[(8, 10), (9, 10), (0, 5), (0, 10), (0, 2), (3, 10), (7, 10), (0, 4), (0, 3), (0, 6), (2, 10), (4, 10), (6, 10), (0, 1), (0, 9), (5, 10), (0, 0), (10, 10), (0, 7), (0, 8), (1, 10), (0, 2), (0, 10), (0, 10)]"],["(5, 5)" ,"[(5, 4), (1, 9)]" ,"[(0, 9), (0, 4), (1, 10), (4, 10), (7, 10), (0, 1), (8, 10), (0, 6), (0, 5), (3, 10), (2, 10), (9, 10), (10, 10), (5, 10), (0, 8)]"],["(5, 5)" ,"[(6, 0), (3, 9), (8, 4), (2, 3)]" ,"[(0, 8), (10, 10), (1, 10), (0, 5), (0, 1), (0, 0), (0, 4), (5, 10), (0, 7), (3, 10), (0, 2), (0, 6), (0, 10), (4, 10), (9, 10), (7, 10), (8, 10), (0, 3), (0, 9), (2, 10), (6, 10), (9, 10), (0, 4)]"],["(5, 5)" ,"[(9, 1), (10, 9), (8, 8), (9, 4), (1, 1)]" ,"[(0, 8), (8, 10), (9, 10), (0, 5), (0, 7), (0, 3), (0, 10), (0, 9), (0, 6), (1, 10), (0, 2), (0, 4), (6, 10), (0, 0), (2, 10), (10, 10), (3, 10), (5, 10), (0, 1), (4, 10), (7, 10), (8, 10)]"],["(5, 5)" ,"[(2, 3), (0, 0)]" ,"[(0, 4), (0, 1), (0, 7), (0, 9), (10, 10), (0, 3), (0, 2), (4, 10), (5, 10), (0, 10), (3, 10), (2, 10), (7, 10), (8, 10), (1, 10), (0, 8)]"],["(5, 5)" ,"[(10, 7), (7, 7), (8, 6)]" ,"[(1, 10), (0, 5), (10, 10), (0, 4), (0, 2), (9, 10), (6, 10), (0, 6), (4, 10), (0, 9), (3, 10), (0, 7), (0, 8), (5, 10), (0, 10)]"],["(5, 5)" ,"[(5, 1), (2, 8), (9, 8), (3, 8), (2, 4)]" ,"[(0, 5), (0, 1), (1, 10), (6, 10), (0, 6), (2, 10), (0, 8), (9, 10), (7, 10), (0, 10), (5, 10), (0, 7), (0, 3), (8, 10), (0, 4), (3, 10), (4, 10), (0, 0), (0, 2), (10, 10), (0, 9), (0, 10), (0, 7)]"],["(5, 5)" ,"[(2, 6), (5, 1)]" ,"[(0, 0), (1, 10), (7, 10), (0, 5), (0, 3), (0, 2), (0, 7), (9, 10), (0, 10), (4, 10), (0, 6), (3, 10), (8, 10), (0, 1), (10, 10)]"],["(5, 5)" ,"[(1, 8), (1, 9), (4, 3), (10, 6), (10, 5)]" ,"[(2, 10), (10, 10), (0, 3), (8, 10), (0, 5), (0, 0), (4, 10), (0, 4), (0, 10), (3, 10), (9, 10), (0, 2), (6, 10), (0, 7), (5, 10), (0, 1), (1, 10)]"],["(5, 5)" ,"[(9, 1), (9, 2), (8, 3)]" ,"[(3, 10), (2, 10), (0, 4), (0, 9), (0, 2), (0, 8), (0, 5), (0, 7), (1, 10), (0, 10), (9, 10), (0, 0), (6, 10), (0, 6), (10, 10), (0, 1), (4, 10), (7, 10), (8, 10), (0, 3), (5, 10), (6, 10), (0, 3)]"],["(5, 5)" ,"[(4, 10), (8, 1), (1, 0), (5, 1), (6, 6)]" ,"[(0, 0), (8, 10), (0, 10), (0, 8), (7, 10), (0, 4), (6, 10), (0, 9), (5, 10), (0, 3), (0, 7), (9, 10), (3, 10), (10, 10), (2, 10), (0, 6), (0, 5)]"],["(5, 5)" ,"[(3, 3), (7, 1), (8, 5), (2, 6)]" ,"[(6, 10), (0, 1), (5, 10), (8, 10), (0, 2), (7, 10), (1, 10), (3, 10), (0, 10), (0, 5), (9, 10), (0, 0), (10, 10), (0, 6), (0, 7), (2, 10), (0, 8), (0, 9), (0, 3), (0, 4), (4, 10)]"],["(5, 5)" ,"[(3, 0), (3, 6), (4, 3), (10, 3), (8, 5)]" ,"[(6, 10), (3, 10), (0, 0), (0, 5), (7, 10), (5, 10), (1, 10), (0, 10), (0, 9), (0, 7), (0, 6), (10, 10), (8, 10), (0, 4), (0, 8), (0, 3), (9, 10), (0, 2), (2, 10), (0, 1), (4, 10), (0, 2), (10, 10)]"],["(5, 5)" ,"[(4, 5), (4, 0), (10, 9)]" ,"[(0, 9), (6, 10), (0, 3), (0, 6), (0, 5), (4, 10), (3, 10), (0, 1), (10, 10), (0, 7), (0, 10), (5, 10), (8, 10), (2, 10), (0, 2), (7, 10), (1, 10), (0, 8), (0, 0), (0, 4), (9, 10), (1, 10), (0, 8), (0, 6), (0, 9)]"],["(5, 5)" ,"[(7, 9), (2, 5), (6, 8), (10, 0), (4, 4)]" ,"[(0, 2), (6, 10), (0, 0), (3, 10), (9, 10), (0, 4), (0, 9), (10, 10), (0, 1), (0, 6), (5, 10), (0, 7), (0, 5), (0, 8), (0, 10), (2, 10), (8, 10), (4, 10), (0, 3), (1, 10), (7, 10), (3, 10), (0, 10), (7, 10)]"],["(5, 5)" ,"[(9, 6), (2, 9), (4, 7), (7, 0), (1, 1)]" ,"[(0, 3), (4, 10), (3, 10), (0, 2), (0, 9), (9, 10), (7, 10), (0, 5), (0, 6), (8, 10), (0, 1), (0, 7), (5, 10), (0, 0), (1, 10), (6, 10), (0, 8), (10, 10), (0, 4), (0, 10), (2, 10), (0, 7), (0, 8), (0, 10), (2, 10)]"],["(5, 5)" ,"[(3, 3), (6, 7), (6, 8), (8, 2), (6, 1)]" ,"[(0, 4), (0, 3), (0, 10), (7, 10), (2, 10), (0, 1), (6, 10), (10, 10), (0, 6), (0, 5), (3, 10), (0, 8), (0, 2), (4, 10), (0, 9), (9, 10), (0, 7), (8, 10), (0, 0), (5, 10), (1, 10), (9, 10), (2, 10)]"],["(5, 5)" ,"[(1, 3), (3, 9), (4, 3), (10, 5), (3, 1)]" ,"[(2, 10), (0, 6), (8, 10), (0, 5), (6, 10), (7, 10), (0, 9), (0, 0), (0, 4), (3, 10), (0, 10), (0, 3), (0, 7), (0, 1), (0, 2), (1, 10), (9, 10), (5, 10), (0, 8)]"],["(5, 5)" ,"[(4, 2), (4, 6), (6, 0)]" ,"[(4, 10), (1, 10), (7, 10), (0, 3), (10, 10), (0, 9), (0, 2), (6, 10), (9, 10), (0, 4), (2, 10), (3, 10), (0, 10), (0, 0), (0, 6)]"],["(5, 5)" ,"[(9, 3), (4, 0)]" ,"[(4, 10), (7, 10), (0, 3), (0, 10), (0, 1), (0, 9), (9, 10), (2, 10), (0, 7), (0, 2), (0, 0), (0, 4), (1, 10), (3, 10), (0, 8), (6, 10), (10, 10), (8, 10), (0, 5), (0, 6), (5, 10)]"],["(5, 5)" ,"[(1, 3), (6, 4), (5, 7), (2, 9)]" ,"[(5, 10), (2, 10), (0, 4), (1, 10), (0, 0), (0, 7), (3, 10), (0, 5), (0, 9), (9, 10), (0, 1), (7, 10), (4, 10), (0, 10), (0, 2)]"],["(5, 5)" ,"[(2, 5), (8, 8), (1, 9)]" ,"[(9, 10), (1, 10), (10, 10), (0, 0), (0, 9), (0, 10), (0, 1), (0, 6), (0, 4), (0, 2), (8, 10), (6, 10), (0, 5), (4, 10), (0, 7), (3, 10), (2, 10), (5, 10)]"],["(5, 5)" ,"[(9, 8), (5, 9), (10, 4)]" ,"[(0, 6), (0, 8), (1, 10), (0, 0), (8, 10), (9, 10), (0, 5), (0, 3), (10, 10), (7, 10), (5, 10), (6, 10), (4, 10), (0, 10), (0, 2), (2, 10), (3, 10), (0, 7), (0, 9), (0, 1), (0, 4), (4, 10), (0, 7)]"],["(5, 5)" ,"[(6, 0), (8, 7)]" ,"[(6, 10), (10, 10), (0, 10), (0, 6), (8, 10), (0, 2), (0, 9), (1, 10), (5, 10), (0, 4), (0, 8), (9, 10), (0, 1), (4, 10), (3, 10), (7, 10), (0, 3), (0, 5), (0, 0), (2, 10), (0, 7), (6, 10), (3, 10), (0, 10)]"],["(5, 5)" ,"[(2, 3), (2, 9), (5, 9), (7, 3), (4, 6)]" ,"[(6, 10), (1, 10), (0, 0), (5, 10), (8, 10), (10, 10), (3, 10), (4, 10), (0, 3), (0, 6), (0, 4), (0, 7), (0, 8), (7, 10), (9, 10), (2, 10), (0, 9), (0, 1), (0, 10), (0, 2), (0, 5)]"],["(5, 5)" ,"[(2, 5), (7, 7), (2, 8), (7, 2)]" ,"[(0, 10), (0, 8), (0, 9), (8, 10), (1, 10), (7, 10), (0, 4), (10, 10), (0, 6), (6, 10), (0, 3), (9, 10), (3, 10), (5, 10), (0, 1), (0, 5), (0, 2), (2, 10), (4, 10), (0, 7), (0, 0)]"],["(5, 5)" ,"[(2, 5), (4, 4)]" ,"[(6, 10), (0, 7), (8, 10), (0, 0), (9, 10), (0, 6), (0, 10), (0, 4), (0, 3), (1, 10), (0, 8), (7, 10), (2, 10), (0, 9), (10, 10), (0, 2), (5, 10)]"],["(5, 5)" ,"[(6, 7), (6, 4), (1, 1), (5, 2)]" ,"[(0, 8), (10, 10), (0, 2), (3, 10), (0, 7), (2, 10), (0, 1), (0, 6), (0, 3), (0, 10), (0, 4), (0, 9), (4, 10), (6, 10), (0, 0), (8, 10), (7, 10), (5, 10), (0, 5), (1, 10), (9, 10)]"],["(5, 5)" ,"[(9, 0), (5, 9), (6, 6), (9, 3)]" ,"[(7, 10), (0, 10), (0, 5), (0, 9), (0, 8), (0, 2), (10, 10), (0, 1), (0, 3), (2, 10), (5, 10), (0, 0), (6, 10), (8, 10), (1, 10)]"],["(5, 5)" ,"[(4, 5), (2, 8), (3, 2)]" ,"[(0, 6), (0, 4), (0, 3), (10, 10), (0, 5), (4, 10), (0, 8), (8, 10), (2, 10), (7, 10), (1, 10), (0, 9), (5, 10), (0, 10), (3, 10), (9, 10), (0, 7)]"],["(5, 5)" ,"[(7, 3), (1, 2), (7, 8), (2, 4), (10, 1)]" ,"[(6, 10), (0, 0), (7, 10), (0, 2), (2, 10), (4, 10), (3, 10), (0, 10), (5, 10), (0, 7), (8, 10), (0, 3), (10, 10), (0, 9), (0, 4), (0, 5), (0, 1), (1, 10), (0, 6), (0, 8), (9, 10), (0, 5), (5, 10), (0, 8), (0, 10)]"],["(5, 5)" ,"[(4, 6), (2, 3), (5, 2)]" ,"[(0, 4), (0, 2), (0, 10), (0, 8), (0, 9), (9, 10), (5, 10), (3, 10), (0, 7), (8, 10), (0, 0), (0, 5), (6, 10), (0, 6), (10, 10), (0, 1), (1, 10), (7, 10), (2, 10), (0, 3), (4, 10), (0, 5), (0, 0), (4, 10), (0, 4)]"],["(5, 5)" ,"[(3, 3), (2, 2), (2, 9)]" ,"[(0, 8), (0, 4), (0, 2), (8, 10), (9, 10), (0, 3), (6, 10), (0, 1), (3, 10), (0, 7), (7, 10), (0, 9), (10, 10), (0, 6), (2, 10), (0, 0)]"],["(5, 5)" ,"[(6, 5), (1, 7), (2, 5)]" ,"[(6, 10), (9, 10), (0, 4), (7, 10), (4, 10), (0, 7), (0, 5), (10, 10), (0, 3), (0, 10), (0, 1), (3, 10), (0, 2), (5, 10), (0, 0), (2, 10), (0, 8), (1, 10), (0, 9), (8, 10), (0, 6), (4, 10), (0, 4), (7, 10), (0, 3)]"],["(5, 5)" ,"[(4, 4), (2, 3)]" ,"[(1, 10), (5, 10), (6, 10), (0, 3), (0, 10), (0, 1), (0, 0), (0, 4), (0, 7), (10, 10), (0, 9), (0, 5), (4, 10), (2, 10), (7, 10), (3, 10), (0, 6), (0, 8), (8, 10), (0, 2), (9, 10), (0, 2), (2, 10), (0, 3)]"],["(5, 5)" ,"[(9, 3), (6, 7)]" ,"[(0, 6), (10, 10), (2, 10), (7, 10), (0, 9), (0, 10), (3, 10), (0, 0), (0, 3), (5, 10), (0, 8), (0, 1), (0, 4), (1, 10), (0, 2), (6, 10), (9, 10), (4, 10), (0, 7), (8, 10)]"],["(5, 5)" ,"[(10, 5), (10, 4), (2, 6), (10, 9), (3, 3)]" ,"[(0, 8), (0, 6), (5, 10), (0, 1), (1, 10), (0, 7), (0, 2), (4, 10), (0, 3), (0, 4), (8, 10), (6, 10), (0, 10), (0, 5), (2, 10), (3, 10), (7, 10), (0, 0), (0, 9), (9, 10), (10, 10), (0, 8)]"],["(5, 5)" ,"[(9, 0), (1, 7), (3, 7), (6, 2), (7, 7)]" ,"[(6, 10), (9, 10), (2, 10), (5, 10), (0, 2), (0, 9), (0, 6), (0, 1), (4, 10), (7, 10), (0, 0), (0, 8), (0, 10), (8, 10), (3, 10), (0, 3), (10, 10), (1, 10), (0, 7), (0, 5), (0, 4), (10, 10), (0, 10), (0, 4)]"],["(5, 5)" ,"[(1, 0), (5, 3), (8, 1)]" ,"[(0, 4), (4, 10), (2, 10), (0, 7), (0, 10), (10, 10), (6, 10), (5, 10), (8, 10), (9, 10), (0, 9), (0, 0), (0, 1), (7, 10), (0, 8), (0, 6), (0, 3), (3, 10), (1, 10), (0, 5), (0, 2), (10, 10), (0, 6), (0, 4), (0, 10)]"],["(5, 5)" ,"[(6, 9), (3, 3), (5, 4)]" ,"[(8, 10), (3, 10), (0, 1), (0, 10), (0, 4), (4, 10), (5, 10), (6, 10), (0, 5), (9, 10), (0, 9), (10, 10), (2, 10), (1, 10), (0, 3), (0, 8)]"],["(5, 5)" ,"[(7, 2), (6, 9)]" ,"[(0, 3), (6, 10), (1, 10), (0, 6), (0, 10), (8, 10), (4, 10), (2, 10), (7, 10), (0, 0), (10, 10), (0, 5), (3, 10), (9, 10), (0, 7), (0, 8), (0, 1), (0, 2), (0, 4), (5, 10), (0, 9), (0, 4)]"],["(5, 5)" ,"[(8, 1), (7, 1)]" ,"[(0, 9), (6, 10), (0, 10), (3, 10), (0, 3), (4, 10), (0, 7), (0, 1), (10, 10), (1, 10), (2, 10), (0, 2), (8, 10), (7, 10), (0, 4), (9, 10), (0, 8), (0, 5), (0, 6), (5, 10), (0, 0), (0, 4), (10, 10), (0, 1), (0, 0)]"],["(5, 5)" ,"[(7, 9), (1, 5)]" ,"[(7, 10), (4, 10), (0, 5), (6, 10), (10, 10), (0, 3), (0, 9), (0, 8), (5, 10), (0, 0), (1, 10), (0, 1), (8, 10), (0, 4), (2, 10), (0, 7)]"],["(5, 5)" ,"[(9, 4), (7, 0), (3, 7)]" ,"[(0, 9), (0, 8), (0, 5), (10, 10), (0, 6), (6, 10), (0, 7), (0, 4), (0, 0), (1, 10), (0, 1), (0, 10), (7, 10), (9, 10), (8, 10), (2, 10), (0, 2), (4, 10)]"],["(5, 5)" ,"[(7, 5), (9, 7), (10, 0)]" ,"[(0, 10), (0, 9), (10, 10), (9, 10), (2, 10), (0, 7), (0, 6), (0, 8), (0, 3), (6, 10), (3, 10), (0, 4), (4, 10), (0, 2), (7, 10)]"],["(5, 5)" ,"[(6, 7), (10, 0), (1, 6), (9, 1), (2, 4)]" ,"[(0, 1), (0, 3), (0, 5), (2, 10), (0, 9), (7, 10), (5, 10), (0, 10), (0, 0), (6, 10), (1, 10), (3, 10), (0, 8), (0, 4), (8, 10), (9, 10), (10, 10), (4, 10), (0, 6), (0, 7)]"],["(5, 5)" ,"[(9, 5), (10, 4)]" ,"[(0, 5), (9, 10), (10, 10), (0, 10), (0, 2), (4, 10), (0, 3), (5, 10), (7, 10), (1, 10), (2, 10), (6, 10), (0, 1), (0, 9), (0, 6), (0, 8), (0, 0)]"],["(5, 5)" ,"[(6, 1), (2, 9)]" ,"[(0, 2), (0, 8), (0, 7), (5, 10), (1, 10), (3, 10), (8, 10), (0, 10), (0, 3), (0, 4), (9, 10), (0, 6), (0, 5), (6, 10), (10, 10), (2, 10), (0, 9), (4, 10), (0, 1), (7, 10), (0, 0), (0, 5)]"],["(5, 5)" ,"[(2, 5), (7, 3), (4, 5), (9, 1)]" ,"[(3, 10), (9, 10), (10, 10), (8, 10), (0, 4), (4, 10), (5, 10), (0, 3), (2, 10), (0, 6), (7, 10), (0, 7), (1, 10), (0, 1), (0, 2), (0, 10)]"],["(5, 5)" ,"[(10, 6), (9, 5), (4, 3), (9, 9), (6, 4)]" ,"[(0, 1), (0, 3), (7, 10), (0, 10), (9, 10), (1, 10), (0, 4), (0, 2), (0, 7), (8, 10), (4, 10), (5, 10), (0, 5), (3, 10), (0, 8), (2, 10), (6, 10), (10, 10), (0, 0), (0, 6)]"],["(5, 5)" ,"[(10, 5), (10, 6), (1, 3), (2, 9)]" ,"[(10, 10), (0, 5), (0, 2), (9, 10), (0, 6), (0, 9), (7, 10), (0, 1), (2, 10), (8, 10), (0, 3), (1, 10), (0, 10), (0, 0), (0, 7), (6, 10), (5, 10), (0, 4), (4, 10), (0, 8), (3, 10), (0, 1), (0, 1), (0, 0)]"],["(5, 5)" ,"[(10, 0), (7, 8)]" ,"[(6, 10), (4, 10), (0, 5), (2, 10), (0, 0), (0, 9), (8, 10), (0, 1), (0, 4), (0, 6), (0, 10), (3, 10), (5, 10), (0, 7), (1, 10), (7, 10), (9, 10), (10, 10), (0, 8), (0, 2)]"],["(5, 5)" ,"[(7, 7), (7, 0), (10, 4), (10, 3)]" ,"[(8, 10), (7, 10), (9, 10), (5, 10), (1, 10), (0, 2), (3, 10), (10, 10), (0, 1), (4, 10), (0, 6), (0, 5), (0, 8), (0, 10), (0, 0), (0, 4), (0, 7), (0, 9), (2, 10)]"],["(5, 5)" ,"[(6, 3), (5, 6), (7, 2), (6, 0)]" ,"[(0, 0), (10, 10), (0, 9), (8, 10), (0, 7), (6, 10), (0, 6), (0, 4), (0, 3), (0, 2), (3, 10), (0, 5), (1, 10), (9, 10), (7, 10), (2, 10), (0, 1), (0, 8), (0, 10), (4, 10), (5, 10), (0, 4)]"],["(5, 5)" ,"[(1, 5), (5, 1)]" ,"[(0, 10), (0, 5), (0, 8), (0, 0), (6, 10), (8, 10), (7, 10), (4, 10), (2, 10), (10, 10), (3, 10), (0, 1), (0, 6), (0, 3), (0, 4), (9, 10), (0, 2), (1, 10), (0, 7), (0, 9)]"],["(5, 5)" ,"[(3, 0), (10, 1)]" ,"[(10, 10), (9, 10), (0, 1), (0, 2), (0, 10), (7, 10), (8, 10), (0, 0), (0, 6), (0, 5), (6, 10), (2, 10), (0, 3), (0, 8), (4, 10), (0, 4)]"],["(5, 5)" ,"[(7, 4), (5, 3), (2, 8), (2, 9), (10, 7)]" ,"[(0, 9), (0, 7), (0, 6), (9, 10), (8, 10), (0, 4), (6, 10), (0, 10), (4, 10), (2, 10), (3, 10), (0, 2), (0, 5), (7, 10), (5, 10), (10, 10), (0, 3), (0, 0), (0, 1)]"],["(5, 5)" ,"[(5, 3), (4, 2)]" ,"[(0, 10), (2, 10), (0, 8), (0, 4), (1, 10), (8, 10), (7, 10), (5, 10), (9, 10), (0, 1), (0, 5), (0, 6), (4, 10), (3, 10), (0, 2), (0, 9), (10, 10), (0, 0), (0, 3), (6, 10), (0, 7), (5, 10)]"],["(5, 5)" ,"[(4, 4), (9, 6)]" ,"[(9, 10), (0, 0), (1, 10), (7, 10), (0, 8), (4, 10), (0, 7), (8, 10), (10, 10), (0, 4), (0, 2), (5, 10), (0, 9), (2, 10), (0, 6), (0, 5)]"],["(5, 5)" ,"[(1, 2), (8, 1), (8, 0)]" ,"[(0, 1), (0, 10), (0, 5), (10, 10), (7, 10), (0, 2), (9, 10), (0, 0), (0, 4), (0, 8), (3, 10), (0, 7), (6, 10), (8, 10), (0, 6), (0, 3), (0, 9), (2, 10), (1, 10), (5, 10), (4, 10), (0, 6), (0, 10)]"],["(5, 5)" ,"[(7, 0), (2, 1), (10, 1)]" ,"[(6, 10), (10, 10), (9, 10), (0, 4), (0, 2), (0, 3), (0, 7), (0, 9), (0, 0), (0, 5), (2, 10), (3, 10), (0, 6), (7, 10), (1, 10), (0, 8), (0, 10), (0, 1), (8, 10), (5, 10)]"],["(5, 5)" ,"[(4, 5), (3, 7)]" ,"[(7, 10), (3, 10), (0, 3), (0, 9), (0, 2), (0, 10), (0, 5), (0, 1), (0, 7), (1, 10), (6, 10), (2, 10), (8, 10), (0, 8), (0, 4), (0, 6), (0, 0), (9, 10), (10, 10), (5, 10), (4, 10), (3, 10), (7, 10), (0, 8), (7, 10)]"],["(5, 5)" ,"[(8, 7), (8, 4), (3, 1)]" ,"[(6, 10), (0, 1), (2, 10), (0, 10), (3, 10), (0, 4), (0, 6), (5, 10), (0, 7), (9, 10), (10, 10), (0, 2), (0, 5), (1, 10), (4, 10), (7, 10)]"],["(5, 5)" ,"[(6, 6), (7, 0), (1, 10)]" ,"[(0, 3), (6, 10), (2, 10), (0, 5), (0, 1), (0, 0), (0, 10), (0, 4), (10, 10), (9, 10), (0, 7), (0, 6), (0, 9), (5, 10), (4, 10)]"],["(5, 5)" ,"[(9, 1), (2, 0), (5, 9)]" ,"[(0, 0), (4, 10), (9, 10), (10, 10), (0, 9), (1, 10), (0, 6), (6, 10), (0, 10), (0, 8), (7, 10), (0, 5), (8, 10), (0, 7), (0, 3), (0, 1), (0, 2), (3, 10)]"],["(5, 5)" ,"[(5, 9), (6, 3), (6, 9), (1, 0), (1, 2)]" ,"[(7, 10), (0, 0), (0, 2), (2, 10), (0, 10), (0, 6), (0, 5), (5, 10), (9, 10), (4, 10), (0, 9), (8, 10), (3, 10), (0, 1), (10, 10), (0, 8), (0, 4), (0, 3), (1, 10), (0, 7), (6, 10), (0, 7), (4, 10)]"],["(5, 5)" ,"[(9, 9), (4, 9)]" ,"[(0, 1), (0, 2), (0, 6), (0, 4), (0, 9), (7, 10), (0, 0), (0, 7), (8, 10), (3, 10), (4, 10), (0, 10), (10, 10), (0, 5), (1, 10), (2, 10), (5, 10), (9, 10), (0, 8), (0, 3), (6, 10), (0, 5), (9, 10)]"],["(5, 5)" ,"[(8, 6), (7, 7), (6, 6)]" ,"[(0, 5), (6, 10), (0, 6), (0, 2), (0, 1), (0, 4), (4, 10), (8, 10), (0, 9), (0, 7), (7, 10), (0, 3), (3, 10), (1, 10), (2, 10), (0, 10), (9, 10), (0, 8), (5, 10), (10, 10), (0, 0)]"],["(5, 5)" ,"[(6, 8), (5, 2), (8, 8), (9, 3)]" ,"[(10, 10), (1, 10), (0, 3), (8, 10), (0, 6), (3, 10), (0, 10), (0, 7), (0, 0), (0, 4), (4, 10), (0, 5), (2, 10), (6, 10), (7, 10), (0, 9), (9, 10), (5, 10), (0, 1), (0, 2), (0, 8), (0, 9), (0, 8)]"],["(5, 5)" ,"[(1, 3), (4, 3), (1, 2)]" ,"[(5, 10), (0, 8), (4, 10), (0, 7), (0, 4), (3, 10), (0, 10), (0, 5), (2, 10), (0, 3), (6, 10), (0, 9), (9, 10), (10, 10), (8, 10), (0, 1), (1, 10), (0, 6), (0, 0), (0, 2), (7, 10), (3, 10), (0, 4)]"],["(5, 5)" ,"[(2, 4), (8, 9), (4, 1), (9, 0), (10, 6)]" ,"[(0, 8), (0, 10), (0, 6), (7, 10), (5, 10), (0, 5), (1, 10), (0, 9), (0, 4), (0, 2), (9, 10), (2, 10), (4, 10), (0, 1), (0, 7), (0, 3), (6, 10)]"],["(5, 5)" ,"[(10, 5), (10, 1), (4, 5), (10, 0), (2, 5)]" ,"[(0, 2), (4, 10), (8, 10), (2, 10), (0, 0), (1, 10), (10, 10), (0, 10), (5, 10), (0, 4), (6, 10), (0, 7), (0, 6), (0, 9), (0, 5), (7, 10), (0, 1), (9, 10), (0, 8), (3, 10), (0, 3), (0, 6), (4, 10)]"],["(5, 5)" ,"[(1, 0), (3, 5), (9, 3)]" ,"[(0, 3), (7, 10), (6, 10), (0, 2), (5, 10), (0, 1), (0, 10), (4, 10), (10, 10), (0, 7), (0, 6), (3, 10), (8, 10), (0, 0), (9, 10), (0, 9), (1, 10), (2, 10), (0, 4), (0, 5), (0, 8)]"],["(5, 5)" ,"[(3, 2), (1, 1)]" ,"[(0, 10), (0, 5), (0, 8), (8, 10), (0, 6), (0, 9), (10, 10), (2, 10), (0, 1), (5, 10), (1, 10), (6, 10), (0, 3), (0, 4), (4, 10), (3, 10), (0, 7)]"],["(5, 5)" ,"[(8, 6), (3, 1), (8, 3), (10, 5), (1, 9)]" ,"[(0, 9), (0, 10), (0, 3), (0, 0), (0, 5), (0, 2), (10, 10), (0, 6), (0, 7), (9, 10), (7, 10), (1, 10), (8, 10), (0, 1), (0, 8), (3, 10), (4, 10), (0, 4), (2, 10), (5, 10), (6, 10), (5, 10), (3, 10)]"],["(5, 5)" ,"[(4, 5), (3, 5), (9, 5), (7, 3), (1, 5)]" ,"[(3, 10), (0, 8), (0, 10), (2, 10), (0, 4), (8, 10), (0, 6), (5, 10), (10, 10), (7, 10), (1, 10), (4, 10), (6, 10), (0, 3), (0, 0), (0, 2), (0, 7)]"],["(5, 5)" ,"[(7, 4), (9, 2)]" ,"[(0, 8), (0, 10), (0, 9), (0, 0), (0, 4), (9, 10), (0, 6), (5, 10), (0, 3), (0, 2), (0, 5), (6, 10), (7, 10), (2, 10), (1, 10), (0, 7), (4, 10), (0, 1), (8, 10), (3, 10), (10, 10), (5, 10), (6, 10), (0, 7)]"],["(5, 5)" ,"[(8, 3), (10, 3), (3, 5), (8, 6)]" ,"[(0, 7), (3, 10), (2, 10), (0, 3), (7, 10), (0, 2), (5, 10), (0, 4), (0, 6), (9, 10), (0, 5), (0, 10), (8, 10), (1, 10), (10, 10), (0, 0), (6, 10), (0, 9), (0, 8), (0, 1), (4, 10), (0, 10), (0, 10)]"],["(5, 5)" ,"[(8, 9), (8, 2), (6, 7)]" ,"[(0, 10), (0, 9), (0, 3), (10, 10), (9, 10), (0, 0), (6, 10), (0, 5), (3, 10), (0, 4), (4, 10), (0, 7), (0, 6), (2, 10), (5, 10), (0, 1), (0, 8), (0, 2), (8, 10), (1, 10), (7, 10), (0, 2), (0, 1), (7, 10)]"],["(5, 5)" ,"[(4, 9), (9, 0), (1, 6)]" ,"[(0, 8), (0, 10), (0, 7), (6, 10), (7, 10), (0, 9), (0, 5), (0, 1), (9, 10), (0, 3), (3, 10), (5, 10), (8, 10), (1, 10), (0, 0), (10, 10), (2, 10)]"],["(5, 5)" ,"[(2, 1), (8, 7), (4, 7), (3, 8)]" ,"[(10, 10), (0, 1), (0, 2), (8, 10), (1, 10), (0, 3), (0, 10), (0, 7), (3, 10), (0, 9), (5, 10), (2, 10), (0, 5), (4, 10), (0, 8), (7, 10), (0, 4), (9, 10), (6, 10), (0, 6), (0, 0), (0, 3)]"],["(5, 5)" ,"[(2, 9), (7, 3), (9, 3), (7, 7), (2, 7)]" ,"[(5, 10), (0, 10), (0, 8), (0, 5), (2, 10), (0, 9), (0, 0), (7, 10), (0, 1), (6, 10), (0, 7), (8, 10), (0, 6), (1, 10), (4, 10), (10, 10)]"],["(5, 5)" ,"[(8, 6), (3, 2)]" ,"[(0, 0), (8, 10), (0, 4), (5, 10), (4, 10), (0, 5), (0, 3), (10, 10), (6, 10), (2, 10), (0, 1), (0, 9), (1, 10), (0, 8), (7, 10), (9, 10), (3, 10), (0, 10), (0, 6), (0, 2), (0, 7), (0, 6), (3, 10)]"]
         ]


def split_list(alist, wanted_parts = 1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]

class CatcherTester(Thread):
    def __init__(self, tid, tname, confs, conf_start):
        Thread.__init__(self)
        self.tid = tid
        self.tname = tname
        self.results = []
        self.confs = confs
        self.conf_start = conf_start


    def run(self):
        conf_count = self.conf_start
        successes = 0
        fails = 0

        for conf in self.confs:
            game_output = \
            subprocess.Popen(
            [
                'python',
                'game.py',
                conf[0],
                conf[1],
                conf[2]
            ],stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()

            colorama_color = Fore.GREEN if game_output == '1' else Fore.RED
            if game_output == '1':
                successes += 1
            else:
                fails += 1

            print('[{}] {} [conf{:03}] [  RESULT: {} ] {} [...]'.format(self.tname ,colorama_color, conf_count, game_output, Style.RESET_ALL))
            self.results.append({'result': game_output, 'conf': 'conf{:03}'.format(conf_count),'conf_num':conf_count , 'thread' : self.tname})
            conf_count += 1


def thread_creator(confs, threads):
    splitted_lists = split_list(confs, threads)
    created_threads = []
    t_count = 0
    arr_size_acum = 0

    for sub_list in splitted_lists:
        thread = CatcherTester(t_count, 'Thread#{:03}'.format(t_count), sub_list, arr_size_acum)
        arr_size_acum += len(sub_list)
        t_count += 1
        created_threads.append(thread)
        thread.start()

    joined_results = []
    for t in created_threads:
        t.join()
        print('THREAD `{}` ENDED'.format(t.tname))
        joined_results.extend(t.results)

    joined_results = sorted(joined_results, key=lambda elem: elem['conf_num'], reverse=False)

    print('\n\n' + '=' * 100 + '\n\n')

    success_count = 0
    fail_count = 0
    for result in joined_results:
        game_output = result['result']
        colorama_color = Fore.GREEN if game_output == '1' else Fore.RED

        success_count += 1 if game_output == '1' else 0
        fail_count += 1 if game_output == '0' else 0

        print('[{}] {} [{}] [ RESULT: {} ] {}'
              .format(
                result['thread'],
                colorama_color,
                result['conf'],
                result['result'],
                Style.RESET_ALL
                )
            )

    print('\n\n')
    print('{}\tSUCCESSES: {}{}'.format(Fore.GREEN, success_count, Style.RESET_ALL))
    print('{}\tFAILS: {}{}'.format(Fore.RED, fail_count, Style.RESET_ALL))
    print('\tTOTAL: {}'.format(success_count + fail_count))


#thread_creator([confs[0]], 1)#Tests first only
#thread_creator([confs[0:len(confs)//4]], 4)#Tests first 25% only
thread_creator(confs, 4)#Tests all