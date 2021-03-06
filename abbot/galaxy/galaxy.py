import random
from functools import lru_cache

from abbot.galaxy.chunk import Chunk
from abbot.math import distance


class Galaxy:
    """Identify and control the environment. Chunks are viewed like a grid,
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
        return int(x // self.chunk_width), int(y // self.chunk_width)

    def closest_celestial_body(self, x, y):
        """ Return the chunk coordinates based on the absolute x,y coordinates """
        closest = None
        closest_distance = -1
        for chunk in self.position_to_active_chunks(x, y):
            for celestial_body in chunk.celestial_bodies:
                celestial_body_distance = (
                    distance(celestial_body.x, celestial_body.y, x, y)
                    - celestial_body.radius
                )
                if closest is None or celestial_body_distance < closest_distance:
                    closest_distance = celestial_body_distance
                    closest = celestial_body
        return closest

    @lru_cache(maxsize=9)
    def chunk_from_chunk_coordinates(self, chunk_x, chunk_y):
        return Chunk(self.seed, chunk_x, chunk_y, self.chunk_width)

    def chunk_center_from_chunk_coordinates(self, chunk_x, chunk_y):
        return self.chunk_width * chunk_x, self.chunk_width * chunk_y

    def position_to_active_chunk_coordinates(self, x, y):
        chunk_coordinate_x, chunk_coordinate_y = self.position_to_chunk_coordinates(
            x, y
        )
        for chunk_offset_x in [-1, 0, 1]:
            for chunk_offset_y in [-1, 0, 1]:
                yield chunk_coordinate_x + chunk_offset_x, chunk_coordinate_y + chunk_offset_y

    def position_to_active_chunks(self, x, y):
        for chunk_x, chunk_y in self.position_to_active_chunk_coordinates(x, y):
            yield self.chunk_from_chunk_coordinates(chunk_x, chunk_y)
