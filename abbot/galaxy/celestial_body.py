import pymunk


class CelestialBody:
    def __init__(self, x, y, radius):
        """ x, y in absolute coordinates """
        self.radius = radius

        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment, body_type=pymunk.body.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.friction = 0.5

    @property
    def x(self):
        return int(self.body.position[0])

    @property
    def y(self):
        return int(self.body.position[1])

    def __eq__(self, obj):
        return self.x == obj.x and self.y == obj.y and self.radius == obj.radius

    def __hash__(self):
        return (self.x << 16) + (self.y << 8) + self.radius

    def __str__(self):
        return f"[CelestialBody {self.x},{self.y} r={self.radius}]"
