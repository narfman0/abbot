import random
from functools import lru_cache


class World():
    """ Identify and control the world. A world can have n chunks. The chunks
    are viewed like a grid, and themselves have coordinates. A chunk can be
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
    def __init__(self, seed=None, chunk_total=1, chunk_width=2**14):
        self.seed = seed if seed else random.randint(0, 2**32)
        self.chunk_total = chunk_total
        self.chunk_width = chunk_width

        def position_to_chunk_coordinates(x, y):
            """ Return the chunk coordinates based on the world x,y coordinates """
            return (int(x//self.chunk_width), int(y//self.chunk_width))

        @lru_cache(maxsize=18)
        def chunk_from_chunk_coordinates(chunk_coordinates):
            return Chunk(self.seed, chunk_coordinates, self.chunk_center_from_chunk_coordinates(chunk_coordinates), self.chunk_width)

        def chunk_center_from_chunk_coordinates(chunk_coordinates):
            return (chunk_width * chunk_coordinates[0], chunk_width * chunk_coordinates[1])

class Chunk():
    """ A chunk within the world. Note that coordinates shall always be
    absolute/world coordinates; chunk coordinates do not exist and we will
    not do math relative to chunk coordinates.
    """
    def __init__(self, seed, chunk_coordinates, chunk_center, chunk_width):
        self.seed = seed
        self.chunk_coordinates = chunk_coordinates
        self.chunk_center = chunk_center
        self.chunk_width = chunk_width

        self.celestial_bodies = []
        create_celestial_body()
        # TODO generate more/varied celestial modies
        # TODO generate features on celestial bodies

        def create_celestial_body():
            x = self.chunk_center[0] + random.randint(-2**9, 2**9)
            y = self.chunk_center[1] + random.randint(-2**9, 2**9)
            radius = random.randint(2**9, 2**11)
            body = CelestialBody(x, y, radius)
            self.celestial_bodies.append(body)


class CelestialBody():
    def __init__(self, x, y, radius):
        """ x, y in absolute world coordinates """
        self.x = x
        self.y = y
        self.radius = radius