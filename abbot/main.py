import arcade

from abbot.ui.gameplay_window import GameplayWindow


def main():
    """ Main method """
    window = GameplayWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
