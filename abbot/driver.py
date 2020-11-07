import random
from typing import Optional

import arcade
import pymunk

from abbot.math import distance
from abbot.npc import Collision, NPC, ATTACK_DISTANCE
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

        self.do_attack = False
        self.galaxy = Galaxy()

        # Physics
        def handle_collision_begin(arbiter, space, data):
            if hasattr(arbiter.shapes[0], "npc"):
                self.handle_npc_collision_begin(
                    arbiter, space, data, arbiter.shapes[0].npc, arbiter.shapes[1]
                )
            if hasattr(arbiter.shapes[1], "npc"):
                self.handle_npc_collision_begin(
                    arbiter, space, data, arbiter.shapes[1].npc, arbiter.shapes[0]
                )
            return True

        def handle_collision_separate(arbiter, space, data):
            if hasattr(arbiter.shapes[0], "npc"):
                self.handle_npc_collision_separate(
                    arbiter, space, data, arbiter.shapes[0].npc, arbiter.shapes[1]
                )
            if hasattr(arbiter.shapes[1], "npc"):
                self.handle_npc_collision_separate(
                    arbiter, space, data, arbiter.shapes[1].npc, arbiter.shapes[0]
                )

        self.space = pymunk.Space()
        self.space.add(self.player.body, self.player.shape)
        self.collision_handler = self.space.add_default_collision_handler()
        self.collision_handler.begin = handle_collision_begin
        self.collision_handler.separate = handle_collision_separate
        self.active_chunks = []
        self.update_active_chunks()

    def update(self, delta_time):
        """ Movement and game logic """
        if self.moving_left:
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.player.body.apply_force_at_local_point(force, (0, 0))
        if self.moving_right:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.player.body.apply_force_at_local_point(force, (0, 0))
        closest_celestial_body = self.galaxy.closest_celestial_body(
            self.player.x, self.player.y
        )
        self.player.update(closest_celestial_body)

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

    def handle_npc_collision_begin(self, arbiter, space, data, npc, shape):
        print(f"NPC collision with shape")
        npc.add_collision(
            Collision(
                normal=arbiter.normal,
                total_impulse=arbiter.total_impulse,
                shape=shape,
                contact_point_set=arbiter.contact_point_set,
                surface_velocity=arbiter.surface_velocity,
            )
        )

    def handle_npc_collision_separate(self, arbiter, space, data, npc, shape):
        print(f"NPC separation with shape")
        npc.remove_collision(shape)
