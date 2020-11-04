import random
from typing import Optional

import arcade
import pymunk

from abbot.math import distance
from abbot.npc import NPC, ATTACK_DISTANCE
from abbot.driver import Driver

SCREEN_TITLE = "Abbot"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024


class GameplayWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.view_left = -SCREEN_WIDTH // 2
        self.view_bottom = -SCREEN_HEIGHT // 2
        self.driver = Driver()

    def on_draw(self):
        """ Render the screen. """
        # viewport and camera
        self.view_left = int(self.driver.player.x) - SCREEN_WIDTH // 2
        self.view_bottom = int(self.driver.player.y) - SCREEN_HEIGHT // 2
        arcade.set_viewport(
            self.view_left,
            SCREEN_WIDTH + self.view_left,
            self.view_bottom,
            SCREEN_HEIGHT + self.view_bottom,
        )

        # Clear the screen to the background color
        arcade.start_render()

        if not self.driver.player.fainted():
            self.driver.player.draw()

        for chunk in self.driver.active_chunks:
            for celestial_body in chunk.celestial_bodies:
                arcade.draw_circle_filled(
                    celestial_body.center_x,
                    celestial_body.center_y,
                    celestial_body.radius,
                    arcade.color.YELLOW,
                )

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"{self.driver.player.x:.2f},{self.driver.player.y:.2f} angle: {self.driver.player.angle:.2f} hp: {self.driver.player.current_hp}"
        arcade.draw_text(
            score_text,
            self.view_left + 10,
            self.view_bottom + 10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.driver.update(delta_time)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.R:
            self.driver = Driver()
            return
        if not self.driver.player.fainted():
            if key == arcade.key.UP or key == arcade.key.SPACE:
                self.driver.jump()
            if key == arcade.key.LEFT:
                self.driver.moving_left = True
            if key == arcade.key.RIGHT:
                self.driver.moving_right = True
            if key == arcade.key.A:
                self.driver.do_attack = True
            if key == arcade.key.C:
                self.driver.player.body.angle = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT:
            self.driver.moving_left = False
        if key == arcade.key.RIGHT:
            self.driver.moving_right = False
