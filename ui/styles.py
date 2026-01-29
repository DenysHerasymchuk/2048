# UI Styling Constants
from game.constants import GRID_SIZE

# Window settings
WINDOW_TITLE = "2048"
WINDOW_MIN_WIDTH = 450
WINDOW_MIN_HEIGHT = 600

# Board dimensions - dynamically calculated based on grid size
MAX_BOARD_SIZE = 450  # Maximum board size in pixels
CELL_PADDING = 10
BOARD_PADDING = 10

# Calculate cell size to fit within max board size
# Formula: MAX_BOARD_SIZE = BOARD_PADDING*2 + CELL_PADDING*(GRID_SIZE+1) + CELL_SIZE*GRID_SIZE
_available_space = MAX_BOARD_SIZE - (BOARD_PADDING * 2) - (CELL_PADDING * (GRID_SIZE + 1))
CELL_SIZE = max(40, _available_space // GRID_SIZE)  # Minimum cell size of 40px

CORNER_RADIUS = max(4, min(8, CELL_SIZE // 12))  # Scale corner radius with cell size

# Typography
TITLE_FONT = ("Helvetica Neue", 48, "bold")
SCORE_LABEL_FONT = ("Helvetica Neue", 12, "bold")
SCORE_VALUE_FONT = ("Helvetica Neue", 22, "bold")
BUTTON_FONT = ("Helvetica Neue", 13, "bold")

# Scale tile fonts based on cell size (base size is 100px)
_font_scale = CELL_SIZE / 100.0
TILE_FONTS = {
    1: ("Helvetica Neue", max(16, int(44 * _font_scale)), "bold"),      # 2-9
    2: ("Helvetica Neue", max(14, int(40 * _font_scale)), "bold"),      # 10-99
    3: ("Helvetica Neue", max(12, int(34 * _font_scale)), "bold"),      # 100-999
    4: ("Helvetica Neue", max(10, int(28 * _font_scale)), "bold"),      # 1000-9999
    5: ("Helvetica Neue", max(8, int(22 * _font_scale)), "bold"),       # 10000+
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
