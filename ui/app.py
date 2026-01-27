import tkinter as tk
import os

from game.board import Board
from game.constants import UP, DOWN, LEFT, RIGHT
from game.logic import GameLogic
from .game_board import GameBoard
from .colors import (
    BACKGROUND_COLOR, HEADER_COLOR, SCORE_BG, SCORE_TEXT, SCORE_VALUE,
    BUTTON_BG, BUTTON_TEXT, BUTTON_HOVER, GAME_OVER_OVERLAY, WIN_OVERLAY
)
from .styles import (
    WINDOW_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    TITLE_FONT, SCORE_LABEL_FONT, SCORE_VALUE_FONT, BUTTON_FONT,
    GAME_OVER_FONT, SUBTITLE_FONT
)


class Game2048App:
    """Main application window for the 2048 game."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)

        # Set window icon
        self._set_icon()

        # Initialize game state
        self.board = Board()
        self.logic = GameLogic(self.board)

        # Build UI
        self._create_widgets()
        self._bind_keys()

        # Start new game
        self.new_game()

        # Center window on screen
        self._center_window()

    def _set_icon(self):
        """Set the window icon from storage/avatar.png."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "storage", "avatar.png")

            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
                self._icon = icon  # Keep reference to prevent garbage collection
        except Exception:
            pass  # Icon is optional, continue without it

    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_frame.pack(padx=20, pady=20)

        # Header section
        self._create_header()

        # Game board
        self.game_board = GameBoard(self.main_frame, self.board)
        self.game_board.pack(pady=(20, 0))

        # Instructions
        self._create_instructions()

    def _create_header(self):
        """Create the header with title, scores, and buttons."""
        header_frame = tk.Frame(self.main_frame, bg=BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X)

        # Left side - Title
        left_frame = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        left_frame.pack(side=tk.LEFT)

        title_label = tk.Label(
            left_frame,
            text="2048",
            font=TITLE_FONT,
            fg=HEADER_COLOR,
            bg=BACKGROUND_COLOR
        )
        title_label.pack(anchor=tk.W)

        # Right side - Scores and buttons
        right_frame = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        right_frame.pack(side=tk.RIGHT)

        # Score boxes container
        scores_frame = tk.Frame(right_frame, bg=BACKGROUND_COLOR)
        scores_frame.pack()

        # Score box
        self.score_frame = self._create_score_box(scores_frame, "SCORE", 0)
        self.score_frame.pack(side=tk.LEFT, padx=(0, 5))

        # Best score box
        self.best_frame = self._create_score_box(scores_frame, "BEST", 0)
        self.best_frame.pack(side=tk.LEFT)

        # Buttons
        buttons_frame = tk.Frame(right_frame, bg=BACKGROUND_COLOR)
        buttons_frame.pack(pady=(10, 0))

        self.new_game_btn = self._create_button(
            buttons_frame, "New Game", self.new_game
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=(0, 5))

    def _create_score_box(self, parent, label_text, value):
        """Create a score display box."""
        frame = tk.Frame(parent, bg=SCORE_BG, padx=15, pady=8)

        label = tk.Label(
            frame,
            text=label_text,
            font=SCORE_LABEL_FONT,
            fg=SCORE_TEXT,
            bg=SCORE_BG
        )
        label.pack()

        value_label = tk.Label(
            frame,
            text=str(value),
            font=SCORE_VALUE_FONT,
            fg=SCORE_VALUE,
            bg=SCORE_BG
        )
        value_label.pack()

        # Store reference to value label for updates
        frame.value_label = value_label
        return frame

    def _create_button(self, parent, text, command):
        """Create a styled button."""
        btn = tk.Button(
            parent,
            text=text,
            font=BUTTON_FONT,
            fg=BUTTON_TEXT,
            bg=BUTTON_BG,
            activeforeground=BUTTON_TEXT,
            activebackground=BUTTON_HOVER,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=command
        )

        # Hover effects
        btn.bind("<Enter>", lambda e: btn.configure(bg=BUTTON_HOVER))
        btn.bind("<Leave>", lambda e: btn.configure(bg=BUTTON_BG))

        return btn

    def _create_instructions(self):
        """Create the instructions section."""
        instructions_frame = tk.Frame(self.main_frame, bg=BACKGROUND_COLOR)
        instructions_frame.pack(pady=(20, 0))

        instruction_text = tk.Label(
            instructions_frame,
            text="Use arrow keys or WASD to move tiles.",
            font=SUBTITLE_FONT,
            fg=HEADER_COLOR,
            bg=BACKGROUND_COLOR
        )
        instruction_text.pack()

        goal_text = tk.Label(
            instructions_frame,
            text="Join the tiles to get to 2048!",
            font=SUBTITLE_FONT,
            fg=HEADER_COLOR,
            bg=BACKGROUND_COLOR
        )
        goal_text.pack()

    def _bind_keys(self):
        """Bind keyboard controls."""
        self.root.bind("<Up>", lambda e: self._handle_move(UP))
        self.root.bind("<Down>", lambda e: self._handle_move(DOWN))
        self.root.bind("<Left>", lambda e: self._handle_move(LEFT))
        self.root.bind("<Right>", lambda e: self._handle_move(RIGHT))

        # WASD controls
        self.root.bind("<w>", lambda e: self._handle_move(UP))
        self.root.bind("<W>", lambda e: self._handle_move(UP))
        self.root.bind("<s>", lambda e: self._handle_move(DOWN))
        self.root.bind("<S>", lambda e: self._handle_move(DOWN))
        self.root.bind("<a>", lambda e: self._handle_move(LEFT))
        self.root.bind("<A>", lambda e: self._handle_move(LEFT))
        self.root.bind("<d>", lambda e: self._handle_move(RIGHT))
        self.root.bind("<D>", lambda e: self._handle_move(RIGHT))

        # New game shortcut
        self.root.bind("<r>", lambda e: self.new_game())
        self.root.bind("<R>", lambda e: self.new_game())

    def _handle_move(self, direction):
        """Handle a move action."""
        # Don't allow moves during animation
        if self.game_board.is_animating():
            return

        if self.board.game_over and not self.board.keep_playing:
            return

        if self.board.won and not self.board.keep_playing:
            return

        moved = self.logic.move(direction)

        if moved:
            self._animate_move()

    def _animate_move(self):
        """Animate the tile movement."""
        moves = self.logic.last_moves
        new_tile_pos = self.logic.new_tile_pos
        old_grid = self.logic.old_grid

        def on_animation_complete():
            self._update_scores()
            self._check_game_state()

        self.game_board.animate_move(moves, new_tile_pos, old_grid, on_animation_complete)

    def _check_game_state(self):
        """Check for game over or win conditions."""
        if self.board.game_over:
            self.game_board.show_overlay(
                "Game Over!",
                GAME_OVER_OVERLAY,
                "#776e65",
                subtitle="Press any key to try again"
            )
            self._bind_restart_on_any_key()
        elif self.board.won and not self.board.keep_playing:
            self._show_win_dialog()

    def _bind_restart_on_any_key(self):
        """Bind any key press to restart the game."""
        self.root.bind("<Key>", self._restart_on_key)
        self.game_board.bind("<Button-1>", self._restart_on_key)

    def _restart_on_key(self, event=None):
        """Restart game when any key is pressed."""
        self.root.unbind("<Key>")
        self.game_board.unbind("<Button-1>")
        self.new_game()

    def _update_scores(self):
        """Update score displays."""
        self.score_frame.value_label.config(text=str(self.board.score))
        self.best_frame.value_label.config(text=str(self.board.best_score))

    def _show_win_dialog(self):
        """Show the win dialog."""
        self.game_board.show_overlay("You Win!", WIN_OVERLAY, "#ffffff")

        # Create continue button overlay
        self.root.after(100, self._add_continue_option)

    def _add_continue_option(self):
        """Add option to continue playing after winning."""
        # This could be enhanced with a proper dialog
        # For now, just allow continuing by pressing any key
        self.root.bind("<space>", self._continue_playing)

    def _continue_playing(self, event=None):
        """Continue playing after winning."""
        self.board.keep_playing = True
        self.board.won = False
        self.game_board.hide_overlay()
        self.root.unbind("<space>")

    def new_game(self):
        """Start a new game."""
        self.board.reset()
        self.game_board.hide_overlay()
        self.game_board.update_board()
        self._update_scores()

    def run(self):
        """Run the application."""
        self.root.mainloop()
