import math


def distance(sprite1, sprite2):
    return math.sqrt((sprite1.x - sprite2.x) ** 2 + (sprite1.y - sprite2.y) ** 2)
