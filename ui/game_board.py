import tkinter as tk
from .colors import get_tile_color, get_text_color, BOARD_COLOR
from .styles import CELL_SIZE, CELL_PADDING, BOARD_PADDING, CORNER_RADIUS, get_tile_font, ANIMATION_DURATION


class AnimatedTile:
    """Represents a tile being animated."""
    def __init__(self, canvas, value, start_x, start_y, end_x, end_y, cell_size):
        self.canvas = canvas
        self.value = value
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.cell_size = cell_size
        self.current_x = start_x
        self.current_y = start_y
        self.tile_id = None
        self.text_id = None
        self._create_tile()

    def _create_tile(self):
        """Create the animated tile."""
        x, y = self.current_x, self.current_y
        # Draw rounded rectangle
        radius = CORNER_RADIUS
        points = [
            x + radius, y,
            x + self.cell_size - radius, y,
            x + self.cell_size, y,
            x + self.cell_size, y + radius,
            x + self.cell_size, y + self.cell_size - radius,
            x + self.cell_size, y + self.cell_size,
            x + self.cell_size - radius, y + self.cell_size,
            x + radius, y + self.cell_size,
            x, y + self.cell_size,
            x, y + self.cell_size - radius,
            x, y + radius,
            x, y,
            x + radius, y,
        ]
        self.tile_id = self.canvas.create_polygon(
            points, smooth=True,
            fill=get_tile_color(self.value),
            outline="",
            tags="animated"
        )

        self.text_id = self.canvas.create_text(
            x + self.cell_size // 2,
            y + self.cell_size // 2,
            text=str(self.value),
            fill=get_text_color(self.value),
            font=get_tile_font(self.value),
            tags="animated"
        )

    def update_position(self, progress):
        """Update tile position based on animation progress (0 to 1)."""
        # Easing function for smooth animation
        t = self._ease_out_quad(progress)

        new_x = self.start_x + (self.end_x - self.start_x) * t
        new_y = self.start_y + (self.end_y - self.start_y) * t

        dx = new_x - self.current_x
        dy = new_y - self.current_y

        self.canvas.move(self.tile_id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)

        self.current_x = new_x
        self.current_y = new_y

    def _ease_out_quad(self, t):
        """Quadratic ease-out for smooth deceleration."""
        return 1 - (1 - t) ** 2

    def destroy(self):
        """Remove the animated tile from canvas."""
        self.canvas.delete(self.tile_id)
        self.canvas.delete(self.text_id)


