import sys
import random
import subprocess
from PIL import Image, ImageDraw

DEBUG     = False
ANIMATION = True

cat    = eval(sys.argv[1])
blocks = eval(sys.argv[2])
exits  = eval(sys.argv[3])

catcher_path = 'my_catcher'


def compute_image(cat, blocks, exits) :
    im = Image.open("tabuleiros/tabuleiro.jpg")
    draw = ImageDraw.Draw(im)

                  
    # Goals
    for el in exits :
        shift = el[0] % 2 * 25
        init_x = shift + el[1]*50 + el[1]*5
        end_x  = shift + (el[1]+1)*50 + el[1]*5
        init_y = el[0]*49
        end_y  = (el[0]+1)*49
        draw.ellipse([init_x, init_y, end_x, end_y],fill = "blue")

    # Blocks
    for el in blocks :
        shift = el[0] % 2 * 25
        init_x = shift + el[1]*50 + el[1]*5
        end_x  = shift + (el[1]+1)*50 + el[1]*5
        init_y = el[0]*49
        end_y  = (el[0]+1)*49
        draw.line([init_x+10, init_y+10, end_x-10, end_y-10],fill = "red", width=6)
        draw.line([init_x+10,end_y-10, end_x-10, init_y+10],fill = "red", width=6)

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
    except :
        if DEBUG :
            print("Catcher makes an unintelligible move `{}`".format(str(catcher)))
        return "loss"
    if catcher == cat :
        if DEBUG :
            print("Catcher cannot step on cat")
        return "loss"
    elif catcher in blocks :
        if DEBUG :
            print("Catcher cannot block a cell twice `{}`".format(str(catcher)))
        return "loss"
    elif catcher[0] < 0 or catcher[1] < 0 or catcher[0] > 10 or catcher[1] > 10 :
        if DEBUG :
            print("Catcher cannot block outside the grid")
        return "loss"

    return catcher

def valid_move_cat(cat, direction, blocks, exits) :
    if not direction :
        if DEBUG :
            print("Cat did not move and got caught")        
        return "loss"
    
    #direction = direction.decode('ascii')

    if not direction in ["NW", "NE", "W", "E", "SW", "SE"] :
        if DEBUG :
            print("Cat makes an unintelligible move")
        return "loss"

    cat = make_move(cat, direction)
    if cat in blocks :
        if DEBUG :
            print("Cat hits the block")
        return "loss"
    if cat in exits :
        if DEBUG :
            print("Cat runs away")
        return "win"

    return cat
    
images = []

while True :
    if ANIMATION :
        images.append(compute_image(cat, blocks, exits))
        
    if DEBUG :
        print("###### Blocks: %s" % str(blocks))
    
    catcher_output = subprocess.Popen(['python', catcher_path + '.py', str(cat), str(blocks), str(exits)], stdout=subprocess.PIPE).communicate()[0].rstrip()
    catcher = valid_move_catcher(cat, catcher_output, blocks, exits)
    if catcher == "loss" :
        print("0")
        break
    elif DEBUG :
        print("CATCHER = %s" % str(catcher))
    blocks.append(catcher)
    
    if ANIMATION :
        images.append(compute_image(cat, blocks, exits))


    
    cat_output = subprocess.Popen(['python', 'gato.py', str(cat), str(blocks), str(exits)],
        stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()


    cat = valid_move_cat(cat, cat_output, blocks, exits) 
    if cat == "loss" :
        print("1")
        break
    elif cat == "win":
        print("0")
        break
    elif DEBUG :
        print("CAT     = %s" % str(cat))
    
    
if ANIMATION:
    images[0].save('games/game_{}.gif'.format(0),
                   save_all=True,
                   append_images=images[1:],
                   duration=200,
                   loop=0)


