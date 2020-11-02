import random
from typing import Optional

import arcade
import pymunk

from abbot.math import distance
from abbot.npc import NPC, ATTACK_DISTANCE
from abbot.galaxy import Chunk, Galaxy

SCREEN_TITLE = "Abbot"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

# Movement speed of player, in pixels per frame
MOVEMENT_SPEED = 2
GRAVITY = 1
PLAYER_JUMP_SPEED = 25
PLAYER_MOVE_FORCE_ON_GROUND = 1000


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.space = Optional[pymunk.Space]

    def setup(self):
        # Set up the player, specifically placing it at these coordinates.
        self.player = NPC("kingkrool", hp=100)

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.do_attack = False
        self.view_left = -PLAYER_START_X
        self.view_bottom = -PLAYER_START_Y

        self.galaxy = Galaxy()

        # Physics
        self.space = pymunk.Space()
        self.space.add(self.player.body, self.player.poly)
        self.active_chunks = []
        self.active_chunks = self.update_active_chunks()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        if not self.player.fainted():
            self.player.draw()

        for chunk in self.active_chunks:
            for celestial_body in chunk.celestial_bodies:
                arcade.draw_circle_filled(
                    celestial_body.center_x,
                    celestial_body.center_y,
                    celestial_body.radius,
                    arcade.color.YELLOW,
                )

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"{self.player.x:.2f},{self.player.y:.2f} angle: {self.player.angle:.2f} hp: {self.player.current_hp}"
        arcade.draw_text(
            score_text,
            self.view_left + 10,
            self.view_bottom + 10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_update(self, delta_time):
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

        # camera update
        self.view_left = int(self.player.x) - SCREEN_WIDTH // 2
        self.view_bottom = int(self.player.y) - SCREEN_HEIGHT // 2
        arcade.set_viewport(
            self.view_left,
            SCREEN_WIDTH + self.view_left,
            self.view_bottom,
            SCREEN_HEIGHT + self.view_bottom,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.R:
            self.setup()
            return
        if not self.player.fainted():
            if key == arcade.key.UP:
                self.moving_up = True
            if key == arcade.key.LEFT:
                self.moving_left = True
            if key == arcade.key.RIGHT:
                self.moving_right = True
            if key == arcade.key.DOWN:
                self.moving_down = True
            if key == arcade.key.A:
                self.do_attack = True
            if key == arcade.key.C:
                self.player.body.angle = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.moving_up = False
        if key == arcade.key.LEFT:
            self.moving_left = False
        if key == arcade.key.RIGHT:
            self.moving_right = False
        if key == arcade.key.DOWN:
            self.moving_down = False

    def update_active_chunks(self):
        last_active_chunks = self.active_chunks or []
        self.active_chunks = list(
            self.galaxy.position_to_active_chunks(
                self.player.x, self.player.y
            )
        )
        # remove chunk sprites from engine
        for last_active_chunk in last_active_chunks:
            if not last_active_chunk in self.active_chunks:
                for celestial_body in last_active_chunk.celestial_bodies:
                    self.space.remove(celestial_body.shape, celestial_body.body)
                    print(f"Removed celestial_body {celestial_body.center_x},{celestial_body.center_y}")
                print(f"Removed chunk {last_active_chunk.chunk_x},{last_active_chunk.chunk_y}")
        # add chunk sprites to engine
        for active_chunk in self.active_chunks:
            if not active_chunk in last_active_chunks:
                for celestial_body in active_chunk.celestial_bodies:
                    mass = 1
                    moment = pymunk.moment_for_circle(mass, 0, celestial_body.radius) 
                    body = pymunk.Body(mass, moment, body_type=pymunk.body.Body.STATIC)
                    body.position = celestial_body.center_x, celestial_body.center_y
                    shape = pymunk.Circle(body, celestial_body.radius)
                    self.space.add(body, shape)
                    celestial_body.body = body
                    celestial_body.shape = shape
                    print(f"Created celestial body at {celestial_body.center_x},{celestial_body.center_y} with r={celestial_body.radius}")
                print(f"Added chunk {active_chunk.chunk_x},{active_chunk.chunk_y}")


def main():
    """ Main method """
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