class GameBoard(tk.Canvas):
    """Visual representation of the 2048 game board."""

    def __init__(self, parent, board, **kwargs):
        self.board = board
        self.cell_size = CELL_SIZE
        self.padding = CELL_PADDING
        self.board_padding = BOARD_PADDING
        self.animating = False
        self.animation_callback = None

        # Calculate canvas size
        self.board_pixel_size = (
            self.cell_size * board.size
            + self.padding * (board.size + 1)
            + self.board_padding * 2
        )

        super().__init__(
            parent,
            width=self.board_pixel_size,
            height=self.board_pixel_size,
            bg=BOARD_COLOR,
            highlightthickness=0,
            **kwargs
        )

        self._draw_empty_board()

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _get_cell_coords(self, row, col):
        """Get the pixel coordinates for a cell."""
        x = (
            self.board_padding
            + self.padding
            + col * (self.cell_size + self.padding)
        )
        y = (
            self.board_padding
            + self.padding
            + row * (self.cell_size + self.padding)
        )
        return x, y

    def _draw_empty_board(self):
        """Draw the board background with empty cell slots."""
        self.delete("background")

        for row in range(self.board.size):
            for col in range(self.board.size):
                x, y = self._get_cell_coords(row, col)
                self._draw_rounded_rect(
                    x, y,
                    x + self.cell_size, y + self.cell_size,
                    CORNER_RADIUS,
                    fill=get_tile_color(0),
                    outline="",
                    tags="background"
                )

    def _draw_tile(self, row, col, value, tags="tile"):
        """Draw a single tile at the given position."""
        if value == 0:
            return None, None

        x, y = self._get_cell_coords(row, col)

        tile_id = self._draw_rounded_rect(
            x, y,
            x + self.cell_size, y + self.cell_size,
            CORNER_RADIUS,
            fill=get_tile_color(value),
            outline="",
            tags=tags
        )

        text_id = self.create_text(
            x + self.cell_size // 2,
            y + self.cell_size // 2,
            text=str(value),
            fill=get_text_color(value),
            font=get_tile_font(value),
            tags=tags
        )

        return tile_id, text_id

    def update_board(self):
        """Update the visual board instantly (no animation)."""
        self.delete("tile")
        self.delete("animated")
        self.delete("new_tile")
        self.delete("static")

        for row in range(self.board.size):
            for col in range(self.board.size):
                value = self.board.get_cell(row, col)
                if value != 0:
                    self._draw_tile(row, col, value)

    def animate_move(self, moves, new_tile_pos, old_grid, callback=None):
        """Animate tile movements."""
        if not moves:
            self.update_board()
            if callback:
                callback()
            return

        self.animating = True
        self.animation_callback = callback

        # Clear existing tiles
        self.delete("tile")
        self.delete("animated")
        self.delete("new_tile")

        # Find which cells are being animated (source positions)
        moving_cells = set()
        for move in moves:
            moving_cells.add((move.from_row, move.from_col))

        # Draw static tiles (tiles that don't move) from old_grid
        if old_grid:
            for row in range(self.board.size):
                for col in range(self.board.size):
                    if (row, col) not in moving_cells and old_grid[row][col] != 0:
                        self._draw_tile(row, col, old_grid[row][col], tags="static")

        # Create animated tiles
        self.animated_tiles = []
        for move in moves:
            start_x, start_y = self._get_cell_coords(move.from_row, move.from_col)
            end_x, end_y = self._get_cell_coords(move.to_row, move.to_col)

            tile = AnimatedTile(
                self, move.value,
                start_x, start_y,
                end_x, end_y,
                self.cell_size
            )
            self.animated_tiles.append(tile)

        # Store new tile position for later
        self.pending_new_tile = new_tile_pos

        # Start animation
        self.animation_start_time = None
        self._animate_step()

    def _animate_step(self):
        """Perform one step of the animation."""
        import time

        if self.animation_start_time is None:
            self.animation_start_time = time.time() * 1000

        current_time = time.time() * 1000
        elapsed = current_time - self.animation_start_time
        progress = min(1.0, elapsed / ANIMATION_DURATION)

        # Update all animated tiles
        for tile in self.animated_tiles:
            tile.update_position(progress)

        if progress < 1.0:
            # Continue animation
            self.after(8, self._animate_step)  # ~120 FPS
        else:
            # Animation complete
            self._finish_animation()

    def _finish_animation(self):
        """Clean up after animation completes."""
        # Remove animated tiles
        for tile in self.animated_tiles:
            tile.destroy()
        self.animated_tiles = []

        # Remove static tiles
        self.delete("static")

        # Draw final board state
        self.update_board()

        # Animate new tile appearing
        if self.pending_new_tile:
            self._animate_new_tile(self.pending_new_tile)
            self.pending_new_tile = None

        self.animating = False

        if self.animation_callback:
            self.after(50, self.animation_callback)

    def _animate_new_tile(self, pos):
        """Animate a new tile appearing with a pop effect."""
        row, col = pos
        value = self.board.get_cell(row, col)
        if value == 0:
            return

        x, y = self._get_cell_coords(row, col)
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2

        # Create small tile that will grow
        self._animate_pop(center_x, center_y, value, 0)

    def _animate_pop(self, center_x, center_y, value, step):
        """Animate tile pop-in effect."""
        max_steps = 6
        if step > max_steps:
            return

        self.delete("new_tile")

        # Calculate scale (starts small, grows to normal, slight overshoot, then settles)
        if step <= max_steps // 2:
            scale = 0.2 + (step / (max_steps // 2)) * 0.9
        else:
            overshoot = 1.1
            settle_progress = (step - max_steps // 2) / (max_steps // 2)
            scale = overshoot - (overshoot - 1.0) * settle_progress

        size = int(self.cell_size * scale)
        half = size // 2

        x1 = center_x - half
        y1 = center_y - half
        x2 = center_x + half
        y2 = center_y + half

        radius = int(CORNER_RADIUS * scale)
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1,
        ]

        self.create_polygon(
            points, smooth=True,
            fill=get_tile_color(value),
            outline="",
            tags="new_tile"
        )

        # Scale font size
        base_font = get_tile_font(value)
        font_size = int(base_font[1] * scale)
        scaled_font = (base_font[0], max(8, font_size), base_font[2])

        self.create_text(
            center_x, center_y,
            text=str(value),
            fill=get_text_color(value),
            font=scaled_font,
            tags="new_tile"
        )

        if step < max_steps:
            self.after(20, lambda: self._animate_pop(center_x, center_y, value, step + 1))
        else:
            # Final cleanup - redraw as normal tile
            self.after(10, self.update_board)

    def show_overlay(self, message, bg_color, text_color="#776e65", subtitle=None):
        """Show an overlay message on the board."""
        # Create darkened overlay background
        self.create_rectangle(
            0, 0, self.board_pixel_size, self.board_pixel_size,
            fill=bg_color,
            stipple="gray50",
            tags="overlay"
        )

        # Create message text
        center_y = self.board_pixel_size // 2
        if subtitle:
            center_y -= 20

        self.create_text(
            self.board_pixel_size // 2,
            center_y,
            text=message,
            fill=text_color,
            font=("Helvetica Neue", 48, "bold"),
            tags="overlay"
        )

        # Create subtitle if provided
        if subtitle:
            self.create_text(
                self.board_pixel_size // 2,
                center_y + 50,
                text=subtitle,
                fill=text_color,
                font=("Helvetica Neue", 16),
                tags="overlay"
            )

    def hide_overlay(self):
        """Hide the overlay message."""
        self.delete("overlay")

    def is_animating(self):
        """Check if animation is in progress."""
        return self.animating
