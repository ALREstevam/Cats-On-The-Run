import sys
import random
import subprocess
from PIL import Image, ImageDraw
from grid.Grid import Grid
import json

#############################################################################
from grid.Grid import Grid
from cats.astarcat.AstarCat import AstarCat
from cats.bfscat.BreadthFirstSearchCat import BreadthFirstSearchCat
from cats.bestfirstcat.BestFirstCat import BestFirstSearchCat
from pprint import pprint
import math
from cats.catshelper.DistanceCalculator import DistanceTypes
from cats.CatFather import Solution
import operator
from cats.catshelper.DistanceCalculator import Distance2DCalculator
import beep_test
#############################################################################


DEBUG     = True
ANIMATION = True

with open('result.json', 'w') as file:
    json.dump([], file)

cat    = eval(sys.argv[1])
blocks = eval(sys.argv[2])
exits  = eval(sys.argv[3])
conf_name  = str(sys.argv[4])

catcher_path = 'my_catcher'
cat_path = 'gato2'


def message(content, conf):
    print('\t\t\n#### [{}] ### {} ####\n'.format(conf, content))


#################################################################
#                      INSERTED CODE
#################################################################
def count(highstack, needles):
    counts = 0
    needles = set(needles)
    for elem in highstack:
        if elem in needles:
            counts += 1
    return counts

def normalize(elem, orig_min, orig_max, reverse=False):
    if reverse:
        orig_min, orig_max = orig_max, orig_min
    if (orig_max-orig_min) == 0: return 1
    return (elem - orig_min)/(orig_max-orig_min)

def translate_1(value, in_from, in_to, out_from, out_to):
    out_range = out_to - out_from
    in_range = in_to - in_from
    in_val = value - in_from
    val = (float(in_val) / in_range) * out_range
    out_val = out_from + val
    return out_val


def translate(value, in_from, in_to, out_from, out_to):
    answer = translate_1(value, in_from, in_to, out_from, out_to)
    return answer if answer >= 0 else 0


goals = exits
walls = blocks







class ScoreCalculator:
    def __init__(self, mode):
        #Todo: one mode for cat neighbours only and one for all grid
        self.grid = Grid(goals, walls, cat, rows=11, cols=11)
        self.grid.assign_difficulty(3)

        self.dist = DistanceTypes.HEX

        astar_cat = AstarCat(
            max_iterations=200,
            grid=self.grid,
            gWeight=1,
            hWeight=1,
            fWeight=1,
            distanceType=self.dist
        )

        self.path_distances = {}
        self.dc = Distance2DCalculator()
        self.cat_obj = astar_cat

        self.path_dist_min_hits = {}
        self.path_distances_values = []
        self.path_distances_min_hits_values = []



    def calc(self, cat_, walls_, goals_):


        self.grid.redesign_reset_grid(goals_, walls_, cat_)

        with open('firetest.txt', 'a+') as file:
            file.write('-'*20+'\n')
            file.write('\nCAT\n')
            file.write('{}'.format(cat_))
            file.write('\nWALLS\n')
            file.write('{}'.format(walls_))
            file.write('\bGOALS\n')
            file.write('{}'.format(goals_))


        self.path_dist_min_hits = {}
        self.path_distances_values = []
        self.path_distances_min_hits_values = []

        #for i in range(11):
        #    for j in range(11):
        #        el = (j, i)
        #        for goal in [goal for goal in goals if goal not in walls]:
        #            if el != goal:
        #                #Path Distance
        #                cat_obj.reset()  # reseting the cat
        #                answer = cat_obj.find_path(start_cell=el, end_cell=goal)  # Finding the path to the goal
        #                path_len = 0
        #                if answer is not Solution.NO_SOLUTION:
        #                    path_len = cat_obj.path.get_distance()
        #                else:
        #                    path_len = 11
        #                if el not in path_distances:
        #                    path_distances[el] = [{'goal': goal, 'len': path_len}]
        #                else:
        #                    path_distances[el].append({'goal': goal, 'len': path_len})


        for i in range(11):
            for j in range(11):
                el = (j, i)

                dist = 0

                if el in walls_ and el in goals_:
                    dist = 10
                if el in walls_:
                    dist = 20
                if el in goals_:
                    dist = 30
                if el == cat_:
                    dist = 40


                if el not in self.path_distances:
                    self.path_distances[el] = [{'goal': (0,0), 'len': dist}]
                else:
                    self.path_distances[el].append({'goal': (0,0), 'len': dist})

        #Path
        for key, elem in self.path_distances.items():
            min_dist = min(elem, key=lambda cont : cont['len'])
            local_path_dist_values = []
            for subelem in elem:
                self.path_distances_values.append(subelem['len'])
                local_path_dist_values.append(subelem['len'])

            hits = count(local_path_dist_values,[min_dist['len']])
            self.path_distances_min_hits_values.append(hits)
            self.path_dist_min_hits[key] = {'len' : min_dist['len'], 'hits' : hits, 'min': min(local_path_dist_values), 'max': max(local_path_dist_values)}

    def score(self, pos):

        el = pos
        elem = self.path_dist_min_hits[el]

        #for key, elem in path_dist_min_hits.items():
        #    el = key

        difficulties = self.grid.get_difficulties()
        p1 = normalize(self.grid.get_cell(el).difficulty, min(difficulties), max(difficulties), reverse=False)

        p2 = normalize(elem['len'], min(self.path_distances_values), max(self.path_distances_values), reverse=True)
        p3 = normalize(elem['hits'], min(self.path_distances_min_hits_values), max(self.path_distances_min_hits_values),
                       reverse=False)

        return {'p1': p1, 'p2': p2, 'p3' : p3}



