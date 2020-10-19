import random
from functools import lru_cache


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


class Chunk:
    """ A chunk within the game. A chunk has coordinates, defined as a
    chunk_x, chunk_y pair.
    
    Note: coordinates shall always be absolute coordinates. Chunk
    coordinates do not exist and we will not do math relative to chunk
    coordinates.
    """

    def __init__(self, seed, chunk_x, chunk_y, chunk_center, chunk_width):
        self.seed = seed
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.chunk_center = chunk_center
        self.chunk_width = chunk_width

        self.seed_chunk()
        self.celestial_bodies = []
        self.create_celestial_body()
        # TODO generate more/varied celestial modies
        # TODO generate features on celestial bodies

    def seed_chunk(self):
        """ Initial pass at seed method. This should be consistent whenever
        we see this chunk, since it will be reclaimed and die at any time.
        This must incorporate the global seed and the chunk coordinates, at
        a minimum.
        """
        random.seed(self.seed + self.chunk_y * self.chunk_width + self.chunk_x)

    def create_celestial_body(self):
        x = self.chunk_center[0] + random.randint(-(2 ** 9), 2 ** 9)
        y = self.chunk_center[1] + random.randint(-(2 ** 9), 2 ** 9)
        radius = random.randint(2 ** 9, 2 ** 11)
        body = CelestialBody(x, y, radius)
        self.celestial_bodies.append(body)


class CelestialBody:
    def __init__(self, x, y, radius):
        """ x, y in absolute coordinates """
        self.x = x
        self.y = y
        self.radius = radius
