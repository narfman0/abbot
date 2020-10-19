import unittest

import pytest

from abbot.galaxy import Chunk


def test_chunk_seed_create_is_equivalent():
    chunk_1 = Chunk(seed=0, chunk_x=0, chunk_y=1, chunk_width=2 ** 10)
    chunk_2 = Chunk(seed=0, chunk_x=0, chunk_y=1, chunk_width=2 ** 10)
    assert len(chunk_1.celestial_bodies) == len(chunk_2.celestial_bodies)
    assert chunk_1.celestial_bodies[0].x == chunk_2.celestial_bodies[0].x
    assert chunk_1.celestial_bodies[0].y == chunk_2.celestial_bodies[0].y
