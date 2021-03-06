import random

import arcade

from abbot.galaxy.celestial_body import CelestialBody


class Chunk:
    """A chunk within the game. A chunk has coordinates, defined as a
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
        self.celestial_bodies = []
        self.create_celestial_body()
        # TODO generate more/varied celestial modies
        # TODO generate features on celestial bodies

    def __eq__(self, obj):
        return self.chunk_seed == obj.chunk_seed

    def __hash__(self):
        return self.chunk_seed

    def __str__(self):
        return f"[Chunk {self.chunk_x},{self.chunk_y} seed={self.chunk_seed}]"

    def seed_chunk(self):
        """Initial pass at seed method. This should be consistent whenever
        we see this chunk, since it will be reclaimed and die at any time.
        This must incorporate the global seed and the chunk coordinates, at
        a minimum.
        """
        random.seed(self.chunk_seed)

    def create_celestial_body(self):
        x = self.center_x + random.randint(-(2 ** 9), 2 ** 9)
        y = self.center_y + random.randint(-(2 ** 9), 2 ** 9)
        radius = random.randint(2 ** 9, 2 ** 11)
        body = CelestialBody(x, y, radius)
        self.celestial_bodies.append(body)

    @property
    def chunk_seed(self):
        return self.seed + self.chunk_y * self.chunk_width + self.chunk_x