#########################################################################




path = []
sc = ScoreCalculator(None)

def compute_image(cat, blocks, exits) :
    beep_test.smallBeep()
    im = Image.open("tabuleiros/tabuleiro.jpg")
    draw = ImageDraw.Draw(im, 'RGBA')

    path.append(cat)
    sc.calc(cat, blocks, exits)

    #######################################################################
    #                       INSERTED CODE
    #######################################################################
    # Score
    for i in range(11):
        for j in range(11):
            el = (j, i)

            shrink = 5

            # dist = ((p3 * 2) + p2) - p1

            # p1 = difficulty
            # p2 = path distance (A*)
            # p3 = min dist hits (min_len_hits)

            score = sc.score(el)['p2']

            #if key in goals and key not in walls:
            #    score += 5

            color = 'hsl(' + str(int(translate(score, 0, 1, 50, 190))) + ', 100%, 50%)'

            shift = el[0] % 2 * 25
            init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
            end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

            init_y = (el[0] * 49) + shrink
            end_y = ((el[0] + 1) * 49) - shrink
            draw.ellipse([init_x, init_y, end_x, end_y], fill=color)
        #####################################################################

    # Goals
    for el in exits :
        shrink = 10

        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink
        draw.ellipse([init_x, init_y, end_x, end_y],fill = "rgba(0, 0, 255, 200)")

    # Blocks
    for el in blocks :
        shift = el[0] % 2 * 25
        init_x = shift + el[1]*50 + el[1]*5
        end_x  = shift + (el[1]+1)*50 + el[1]*5
        init_y = el[0]*49
        end_y  = (el[0]+1)*49
        draw.line([init_x+10, init_y+10, end_x-10, end_y-10],fill = "red", width=6)
        draw.line([init_x+10,end_y-10, end_x-10, init_y+10],fill = "red", width=6)

    # Path
    for el in path:
        shrink = 15

        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink

        draw.ellipse([init_x, init_y, end_x, end_y], fill=(5, 5, 5, 50))
    # Cat
    for el in [cat] :
        shrink = 10

        shift = el[0] % 2 * 25
        init_x = (shift + el[1]*50 + el[1]*5) + shrink
        end_x  = (shift + (el[1]+1)*50 + el[1]*5) - shrink

        init_y = (el[0]*49) + shrink
        end_y  = ((el[0]+1)*49) - shrink

        draw.ellipse([init_x, init_y, end_x, end_y],fill = "#808080")

        draw.point((init_x, init_y), fill='red')

        draw.polygon([(init_x, init_y + shrink), (init_x + 5, init_y - 10), (init_x + 15, init_y + 5)], fill="#808080")
        draw.polygon([(init_x + 30, init_y + shrink),(init_x + 25, init_y - 10),(init_x + 15, init_y + 5)], fill="#808080")

        draw.ellipse([init_x + 6, init_y + 6 , init_x + 11, init_y + 11], fill="black")
        draw.ellipse([init_x + 8 + 10, init_y + 6, init_x + 13 + 10, init_y + 11], fill="black")
        draw.polygon([(init_x + 12, init_y + 15), (init_x + 18, init_y + 15), (init_x + 15, init_y + 18)],fill="black")

    del draw
    return im


