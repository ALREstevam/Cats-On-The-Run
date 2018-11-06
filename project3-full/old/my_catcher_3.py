import sys


SHOW_EXCEPTIONS = True
RECORD_LOG = False
TESTING = False

if TESTING:

    print('YOU ARE IN TESTING MODE!!!', file=sys.stderr)

    cat    = (5,5)
    walls = [(2, 8), (2, 1), (7, 7), (4, 7), (6, 5), (4, 5)]
    goals  = [(4, 10), (0, 5), (0, 10), (3, 10), (7, 10), (0, 3), (0, 2), (0, 1), (0, 8), (6, 10), (0, 9), (10, 10), (8, 10), (0, 0), (0, 4), (2, 10), (5, 10), (1, 10), (0, 7), (0, 6), (9, 10), (9, 10), (0, 6), (2, 10), (9, 10)]
else:
    cat = eval(sys.argv[1])
    walls = eval(sys.argv[2])
    goals = eval(sys.argv[3])



def catch(cat, walls, goals):
    import scores_calculator_catcher

    sc2 = scores_calculator_catcher.ScoreCalculator(walls=walls, goals=goals, cat=cat)

    sc2.scores()

    print(
        max( sc2.grid.as_list(),
             key= lambda elem :
             -10 if elem.is_wall or elem.pos == cat else elem.score
             ).pos
    )


catch(cat, walls, goals)


