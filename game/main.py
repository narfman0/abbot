import random

import arcade

from game.math import distance
from game.npc import NPC, ATTACK_DISTANCE

SCREEN_TITLE = "Game"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

# Movement speed of player, in pixels per frame
MOVEMENT_SPEED = 2
GRAVITY = 1
PLAYER_JUMP_SPEED = 25

PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = SCREEN_HEIGHT / 2


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Separate variable that holds the player sprite
        self.terrain = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player = NPC("kingkrool", hp=100)
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        # Physics
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.terrain)

        self.do_attack = False

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen to the background color
        arcade.start_render()

        self.terrain.draw()
        if not self.player.fainted():
            self.player.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"x: {self.player.center_x} y: {self.player.center_y} hp: {self.player.current_hp}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.moving_up:
            self.player.change_y = MOVEMENT_SPEED
        elif self.moving_down:
            self.player.change_y = -MOVEMENT_SPEED
        else:
            self.player.change_y = 0
        if self.moving_left:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.moving_right:
            self.player.change_x = MOVEMENT_SPEED
        else:
            self.player.change_x = 0
        self.player.update()
        self.terrain.update()
        self.physics_engine.update()
        if self.do_attack:
            self.do_attack = False
            self.player.attack([])

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


def main():
    """ Main method """
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
