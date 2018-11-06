import sys

import scores_calculator_cat

cat    = (5,5)
walls = set([(2, 8), (2, 1), (4, 6), (7, 7), (4,7), (6,5)])
goals  = set([(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)])


cat     = eval(sys.argv[1])
walls   = set(eval(sys.argv[2]))
goals   = set(eval(sys.argv[3]))

def score_calc(s1_pathlen, s2_min_hits, s3_path_dif, s4_local_dif, s5_near_goal):
    return s2_min_hits

def walk(cat, walls, goals):
    sc2 = scores_calculator_cat.ScoreCalculator(walls=walls, goals=goals, diff_spred_steps=2)

    try:
        sc2.scores()

        cat_neibs = sc2.grid.get_cell(cat).neibs

        print(
        cat_neibs[max(cat_neibs,
                      key= lambda elem: elem.score if not elem.is_wall else -1)]
        )

    except Exception:
        sys.exit()


walk(cat, walls, goals)


