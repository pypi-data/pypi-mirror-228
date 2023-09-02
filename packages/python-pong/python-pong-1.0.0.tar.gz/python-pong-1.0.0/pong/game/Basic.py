import math
import random
import tkinter
import pygame
import time

from pong.components.Controller import Controller
from pong.components.Ball import Ball
from pong.components.Text import Text


class Basic:

    def __init__(
        self,
        controller_width=1/20,
        controller_height=2/3,
        player_velocity=None,
        ball_velocity=None,
        frame_rate=60,
        tick_rate=40
    ):
        # Initialise pygame
        pygame.init()

        # Initialises font
        pygame.font.init()

        # Get monitor resolution
        width, height = self.__get_monitor_resolution()

        # Scale monitor resolution
        width = width - (width / 5)
        height = height - (height / 5)

        # Set up pygame screen
        self.screen = pygame.display.set_mode((width, height))

        # Set up rectangle dimensions
        rectangle_width = width * controller_width
        rectangle_height = height * controller_height

        # Set up first rectangle position
        rectangle_left = width * (1 / 10)
        rectangle_top = height * (1 / 6)

        # Set up first rectangle
        rectangle = pygame.Rect(rectangle_left, rectangle_top, rectangle_width, rectangle_height)

        # Set up player one controller
        self.controller_one = Controller(self.screen, rectangle)

        # Set up second rectangle position
        rectangle_left = width * (17 / 20)
        rectangle_top = height * (1 / 6)

        # Set up second rectangle
        rectangle = pygame.Rect(rectangle_left, rectangle_top, rectangle_width, rectangle_height)

        # Set up player two controller
        self.controller_two = Controller(self.screen, rectangle)

        # Calculate player velocity
        player_velocity = pygame.Vector2(0, height / 50) if (player_velocity is None) else player_velocity

        # Set player velocities
        self.player_velocity = player_velocity
        self.negative_player_velocity = pygame.Vector2(-player_velocity.x, -player_velocity.y)

        # Calculate ball radius
        radius = (width + height) / 80

        # Set up ball
        self.ball = Ball(self.screen, radius)

        # Calculate and set ball velocity
        self.ball_velocity = pygame.Vector2(width / 50, 0) if (ball_velocity is None) else ball_velocity

        # Set ball reset
        self.ball_reset_one = False
        self.ball_reset_two = True

        # Set no velocity
        self.no_velocity = pygame.Vector2(0, 0)

        # Create fps text
        self.fps_text = Text(self.screen, (0, 0))

        # Calculate player text position
        player_text_x = width / 2 - 31.5
        player_text_y = 0

        # Create player text
        self.player_text = Text(self.screen, (player_text_x, player_text_y))

        # Create player scores
        self.player_one_score = 0
        self.player_two_score = 0

        # Set clock
        self.clock = pygame.time.Clock()

        # Set frame rate
        self.frame_rate = frame_rate

        # Set tick rate
        self.tick_rate = tick_rate

        # Start game loop
        self.__game_loop()

    def __game_loop(self):
        # Set up current epoch time
        current_epoch_time = time.time()

        # Set up tick interval
        tick_interval = 1 / self.tick_rate

        # Set up main game loop
        running = True

        # Start main game loop
        while running:

            # Tick the clock
            self.clock.tick(self.frame_rate)

            # Iterate through events
            for event in pygame.event.get():

                # Handle quit event
                if event.type == pygame.QUIT:
                    running = False

            # Handle frame
            if time.time() - current_epoch_time >= tick_interval:

                # Call frame handler
                self.__handle_tick()

                # Update current epoch time
                current_epoch_time = time.time()

            # Update display
            pygame.display.update()

    def __handle_tick(self):
        # Handle controllers
        self.__handle_controllers()

        # Handle collisions
        self.__handle_collisions()

        # Handle bounds
        self.__handle_bounds()

        # Handle ball
        self.__handle_ball()

        # Create fps string
        fps_string = "fps: " + str(int(self.clock.get_fps()))

        # Set fps text
        self.fps_text.set_text(fps_string)

        # Update fps text
        self.fps_text.update()

        # Create player string
        player_string = str(self.player_one_score) + "    |    " + str(self.player_two_score)

        # Set player text
        self.player_text.set_text(player_string)

        # Update player text
        self.player_text.update()

    def __handle_controllers(self):
        # Obtain keys and modifiers
        keys = pygame.key.get_pressed()

        # Obtain controller vertical positions
        controller_one_y = self.controller_one.get_y()
        controller_two_y = self.controller_two.get_y()

        # Check for top overflows
        overflow_one_top = controller_one_y <= 0
        overflow_two_top = controller_two_y <= 0

        # Check for bottom overflows
        overflow_one_bottom = controller_one_y + self.controller_one.rectangle.height >= self.screen.get_height()
        overflow_two_bottom = controller_two_y + self.controller_two.rectangle.height >= self.screen.get_height()

        # Manage player one movement
        if keys[pygame.K_w] and not overflow_one_top:
            self.controller_one.set_velocity(self.player_velocity)

        elif keys[pygame.K_s] and not overflow_one_bottom:
            self.controller_one.set_velocity(self.negative_player_velocity)

        else:
            self.controller_one.set_velocity(self.no_velocity)

        # Manage player two movement
        if keys[pygame.K_UP] and not overflow_two_top:
            self.controller_two.set_velocity(self.player_velocity)

        elif keys[pygame.K_DOWN] and not overflow_two_bottom:
            self.controller_two.set_velocity(self.negative_player_velocity)

        else:
            self.controller_two.set_velocity(self.no_velocity)

        # Update controllers
        self.controller_one.update()
        self.controller_two.update()

    def __handle_collisions(self):
        # Obtain controller vertical positions
        controller_one_y = self.controller_one.get_y()
        controller_two_y = self.controller_two.get_y()

        # Obtain controller horizontal positions
        controller_one_x = self.controller_one.get_x()
        controller_two_x = self.controller_two.get_x()

        # Obtain controller widths
        controller_one_width = self.controller_one.get_width()
        controller_two_width = self.controller_two.get_width()

        # Obtain controller heights
        controller_one_height = self.controller_one.get_height()
        controller_two_height = self.controller_two.get_height()

        # Obtain ball positions
        ball_x = self.ball.get_x()
        ball_y = self.ball.get_y()
        radius = self.ball.get_radius()

        # Detect horizontal collisions
        horizontal_collision_one = controller_one_x <= ball_x - radius < controller_one_x + controller_one_width
        horizontal_collision_two = controller_two_x <= ball_x + radius < controller_two_x + controller_two_width

        # Detect vertical collisions
        vertical_collision_one = controller_one_y <= ball_y < controller_one_y + controller_one_height
        vertical_collision_two = controller_two_y <= ball_y < controller_two_y + controller_two_height

        # Generate random ball angle
        ball_angle = random.randint(80, 90)

        # Calculate ball velocity magnitude
        ball_velocity_magnitude = self.ball_velocity.magnitude()

        # Calculate velocities
        ball_horizontal = ball_velocity_magnitude * math.sin(math.radians(ball_angle))
        ball_vertical = ball_velocity_magnitude * math.cos(math.radians(ball_angle))

        # Generate random vertical direction
        direction = random.randint(0, 1)

        # Negate ball angle if direction is False
        ball_vertical = -ball_vertical if direction else ball_vertical

        # Detect player one collision
        if horizontal_collision_one and vertical_collision_one:
            self.ball.set_velocity(pygame.Vector2(ball_horizontal, ball_vertical))

        # Detect player two collision
        elif horizontal_collision_two and vertical_collision_two:
            self.ball.set_velocity(pygame.Vector2(-ball_horizontal, ball_vertical))

    def __handle_bounds(self):
        # Obtain screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Obtain ball positions
        ball_x = self.ball.get_x()
        ball_y = self.ball.get_y()
        radius = self.ball.get_radius()

        # Detect horizontal overflows
        left_overflow = ball_x + radius <= 0
        right_overflow = ball_x - radius >= screen_width

        # Detect vertical overflows
        top_overflow = ball_y + radius <= 0
        bottom_overflow = ball_y - radius >= screen_height

        # Detect left overflow
        if left_overflow:

            # Increment player two score
            self.player_two_score += 1

            # Set ball reset one
            self.ball_reset_one = True

        # Detect right overflow
        elif right_overflow:

            # Increment player two score
            self.player_one_score += 1

            # Set ball reset one
            self.ball_reset_one = True

        # Detect ball overflowing vertically
        elif top_overflow or bottom_overflow:
            self.ball_reset_one = True

    def __handle_ball(self):
        # Obtain keys and modifiers
        keys = pygame.key.get_pressed()

        # Manage ball movement
        if self.ball_reset_one:

            # Centre ball
            self.ball.set_x(self.screen.get_width() / 2)
            self.ball.set_y(self.screen.get_height() / 2)

            # Stop ball moving
            self.ball.set_velocity(self.no_velocity)

            # Stop ball reset one
            self.ball_reset_one = False

            # Allow ball reset two
            self.ball_reset_two = True

        elif keys[pygame.K_SPACE] and self.ball_reset_two:

            # Set ball velocity
            self.ball.set_velocity(self.ball_velocity)

            # Stop ball reset two
            self.ball_reset_two = False

        # Update ball
        self.ball.update()

    def __get_monitor_resolution(self) -> tuple[int, int]:
        # Get tkinter widget
        root = tkinter.Tk()

        # Return dimensions from default pong
        return root.winfo_screenwidth(), root.winfo_screenheight()
