import random
from functools import lru_cache

from abbot.galaxy.chunk import Chunk


class Galaxy:
    """ Identify and control the environment. Chunks are viewed like a grid,
    and themselves have coordinates. Coordinates originate at 0,0 and can
    be positive or negative. A chunk can be
    thrown away when a player distances themselves sufficiently, and
    regenerated upon demand with the seed and coordinates.

    Initially we might start with 1 chunk, but eventually we would expect
    something like 9 chunks active at any one time. They should be small enough
    to allow for on the fly generation. They might have 0-x celestial bodies.
    Celestial bodies should not bleed into other chunks. Bodies should not move
    within chunks. This allows each chunk to only care about what is within the
    chunk. This could lead to bodies being in close proximity to each other,
    but we will handle that at the physics engine level.
    """

    def __init__(self, seed=None, chunk_width=2 ** 14):
        self.seed = seed if seed else random.randint(0, 2 ** 32)
        self.chunk_width = chunk_width

    def position_to_chunk_coordinates(self, x, y):
        """ Return the chunk coordinates based on the absolute x,y coordinates """
        return (int(x // self.chunk_width), int(y // self.chunk_width))

    @lru_cache(maxsize=18)
    def chunk_from_chunk_coordinates(self, chunk_x, chunk_y):
        return Chunk(
            self.seed,
            chunk_x,
            chunk_y,
            self.chunk_center_from_chunk_coordinates(chunk_x, chunk_y),
            self.chunk_width,
        )

    def chunk_center_from_chunk_coordinates(self, chunk_x, chunk_y):
        return (self.chunk_width * chunk_x, self.chunk_width * chunk_y)
