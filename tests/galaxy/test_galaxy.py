import unittest

import pytest

from abbot.galaxy import Chunk, Galaxy


@pytest.fixture
def galaxy():
    return Galaxy(seed=0)


def test_position_to_chunk_coordinates(galaxy):
    assert galaxy.position_to_chunk_coordinates(0, 0) == (0, 0)
    assert galaxy.position_to_chunk_coordinates(galaxy.chunk_width + 1, 0) == (1, 0)
    assert galaxy.position_to_chunk_coordinates(0, -galaxy.chunk_width) == (0, -1)


def test_chunk_from_chunk_coordinates(galaxy):
    for x, y in [(0, 0), (1, 0), (1, 1), (-1, -1)]:
        assert isinstance(galaxy.chunk_from_chunk_coordinates(x, y), Chunk)


def test_chunk_center_from_chunk_coordinates(galaxy):
    assert galaxy.chunk_center_from_chunk_coordinates(0, 0) == (0, 0)
    assert galaxy.chunk_center_from_chunk_coordinates(1, 0) == (galaxy.chunk_width, 0)
