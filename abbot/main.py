import random
from typing import Optional

import arcade

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
PLAYER_MOVE_FORCE_ON_GROUND = 8000

PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = SCREEN_HEIGHT / 2


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

    def setup(self):
        # Set up the player, specifically placing it at these coordinates.
        self.player = NPC("kingkrool", hp=100)
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        # Physics
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.do_attack = False
        self.view_left = -PLAYER_START_X
        self.view_bottom = -PLAYER_START_Y

        self.galaxy = Galaxy()

        # Physics
        self.physics_engine = arcade.PymunkPhysicsEngine()
        self.physics_engine.add_sprite(
            self.player,
            friction=1.0,
            mass=2.0,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=1000,
            max_vertical_velocity=1000,
        )
        self.active_chunks = []
        self.active_chunks = self.update_active_chunks()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        self.terrain.draw()
        if not self.player.fainted():
            self.player.draw()

        for chunk in self.active_chunks:
            for celestial_body in chunk.celestial_bodies:
                arcade.draw_circle_filled(
                    celestial_body.x,
                    celestial_body.y,
                    celestial_body.radius,
                    arcade.color.YELLOW,
                )

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"x: {self.player.center_x} y: {self.player.center_y} hp: {self.player.current_hp}"
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
            self.physics_engine.apply_force(self.player, force)
        if self.moving_down:
            force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
            self.physics_engine.apply_force(self.player, force)
        if self.moving_left:
            force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.player, force)
        if self.moving_right:
            force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            self.physics_engine.apply_force(self.player, force)
        self.player.update()
        self.update_active_chunks()
        self.physics_engine.step()
        if self.do_attack:
            self.do_attack = False
            self.player.attack([])

        # camera update
        self.view_left = int(self.player.center_x) - SCREEN_WIDTH // 2
        self.view_bottom = int(self.player.center_y) - SCREEN_HEIGHT // 2
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
        last_active_chunks = self.active_chunks
        self.active_chunks = list(
            self.galaxy.position_to_active_chunks(
                self.player.center_x, self.player.center_y
            )
        )
        # remove chunk sprites from engine
        for last_active_chunk in last_active_chunks:
            if not Chunk.chunks_contain_chunk(self.active_chunks, last_active_chunk):
                self.physics_engine.remove_sprite_list(
                    last_active_chunk.celestial_bodies
                )
        # add chunk sprites to engine
        for active_chunk in self.active_chunks:
            if not Chunk.chunks_contain_chunk(last_active_chunks, active_chunk):
                for body in active_chunk.celestial_bodies:
                    self.physics_engine.add_sprite(
                        body,
                        friction=0.7,
                        collision_type="wall",
                        radius=body.radius,
                        body_type=arcade.PymunkPhysicsEngine.STATIC,
                    )


def main():
    """ Main method """
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
