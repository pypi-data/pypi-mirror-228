import pygame
import pong.utility.colours as colours


class Controller:

    def __init__(self, screen: pygame.Surface, rectangle: pygame.Rect):
        # Set up screen
        self.screen = screen

        # Obtain screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Set up rectangle
        self.rectangle = rectangle

        # Draw rectangle
        pygame.draw.rect(self.screen, colours.WHITE, self.rectangle)

        # Set initial velocity
        self.velocity = pygame.Vector2(0, 0)

    def get_x(self):
        return self.rectangle.x

    def get_y(self):
        return self.rectangle.y

    def get_width(self):
        return self.rectangle.width

    def get_height(self):
        return self.rectangle.height

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity: pygame.Vector2):
        self.velocity = velocity

    def update(self):
        # Clear current controller
        pygame.draw.rect(self.screen, colours.BLACK, self.rectangle)

        # Update position for frame
        self.rectangle.x -= self.velocity.x
        self.rectangle.y -= self.velocity.y

        # Draw new controller
        pygame.draw.rect(self.screen, colours.WHITE, self.rectangle)
