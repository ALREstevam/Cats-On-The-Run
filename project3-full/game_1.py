import sys
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont

#############################################################################
import beep_test
import scores_calculator_cat
import scores_calculator_catcher
#############################################################################



DEBUG     = True
ANIMATION = True
SHOW_MODE = 'CATCHER'


cat    = eval(sys.argv[1])
blocks = eval(sys.argv[2])
exits  = eval(sys.argv[3])
conf_name  = str(sys.argv[4])

catcher_path = 'my_catcher_4'
cat_path = 'gato3'


def message(content, conf):
    print('\t\t\n#### [{}] ### {} ####\n'.format(conf, content))

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


#########################################################################





#########################################################################


path = []



def compute_image(cat, blocks, exits) :


    #

    if SHOW_MODE == 'CATCHER':
        sc = scores_calculator_catcher.ScoreCalculator(goals=exits, walls=blocks, cat=cat)
    else:
        sc = scores_calculator_cat.ScoreCalculator(goals=exits, walls=blocks, diff_spred_steps=2)


    scores = sc.scores()

    beep_test.smallBeep()
    im = Image.open("tabuleiros/tabuleiro.jpg")
    draw = ImageDraw.Draw(im, 'RGBA')

    path.append(cat)


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

            #if key in goals and key not in walls:
            #    score += 5

            cell = sc.grid.get_cell(el)

            color = 'hsl(' + str(int(translate(cell.score, sc.score_range[0], sc.score_range[1], 0, 360))) + ', 100%, 50%)'

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
        draw.line([init_x + 10, init_y + 10, end_x - 10, end_y - 10], fill="red", width=7)
        draw.line([init_x + 10, end_y - 10, end_x - 10, init_y + 10], fill="red", width=7)
        draw.line([init_x+10, init_y+10, end_x-10, end_y-10],fill = "black", width=6)
        draw.line([init_x+10,end_y-10, end_x-10, init_y+10],fill = "black", width=6)

    # Path
    for el in path:
        shrink = 15

        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink

        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink

        draw.ellipse([init_x, init_y, end_x, end_y], fill=(5, 5, 5, 50))

    #Score

    for i in range(11):
        for j in range(11):
            el = (j, i)

            shrink = 5

            # dist = ((p3 * 2) + p2) - p1

            # p1 = difficulty
            # p2 = path distance (A*)
            # p3 = min dist hits (min_len_hits)


            #if key in goals and key not in walls:
            #    score += 5

            #color = 'hsl(' + str(int(translate(score, 0, 1, 360, 0))) + ', 100%, 50%)'


            color = '#3c3c3c'
            #if score <= best_score + 0.01 and score >= best_score -0.01:
            #    color = 'red'

            shift = el[0] % 2 * 25
            init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
            init_y = (el[0] * 49) + shrink
            draw.text((init_x+4,init_y+5), '{:1.2f}'.format(sc.grid.get_cell(pos=el).score), 'black', font = ImageFont.truetype("./MAKISUPA.TTF", 12, layout_engine=1), )

            #draw.text((init_x + 4, init_y + 20), '{}'.format(el), color,font=ImageFont.truetype("./MAKISUPA.TTF", 12, layout_engine=2), )

            # Cat
    for el in [cat]:
        shrink = 10
        shift = el[0] % 2 * 25
        init_x = (shift + el[1] * 50 + el[1] * 5) + shrink
        end_x = (shift + (el[1] + 1) * 50 + el[1] * 5) - shrink
        init_y = (el[0] * 49) + shrink
        end_y = ((el[0] + 1) * 49) - shrink
        draw.ellipse([init_x, init_y, end_x, end_y], fill="#808080")
        draw.point((init_x, init_y), fill='red')
        draw.polygon([(init_x, init_y + shrink), (init_x + 5, init_y - 10), (init_x + 15, init_y + 5)],
                     fill="#808080")
        draw.polygon([(init_x + 30, init_y + shrink), (init_x + 25, init_y - 10), (init_x + 15, init_y + 5)],
                     fill="#808080")
        draw.ellipse([init_x + 6, init_y + 6, init_x + 11, init_y + 11], fill="black")
        draw.ellipse([init_x + 8 + 10, init_y + 6, init_x + 13 + 10, init_y + 11], fill="black")
        draw.polygon([(init_x + 12, init_y + 15), (init_x + 18, init_y + 15), (init_x + 15, init_y + 18)],
                     fill="black")

    del draw

    beep_test.smallBeep2()
    im.save('games/proto.png')

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


