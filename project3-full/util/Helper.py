class Helper:
    #@staticmethod
    #def valid_goals(goals, walls, cat_pos):
    #    return [goal for goal in goals if goal not in walls and goal != cat_pos]

    @staticmethod
    def count(full_elements, needles) -> int:
        counts = 0
        needles = set(needles)
        for elem in full_elements:
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
    def average(lst) -> float:
        return sum(lst) / float(len(lst))

    @staticmethod
    def minimum_elements(lst, required_elements=1) -> float:
        lst.sort()
        return lst[0:min([len(lst), required_elements])]

    @staticmethod
    def minimum_average(lst, max_elements=1) -> float:
        true_elems = Helper.minimum_elements(lst, max_elements)
        if len(true_elems) == 0:
            return 0
        return sum(true_elems) / float(len(true_elems))


    @staticmethod
    def candidate_neibs(xy):
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

    @staticmethod
    def neibs_pos(rowcol, walls, cat, exclude_non_walkable = True) -> list:
        '''
        Obtém a posição de vizinhos válidos
        '''
        candidates = Helper.candidate_neibs(rowcol)
        if exclude_non_walkable:
            used = walls.copy()
            used.add(cat)
            candidates = [elem for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10 and elem not in used]
        else:
            candidates = [elem for elem in candidates if elem[0] >= 0 and elem[0] <= 10 and elem[1] >= 0 and elem[1] <= 10]
        return candidates


    @staticmethod
    def valid_goals(goals, walls):
        return [goal for goal in goals if goal not in walls]

    @staticmethod
    def count_lead_goals(cell, goals, walls, cat):
        if cell in walls or cell == cat:
            return 0
        neibs = Helper.neibs_pos(cell, walls, cat, True)
        valid_goals = Helper.valid_goals(goals, walls)

        valid_goal_count = .5 if cell in valid_goals else 0

        for neib in neibs:
            if neib in valid_goals:
                valid_goal_count += 1

        if valid_goal_count >= 3:
            valid_goal_count = 3

        return valid_goal_count

    @staticmethod
    def in_diamond(pos):
        diamond_cells = (
            (2,2), (0, 3), (1, 2), (3, 1), (4, 1), (5, 0), (6, 1), (7, 1), (8, 2), (9, 2),
            (10, 3), (9, 5), (10, 8), (9, 8), (8, 9), (7, 9), (6, 10), (5, 9), (4, 10),
            (3, 9), (2, 9), (1, 8), (0, 8), (1, 5)
        )
        return 1 if pos in diamond_cells else 0


    @staticmethod
    def walkables_around(pos, cat, walls):
        return len(Helper.neibs_pos(pos, walls, cat, True))

    @staticmethod
    def is_between(value, min_fence, max_fence, inclusive_min=True, inclusive_max=False):
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

    @staticmethod
    def position_is_valid(pos):
        return pos[0] >= 0 and pos[0] <= 10 and pos[1] >= 0 and pos[1] <= 10


Help = Helper()