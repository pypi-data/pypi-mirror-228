# python-pong
python-pong is a simple, open-source Python library for quickly setting up components and games of Pong in Pygame.

## Installation
python-pong can be installed from PyPI using pip. Simply run the command `python -m pip install python-pong`
globally, or in your virtual Python project environment, where `python` is your current Python distribution.

## Usage
python-pong makes usage of multiple packages containing modules and classes that can be easily incorporated into a
Pygame Python project to assist the development of a custom game of Pong.

>### pong.components 
> The pong.components package contains only classes that implement individual components that can be
used within a game of Pong. Each component should be attached to a pygame.Surface object during instantiation.
> ### pong.game
> The pong.game package contains only classes that implement configurable
games of Pong in Pygame. These classes might require additional dependencies such as Tkinter within the Python standard library.
> ### pong.utility
> The pong.utility package contains modules that provide useful global constants, classes and functions for
development of a game of Pong in Pygame.

An example of the python-pong library being used to create a basic game of Pong is shown in the following:

```python
from pong.game.Basic import Basic


def main():
    # create a pre-configured instance of a basic Pong game
    Basic()

    
if __name__ == "__main__":
    main()
```