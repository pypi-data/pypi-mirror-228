import pygame
import pong.utility.colours as colours


class Text:

    def __init__(self, screen: pygame.Surface, coordinates: tuple[float, float]):
        # Set up screen
        self.screen = screen

        # Obtain screen dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Create default system font
        self.font = pygame.font.SysFont(None, 25)

        # Set previous text
        self.previous_text = None

        # Create text and private text string
        self.text = self.font.render("", True, colours.WHITE)
        self.__text = ""

        # Draw text
        self.screen.blit(self.text, (50, 50))

        # Set coordinates
        self.coordinates = coordinates
        pygame.display.update()

    def set_text(self, text: str):
        # Set previous text
        self.previous_text = self.text

        # Set text and private text string
        self.text = self.font.render(text, True, colours.WHITE)
        self.__text = text

    def get_text(self):
        return self.__text

    def update(self):
        # Obtain previous text dimensions
        width = self.previous_text.get_width()
        height = self.previous_text.get_height()

        # Clear current text
        rectangle = pygame.Rect(self.coordinates, (width, height))
        pygame.draw.rect(self.screen, colours.BLACK, rectangle)

        # Draw new text
        self.screen.blit(self.text, self.coordinates)
