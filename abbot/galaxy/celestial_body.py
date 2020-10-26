import arcade

class CelestialBody(arcade.Sprite):
    def __init__(self, center_x, center_y, radius):
        """ x, y in absolute coordinates """
        super().__init__(center_x=center_x, center_y=center_y)
        self.radius = radius
