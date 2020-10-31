import random

import arcade
import pymunk

from abbot.animated_sprite import AnimatedSprite
from abbot.math import distance

ATTACK_DISTANCE = 100


class NPC(AnimatedSprite):
    def __init__(self, sprite_name, hp=1, attack_stat=1, defense_stat=0, scale=1, x=0, y=0):
        super().__init__(sprite_name, scale)
        self.hp = hp
        self.current_hp = hp
        self.defense_stat = defense_stat
        self.attack_stat = attack_stat
        self.non_looped_frames_remaining = 0
        self.body = pymunk.Body(1,1666)
        self.body.position = x, y
        self.poly = pymunk.Poly.create_box(self.body)

    def attack(self, npcs):
        if self.fainted() or self.current_animation_name == "attack":
            return
        self.set_animation("attack", False)
        self.non_looped_frames_remaining = self.get_current_animation_total_frames()
        for npc in npcs:
            if distance(npc, self) < ATTACK_DISTANCE:
                npc.current_hp = max(
                    0, npc.current_hp - (self.attack_stat - npc.defense_stat)
                )
                if npc.has_animation("hurt") and npc.current_animation_name == "idle":
                    npc.set_animation("hurt")  # TODO: loop=False

    def fainted(self):
        return self.current_hp <= 0

    def update(self):
        super().update()
        if not self.loop:
            self.non_looped_frames_remaining -= 1
            if self.non_looped_frames_remaining <= 0:
                self.non_looped_frames_remaining = 0
                self.set_animation("idle")
        if (
            self.has_animation("walk")
            and (self.change_x != 0 or self.change_y != 0)
            and self.current_animation_name == "idle"
        ):
            self.set_animation("walk")
        elif (
            self.change_x == 0
            and self.change_y == 0
            and self.current_animation_name == "walk"
        ):
            self.set_animation("idle")
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y
        self.angle = self.body.angle
