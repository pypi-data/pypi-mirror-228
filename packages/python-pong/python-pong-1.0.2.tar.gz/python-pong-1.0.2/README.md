# python-pong [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/dyrektrypt/python-pong/blob/master/LICENSE)
python-pong is a simple Python library for quickly setting up components and games of Pong in Pygame.

## Installation
python-pong can be installed from PyPI using pip. Simply run the command `python -m pip install python-pong`
globally, or in your virtual Python project environment, where `python` is your current Python distribution.

## Usage
The contents of the python-pong libraries packages is shown in the following:

### pong.components
```
Ball.py
    class Ball(screen: pygame.Surface, radius: float)
        def get_x()
        def set_x(x: int)
        def get_y()
        def set_y(y: int)
        def get_radius()
        def get_velocity()
        def set_velocity(velocity: pygame.Vector2)
        def update()
        
Controller.py
    class Controller(screen: pygame.Surface, rectangle: pygame.Rect)
        def get_x()
        def get_y()
        def get_width()
        def get_height()
        def get_velocity()
        def set_velocity(velocity: pygame.Vector2)
        def update()
        
Text.py 
    class Text(screen: pygame.Surface, coordinates: tuple[float, float]))
        def get_text()
        def set_text(x: int)
        def update()
```

### pong.game
```
Basic.py
    class Basic(
        controller_width=1/20,
        controller_height=2/3,
        player_velocity=None,
        ball_velocity=None,
        frame_rate=60,
        tick_rate=40#
    )
```

### pong.utility
```
colours.py
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
```


An example of the python-pong library being used to create a game of Pong from the Basic class is shown below:

```python
from pong.game.Basic import Basic


def main():
    # Create a Pong game
    Basic()

    
if __name__ == "__main__":
    main()
```