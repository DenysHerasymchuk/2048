#!/usr/bin/env python3
"""
2048 Game - A beautiful tkinter implementation

Controls:
    - Arrow keys or WASD to move tiles
    - R to restart the game
    - Space to continue after winning

Author: 2048 Project
"""

from ui.app import Game2048App


def main():
    """Main entry point for the 2048 game."""
    app = Game2048App()
    app.run()


if __name__ == "__main__":
    main()
