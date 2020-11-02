import random

import arcade
import pymunk

from abbot.ui.animated_sprite import AnimatedSprite
from abbot.math import distance

ATTACK_DISTANCE = 100


class NPC():
    def __init__(self, sprite_name, hp=1, attack_stat=1, defense_stat=0, scale=1, x=0, y=0):
        self.hp = hp
        self.current_hp = hp
        self.defense_stat = defense_stat
        self.attack_stat = attack_stat
        self._sprite = AnimatedSprite(sprite_name, scale)
        self._sprite.center_x = x
        self._sprite.center_y = y
        self.non_looped_frames_remaining = 0
        self.body = pymunk.Body(1,1666)
        self.body.position = x, y
        self.poly = pymunk.Poly.create_box(self.body, radius=self._sprite.texture.width/2)

    def attack(self, npcs):
        if self.fainted() or self._sprite.current_animation_name == "attack":
            return
        self._sprite.set_animation("attack", False)
        self.non_looped_frames_remaining = self._sprite.get_current_animation_total_frames()
        for npc in npcs:
            if distance(npc, self) < ATTACK_DISTANCE:
                npc.current_hp = max(
                    0, npc.current_hp - (self.attack_stat - npc.defense_stat)
                )
                if npc.has_animation("hurt") and npc.current_animation_name == "idle":
                    npc.set_animation("hurt")  # TODO: loop=False

    def draw(self):
        self._sprite.draw()

    def fainted(self):
        return self.current_hp <= 0

    def update(self):
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
            self.set_animation("walk")
        elif (
            self._sprite.change_x == 0
            and self._sprite.change_y == 0
            and self._sprite.current_animation_name == "walk"
        ):
            self._sprite.set_animation("idle")
        self._sprite.center_x = self.body.position.x
        self._sprite.center_y = self.body.position.y
        self._sprite.angle = self.body.angle

    @property
    def x(self):
        return self.body.position.x

    @property
    def y(self):
        return self.body.position.y

    @property
    def angle(self):
        return self.body.angle