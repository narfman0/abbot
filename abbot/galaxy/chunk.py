import random

import arcade

from abbot.galaxy.celestial_body import CelestialBody


class Chunk:
    """ A chunk within the game. A chunk has coordinates, defined as a
    chunk_x, chunk_y pair.
    
    Note: coordinates shall always be absolute coordinates. Chunk
    coordinates do not exist and we will not do math relative to chunk
    coordinates.
    """

    def __init__(self, seed, chunk_x, chunk_y, chunk_width):
        self.seed = seed
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.chunk_width = chunk_width
        self.center_x = chunk_x * chunk_width
        self.center_y = chunk_y * chunk_width

        self.seed_chunk()
        self.celestial_bodies = arcade.SpriteList()
        self.create_celestial_body()
        # TODO generate more/varied celestial modies
        # TODO generate features on celestial bodies

    def __eq__(self, obj):
        return self.seed_chunk() == obj.seed_chunk()

    def seed_chunk(self):
        """ Initial pass at seed method. This should be consistent whenever
        we see this chunk, since it will be reclaimed and die at any time.
        This must incorporate the global seed and the chunk coordinates, at
        a minimum.
        """
        random.seed(self.seed + self.chunk_y * self.chunk_width + self.chunk_x)

    def create_celestial_body(self):
        x = self.center_x + random.randint(-(2 ** 9), 2 ** 9)
        y = self.center_y + random.randint(-(2 ** 9), 2 ** 9)
        radius = random.randint(2 ** 9, 2 ** 11)
        body = CelestialBody(x, y, radius)
        self.celestial_bodies.append(body)