def make_move(cat, direction) :
    candidates = {}
    if cat[0] % 2 == 0 :
        candidates = {
            "NW" : (cat[0] - 1, cat[1] - 1,), 
            "NE" : (cat[0] - 1, cat[1],    ), 
            "W"  : (cat[0], cat[1] - 1,    ), 
            "E"  : (cat[0], cat[1] + 1,    ), 
            "SW" : (cat[0] + 1, cat[1] - 1,), 
            "SE" : (cat[0] + 1, cat[1],    ), 
        }
    else :
        candidates = {
            "NW" : (cat[0] - 1, cat[1],     ),
            "NE" : (cat[0] - 1, cat[1] + 1, ),
            "W"  : (cat[0], cat[1] - 1,     ),
            "E"  : (cat[0], cat[1] + 1,     ),
            "SW" : (cat[0] + 1, cat[1],     ),
            "SE" : (cat[0] + 1, cat[1]+1,   ),
        }
    return candidates[direction]


def generate_random(used) :
    candidate = (random.randint(0, 10), random.randint(0, 10))
    while candidate in used :
        candidate = (random.randint(0, 10), random.randint(0, 10))    
    return candidate

def valid_move_catcher(cat, catcher, blocks, exits) :
    try :
        catcher = tuple(eval(catcher)[:2])
    except Exception as e:
        message(e, conf_name)
        if DEBUG :
            message("Catcher makes an unintelligible move `{}`".format(str(catcher)), conf=conf_name)
        return "loss"
    if catcher == cat :
        if DEBUG :
            message("Catcher cannot step on cat", conf=conf_name)
        return "loss"
    elif catcher in blocks :
        if DEBUG :
            message("Catcher cannot block a cell twice `{}`".format(str(catcher)), conf=conf_name)
        return "loss"
    elif catcher[0] < 0 or catcher[1] < 0 or catcher[0] > 10 or catcher[1] > 10 :
        if DEBUG :
            message("Catcher cannot block outside the grid", conf=conf_name)
        return "loss"
    return catcher

def valid_move_cat(cat, direction, blocks, exits) :
    if not direction :
        if DEBUG :
            message("Cat did not move and got caught | sayed: `{}`".format(cat), conf=conf_name)
        return "loss"
    
    #direction = direction.decode('ascii')

    if not direction in ["NW", "NE", "W", "E", "SW", "SE"] :
        if DEBUG :
            message("Cat makes an unintelligible move : `{}`".format(direction), conf=conf_name)
        return "loss"

    cat = make_move(cat, direction)
    if cat in blocks :
        if DEBUG :
            message("Cat hits the block `{}` -said- `{}`".format(cat,direction), conf=conf_name)
        return "loss"
    if cat in exits :
        if DEBUG :
            message("**Cat runs away :)**", conf=conf_name)
        return "win"

    return cat
    
images = []

while True :
    if ANIMATION :
        images.append(compute_image(cat, blocks, exits))
        
    if DEBUG :
        print("###### Blocks: %s" % str(blocks))
        pass
    catcher_output = subprocess.Popen(['python', catcher_path + '.py', str(cat), str(blocks), str(exits)], stdout=subprocess.PIPE).communicate()[0].rstrip()
    catcher = valid_move_catcher(cat, catcher_output, blocks, exits)
    if catcher == "loss" :
        print("0")
        break
    elif DEBUG :
        print("CATCHER = %s" % str(catcher))
        pass
    blocks.append(catcher)
    
    if ANIMATION :
        images.append(compute_image(cat, blocks, exits))



    cat_output = subprocess.Popen(['python', cat_path + '.py', str(cat), str(blocks), str(exits)],
        stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()


    cat = valid_move_cat(cat, cat_output, blocks, exits) 
    if cat == "loss" :
        print("1")
        break
    elif cat == "win":
        print("0")
        break
    elif DEBUG :
        pass
        print("CAT     = %s" % str(cat))
    
    
if ANIMATION:
    images[0].save('games/game_{}.gif'.format(conf_name),
                   save_all=True,
                   append_images=images[1:],
                   duration=350,
                   loop=0)


