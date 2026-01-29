#!/usr/bin/env python3
"""
2048 Game - A beautiful tkinter implementation

Controls:
    - Arrow keys or WASD to move tiles
    - R to restart the game
    - Space to continue after winning

Author: 2048 Project
"""

import sys


def main():
    """Main entry point for the 2048 game."""
    try:
        from ui.app import Game2048App
        app = Game2048App()
        app.run()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nProgram stopped: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
