import random
from typing import Optional

import arcade
import pymunk

from abbot.math import distance
from abbot.npc import NPC, ATTACK_DISTANCE
from abbot.galaxy import Chunk, Galaxy

# Movement speed of player, in pixels per frame
MOVEMENT_SPEED = 2
GRAVITY = 1
PLAYER_JUMP_SPEED = 25
PLAYER_MOVE_FORCE_ON_GROUND = 1000


class Driver:
    def __init__(self):
        # Set up the player, specifically placing it at these coordinates.
        self.player = NPC("kingkrool", hp=100)

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.do_attack = False
        self.galaxy = Galaxy()

        # Physics
        self.space = pymunk.Space()
        self.space.add(self.player.body, self.player.poly)
        self.active_chunks = []
        self.active_chunks = self.update_active_chunks()

    def update(self, delta_time):
        """ Movement and game logic """
        if self.moving_up:
            force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
            self.player.body.apply_force_at_local_point(force, (0, 0))
        if self.moving_down:
            force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
            self.player.body.apply_force_at_local_point(force, (0, 0))
        if self.moving_left:
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.player.body.apply_force_at_local_point(force, (0, 0))
        if self.moving_right:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.player.body.apply_force_at_local_point(force, (0, 0))
        self.player.update()

        self.update_active_chunks()
        self.space.step(delta_time)
        if self.do_attack:
            self.do_attack = False
            self.player.attack([])

    def update_active_chunks(self):
        last_active_chunks = self.active_chunks or []
        self.active_chunks = list(
            self.galaxy.position_to_active_chunks(self.player.x, self.player.y)
        )
        # remove chunk sprites from engine
        for last_active_chunk in last_active_chunks:
            if not last_active_chunk in self.active_chunks:
                for celestial_body in last_active_chunk.celestial_bodies:
                    try:
                        self.space.remove(celestial_body.shape, celestial_body.body)
                        print(f"Removed celestial_body {celestial_body}")
                    except:
                        print(f"Error removing celestial body {celestial_body}")

                print(f"Removed chunk {last_active_chunk}")
        # add chunk sprites to engine
        for active_chunk in self.active_chunks:
            if not active_chunk in last_active_chunks:
                for celestial_body in active_chunk.celestial_bodies:
                    try:
                        self.space.add(celestial_body.body, celestial_body.shape)
                        print(f"Created celestial body {celestial_body}")
                    except:
                        print(
                            f"Error, duplicate adding celestial body {celestial_body}"
                        )

                print(f"Added chunk {active_chunk}")
