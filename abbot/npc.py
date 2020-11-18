import math
import random
import time
from dataclasses import dataclass

import arcade
import pymunk

from abbot import settings
from abbot.ui.animated_sprite import AnimatedSprite
from abbot.math import distance

ATTACK_DISTANCE = 100
PLAYER_JUMP_IMPULSE = 1000
PLAYER_GRAVITY_IMPULSE = 20


class NPC:
    def __init__(
        self, sprite_name, hp=1, attack_stat=1, defense_stat=0, scale=1, x=0, y=0
    ):
        self.hp = hp
        self.current_hp = hp
        self.defense_stat = defense_stat
        self.attack_stat = attack_stat
        self._sprite = AnimatedSprite(sprite_name, scale)
        self._sprite.center_x = x
        self._sprite.center_y = y
        self.non_looped_frames_remaining = 0
        self.body = pymunk.Body(1, 1666)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius=self._sprite.texture.width / 2)
        self.shape.elasticity = 0
        self.shape.friction = 0.5
        self.shape.npc = self
        self._collisions = []
        self._time_last_collision = 0
        self._time_last_jump = 0

    def attack(self, npcs):
        if self.fainted() or self._sprite.current_animation_name == "attack":
            return
        self._sprite.set_animation("attack", False)
        self.non_looped_frames_remaining = (
            self._sprite.get_current_animation_total_frames()
        )
        for npc in npcs:
            if distance(npc.x, npc.y, self.x, self.y) < ATTACK_DISTANCE:
                npc.current_hp = max(
                    0, npc.current_hp - (self.attack_stat - npc.defense_stat)
                )
                if (
                    npc._sprite.has_animation("hurt")
                    and npc._sprite.current_animation_name == "idle"
                ):
                    npc._sprite.set_animation("hurt")  # TODO: loop=False

    def draw(self):
        self._sprite.center_x = self.body.position.x
        self._sprite.center_y = self.body.position.y
        self._sprite.angle = math.degrees(self.body.angle)
        self._sprite.draw()

    def fainted(self):
        return self.current_hp <= 0

    def update(self, closest_celestial_body):
        # animation related
        self._sprite.update()
        if not self._sprite.loop:
            self.non_looped_frames_remaining -= 1
            if self.non_looped_frames_remaining <= 0:
                self.non_looped_frames_remaining = 0
                self._sprite.set_animation("idle")
        if (
            self._sprite.has_animation("walk")
            and (self._sprite.change_x != 0 or self._sprite.change_y != 0)
            and self._sprite.current_animation_name == "idle"
        ):
            self._sprite.set_animation("walk")
        elif (
            self._sprite.change_x == 0
            and self._sprite.change_y == 0
            and self._sprite.current_animation_name == "walk"
        ):
            self._sprite.set_animation("idle")

        # physics
        self.body.angular_velocity = 0
        if closest_celestial_body:
            polar_angle = math.atan2(
                self.y - closest_celestial_body.y, self.x - closest_celestial_body.x
            )
            polar_x = math.cos(polar_angle)
            polar_y = math.sin(polar_angle)

            ## npc angle
            target_angle = polar_angle - math.pi / 2
            self.body.angle = target_angle  # TODO smoothed_angle
            # print(f"smoothed_angle={smoothed_angle}")

            ## gravity
            self.body.apply_impulse_at_local_point((0, -PLAYER_GRAVITY_IMPULSE))

    def jump(self):
        if settings.USE_SIMPLE_JUMP_PHYSICS:
            if self._collisions or time.time() - self._time_last_collision < 0.1:
                self.body.apply_impulse_at_local_point((0, PLAYER_JUMP_IMPULSE))
                self._time_last_jump = time.time()
        else:
            # more complex and right sounding, but has been less "correct"
            for collision in self._collisions:
                if (
                    collision.shape.body is not None
                    and abs(collision.normal.x / collision.normal.y)
                    < self.shape.friction
                ):
                    self.body.apply_impulse_at_local_point((0, PLAYER_JUMP_IMPULSE))
                    return

    def add_collision(self, collision):
        self._collisions.append(collision)
        self.last_collision = time.time()

    def remove_collision(self, shape):
        to_remove = []
        for collision in self._collisions:
            if collision.shape == shape:
                to_remove.append(collision)
        for collision in to_remove:
            self._collisions.remove(collision)

    @property
    def x(self):
        return self.body.position.x

    @property
    def y(self):
        return self.body.position.y

    @property
    def angle(self):
        return self.body.angle


@dataclass
class Collision:
    """Class for keeping track of an item in inventory."""

    contact_point_set: []
    normal: pymunk.Vec2d
    shape: pymunk.Shape
    surface_velocity: pymunk.Vec2d
    total_impulse: float
