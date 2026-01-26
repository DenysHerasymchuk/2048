# Beautiful color scheme for 2048 tiles

# Background colors for each tile value
TILE_COLORS = {
    0: "#cdc1b4",      # Empty tile
    2: "#eee4da",      # Cream
    4: "#ede0c8",      # Light tan
    8: "#f2b179",      # Orange
    16: "#f59563",     # Dark orange
    32: "#f67c5f",     # Red-orange
    64: "#f65e3b",     # Red
    128: "#edcf72",    # Yellow
    256: "#edcc61",    # Gold
    512: "#edc850",    # Bright gold
    1024: "#edc53f",   # Deep gold
    2048: "#edc22e",   # Victory gold
    4096: "#3c3a32",   # Dark
    8192: "#3c3a32",   # Dark
}

# Text colors for each tile value
TEXT_COLORS = {
    0: "#cdc1b4",      # Same as background (invisible)
    2: "#776e65",      # Dark brown
    4: "#776e65",      # Dark brown
    8: "#f9f6f2",      # White
    16: "#f9f6f2",     # White
    32: "#f9f6f2",     # White
    64: "#f9f6f2",     # White
    128: "#f9f6f2",    # White
    256: "#f9f6f2",    # White
    512: "#f9f6f2",    # White
    1024: "#f9f6f2",   # White
    2048: "#f9f6f2",   # White
    4096: "#f9f6f2",   # White
    8192: "#f9f6f2",   # White
}

# UI Colors
BACKGROUND_COLOR = "#faf8ef"      # Main background
BOARD_COLOR = "#bbada0"           # Board background
HEADER_COLOR = "#776e65"          # Header text
SCORE_BG = "#bbada0"              # Score background
SCORE_TEXT = "#eee4da"            # Score label
SCORE_VALUE = "#ffffff"           # Score value
BUTTON_BG = "#8f7a66"             # Button background
BUTTON_TEXT = "#f9f6f2"           # Button text
BUTTON_HOVER = "#9f8b77"          # Button hover
GAME_OVER_OVERLAY = "#eee4da"     # Game over overlay
WIN_OVERLAY = "#edc22e"           # Win overlay


def get_tile_color(value):
    """Get background color for a tile value."""
    return TILE_COLORS.get(value, "#3c3a32")


def get_text_color(value):
    """Get text color for a tile value."""
    return TEXT_COLORS.get(value, "#f9f6f2")
