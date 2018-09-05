import importlib
import sys

filename = sys.argv[1]
mod = importlib.import_module(filename)

#print(mod.cat)

print(mod.exits)
print(mod.exits[0])
print(tuple(mod.cat))

chosen_exit = mod.exits[0]


def move(cat, direction, blocked) :
    canditates = []
    
    if cat[0] % 2 == 0 :
        candidates = [
            (cat[0] - 1, cat[1] - 1, "NW"),
            (cat[0] - 1, cat[1],     "NE"),
            (cat[0], cat[1] - 1,     "W"),
            (cat[0], cat[1] + 1,     "E"),
            (cat[0] + 1, cat[1] - 1, "SW"),
            (cat[0] + 1, cat[1],     "SE")
        ]
    else :
        candidates = [
            (cat[0] - 1, cat[1],     "NW"),
            (cat[0] - 1, cat[1] + 1, "NE"),
            (cat[0], cat[1] - 1,     "W"),
            (cat[0], cat[1] + 1,     "E"),
            (cat[0] + 1, cat[1],     "SW"),
            (cat[0] + 1, cat[1]+1,   "SE")
        ]
        
    for el in candidates :
        cand = (el[0], el[1])
        if direction == el[2]:
            return cand        
    return None
	

while tuple(mod.cat) != chosen_exit:

	walk_direction = ''

	#North
	if chosen_exit[0] < mod.cat[0]:
		walk_direction+='N'

	#South
	elif chosen_exit[0] > mod.cat[0]:
		walk_direction+='S'

	#East
	if chosen_exit[1] > mod.cat[1]:
		walk_direction+='E'

	#West
	elif chosen_exit[1] < mod.cat[1]:
		walk_direction+='W'


	print(walk_direction)
	mod.cat = move(mod.cat, walk_direction, [])






