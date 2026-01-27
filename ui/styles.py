# UI Styling Constants

# Window settings
WINDOW_TITLE = "2048"
WINDOW_MIN_WIDTH = 450
WINDOW_MIN_HEIGHT = 600

# Board dimensions
CELL_SIZE = 100
CELL_PADDING = 12
BOARD_PADDING = 12
CORNER_RADIUS = 8

# Typography
TITLE_FONT = ("Helvetica Neue", 48, "bold")
SCORE_LABEL_FONT = ("Helvetica Neue", 12, "bold")
SCORE_VALUE_FONT = ("Helvetica Neue", 22, "bold")
BUTTON_FONT = ("Helvetica Neue", 13, "bold")
TILE_FONTS = {
    1: ("Helvetica Neue", 44, "bold"),      # 2-9
    2: ("Helvetica Neue", 40, "bold"),      # 10-99
    3: ("Helvetica Neue", 34, "bold"),      # 100-999
    4: ("Helvetica Neue", 28, "bold"),      # 1000-9999
    5: ("Helvetica Neue", 22, "bold"),      # 10000+
}
GAME_OVER_FONT = ("Helvetica Neue", 36, "bold")
SUBTITLE_FONT = ("Helvetica Neue", 14)

# Animation
ANIMATION_DURATION = 100  # milliseconds


def get_tile_font(value):
    """Get appropriate font size based on tile value."""
    if value == 0:
        return TILE_FONTS[1]
    digits = len(str(value))
    return TILE_FONTS.get(digits, TILE_FONTS[5])
