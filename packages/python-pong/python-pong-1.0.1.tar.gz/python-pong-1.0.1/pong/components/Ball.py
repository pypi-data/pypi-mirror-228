import pygame
import pong.utility.colours as colours


class Ball:

    def __init__(self, screen: pygame.Surface, radius: float):
        # Set up screen
        self.screen = screen

        # Obtain screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Obtain radius
        self.radius = radius

        # Calculate centre of screen
        start_x = self.width / 2
        start_y = self.height / 2

        # Draw circle
        pygame.draw.circle(self.screen, colours.WHITE, (start_x, start_y), self.radius)

        # Set initial position
        self.x = start_x
        self.y = start_y

        # Set initial velocity
        self.velocity = pygame.Vector2(0, 0)

    def get_x(self):
        return self.x

    def set_x(self, x: int):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y: int):
        self.y = y

    def get_radius(self):
        return self.radius

    def set_velocity(self, velocity: pygame.Vector2):
        # Set new velocity
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def update(self):
        # Clear current ball
        pygame.draw.circle(self.screen, colours.BLACK, (self.x, self.y), self.radius)

        # Update position for frame
        self.x += self.velocity.x
        self.y += self.velocity.y

        # Draw new ball
        pygame.draw.circle(self.screen, colours.WHITE, (self.x, self.y), self.radius)
