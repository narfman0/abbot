import arcade
import pymunk


class CelestialBody(arcade.Sprite):
    def __init__(self, center_x, center_y, radius):
        """ x, y in absolute coordinates """
        super().__init__(center_x=center_x, center_y=center_y)
        self.radius = radius

        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment, body_type=pymunk.body.Body.STATIC)
        self.body.position = center_x, center_y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.friction = 0.5

    @property
    def x(self):
        return self.center_x

    @property
    def y(self):
        return self.center_y

    def __eq__(self, obj):
        return (
            self.center_x == obj.center_x
            and self.center_y == obj.center_y
            and self.radius == obj.radius
        )

    def __hash__(self):
        return (self.center_x << 16) + (self.center_y << 8) + self.radius

    def __str__(self):
        return f"[CelestialBody {self.center_x},{self.center_y} r={self.radius}]"
