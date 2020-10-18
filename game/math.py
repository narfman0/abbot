import math


def distance(sprite1, sprite2):
    return math.sqrt(
        (sprite1.center_x - sprite2.center_x) ** 2
        + (sprite1.center_y - sprite2.center_y) ** 2
    )
