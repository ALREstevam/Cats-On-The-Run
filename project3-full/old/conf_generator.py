import random
import math


def fill(minsize, maxsize, constant, random_on_x = False, random_range = 10) -> set:
    size = random.randint(minsize, maxsize)

    answer = set()

    while len(answer) < size:

        random_value = random.randint(0, random_range)

        if random_on_x:
            value = (random_value, constant)
        else:
            value = (constant, random_value)
        if value not in answer:
            answer.add(value)

    return answer


def confs():

    answer = []
    cat = (5, 5)

    for i in range(100):
        wall_amount = random.randint(0, 5)

        walls = [
            (
                random.randint(0, 10),
                random.randint(0, 10)
            ) for _ in range(wall_amount)
            ]

        if cat in walls:
            walls.remove(cat)

        #goals_amount = math.ceil(random.randint(25, 35)//3)

        goals = fill(25 // 3, 35 // 3, 0, True)
        goals.union(fill(25 // 3, 35 // 3, 10, True))
        goals.union(fill(25 // 3, 35 // 3, 0, False))

        answer.append(["{}".format(cat), "{}".format(walls), "{}".format(goals) ])
    return answer




