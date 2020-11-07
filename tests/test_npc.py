import unittest

import pytest

from abbot.npc import NPC


def test_npc_attack():
    attacker = NPC("kingkrool")
    defender = NPC("kingkrool")
    attacker.attack([defender])
    assert defender.current_hp < defender.hp


def test_npc_fainted():
    npc = NPC("kingkrool")
    npc.current_hp -= npc.current_hp
    assert npc.fainted()


def test_npc_updated():
    npc = NPC("kingkrool")
    npc.update(None)
