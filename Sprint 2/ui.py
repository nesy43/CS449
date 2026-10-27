import tkinter as tk
from tkinter import messagebox

from board import PEG, EMPTY, BLOCK, create_board, count_pegs
from moves import make_move
from game_over import is_game_over, is_winner


class PegSolitaireUI:
    """Tkinter drag-and-drop interface for Peg Solitaire."""

    CANVAS_SIZE = 720
    PADDING = 35

    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.resizable(False, False)

        self.board_type = tk.StringVar(value="english")
        self.size_text = tk.StringVar(value="7")
        self.status_text = tk.StringVar(
            value="Choose a board type and size, then click New Game."
        )

        self.board = None
        self.active_board_type = None
        self.cell_size = 0
        self.origin_x = 0
        self.origin_y = 0
        self.drag_start = None
        self.drag_item = None
        self.drag_offset = (0, 0)

        # Tracks the peg selected by clicking.
        self.selected_cell = None

        # Tracks the mouse press so clicks and drags can be distinguished.
        self.press_cell = None
        self.press_position = None

        controls = tk.Frame(root, padx=12, pady=10)
        controls.pack(fill="x")

        tk.Label(controls, text="Board type:").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        for col, (label, value) in enumerate(
            [("English", "english"),
             ("Diamond", "diamond"),
             ("Hexagon", "hexagon")],
            start=1,
        ):
            tk.Radiobutton(
                controls,
                text=label,
                variable=self.board_type,
                value=value,
            ).grid(row=0, column=col, sticky="w", padx=4)

        tk.Label(controls, text="Board size (odd, 7+):").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        tk.Entry(
            controls, textvariable=self.size_text, width=8
        ).grid(row=1, column=1, sticky="w", pady=(8, 0))

        tk.Button(
            controls,
            text="New Game",
            command=self.new_game,
            padx=12,
        ).grid(row=1, column=2, sticky="w", padx=8, pady=(8, 0))

        self.canvas = tk.Canvas(
            root,
            width=self.CANVAS_SIZE,
            height=self.CANVAS_SIZE,
            background="#f3f0e8",
            highlightthickness=0,
        )
        self.canvas.pack(padx=12, pady=(0, 8))
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        tk.Label(
            root,
            textvariable=self.status_text,
            anchor="w",
            padx=12,
            pady=10,
            wraplength=self.CANVAS_SIZE,
        ).pack(fill="x")

    def new_game(self):
        """Validate settings and create a fresh board."""
        board_type = self.board_type.get()

        try:
            size = int(self.size_text.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid size", "Enter an odd whole number of at least 7."
            )
            return

        if size < 7 or size % 2 == 0:
            messagebox.showerror(
                "Invalid size", "Board size must be odd and at least 7."
            )
            return

        try:
            self.board = create_board(board_type, size)
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Could not create board", str(exc))
            return

        self.active_board_type = board_type
        self.drag_start = None
        self.selected_cell = None
        self.press_cell = None
        self.press_position = None
        self.clear_drag_item()
        self.draw_board()
        self.update_status("New game started.")

    def clear_drag_item(self):
        if self.drag_item is not None:
            self.canvas.delete(self.drag_item)
            self.drag_item = None

    def draw_board(self):
        self.canvas.delete("all")
        if self.board is None:
            self.canvas.create_text(
                self.CANVAS_SIZE / 2,
                self.CANVAS_SIZE / 2,
                text="Select your settings and click New Game",
                font=("Arial", 16),
                fill="#555555",
            )
            return

        size = len(self.board)
        available = self.CANVAS_SIZE - 2 * self.PADDING
        self.cell_size = min(available / size, 76)
        board_pixels = self.cell_size * size
        self.origin_x = (self.CANVAS_SIZE - board_pixels) / 2
        self.origin_y = (self.CANVAS_SIZE - board_pixels) / 2
        radius = self.cell_size * 0.34

        for row in range(size):
            for col in range(size):
                cell = self.board[row][col]
                if cell == BLOCK:
                    continue

                is_selected = (row, col) == self.selected_cell

                x, y = self.cell_center(row, col)
                self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill="#d9d1c2",
                    outline="#8b8172",
                    width=2,
                )

                if cell == PEG:
                    peg_radius = radius * 0.78
                    self.canvas.create_oval(
                        x - peg_radius,
                        y - peg_radius,
                        x + peg_radius,
                        y + peg_radius,
                        fill="#356b8c",
                        outline="#20475e",
                        width=2,
                        tags=("peg", f"peg-{row}-{col}"),
                    )
                    self.canvas.create_oval(
                        x - peg_radius * 0.45,
                        y - peg_radius * 0.5,
                        x - peg_radius * 0.05,
                        y - peg_radius * 0.1,
                        fill="#8fb8ce",
                        outline="",
                        tags=("peg", f"peg-{row}-{col}"),
                    )

    def cell_center(self, row, col):
        x = self.origin_x + (col + 0.5) * self.cell_size
        y = self.origin_y + (row + 0.5) * self.cell_size
        return x, y

    def point_to_cell(self, x, y):
        """Convert canvas coordinates into board row and column."""
        if self.board is None or self.cell_size <= 0:
            return None

        col = int((x - self.origin_x) / self.cell_size)
        row = int((y - self.origin_y) / self.cell_size)

        if 0 <= row < len(self.board) and 0 <= col < len(self.board):
            if self.board[row][col] != BLOCK:
                return row, col

        return None


    def on_press(self, event):
        if self.board is None:
            return

        if is_game_over(self.board, self.active_board_type):
            return

        self.press_cell = self.point_to_cell(event.x, event.y)
        self.press_position = (event.x, event.y)
        self.drag_start = None

        cell = self.press_cell

        # Clicking outside the playable board cancels selection.
        if cell is None:
            self.selected_cell = None
            self.draw_board()
            return

        row, col = cell

        # Only pegs can be dragged.
        if self.board[row][col] == PEG:
            self.drag_start = cell

            x, y = self.cell_center(row, col)
            radius = self.cell_size * 0.34 * 0.78

            self.drag_item = self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill="#356b8c",
                outline="#20475e",
                width=2,
                tags=("dragged-peg",),
            )


    def on_drag(self, event):
        if self.drag_start is None or self.drag_item is None:
            return

        # Move the temporary peg image with the mouse.
        radius = self.cell_size * 0.34 * 0.78

        self.canvas.coords(
            self.drag_item,
            event.x - radius,
            event.y - radius,
            event.x + radius,
            event.y + radius,
        )


    def on_release(self, event):
        if self.press_position is None:
            return

        start = self.drag_start
        start_cell = self.press_cell

        # Determine whether the mouse moved enough to count as a drag.
        dx = event.x - self.press_position[0]
        dy = event.y - self.press_position[1]
        was_drag = dx * dx + dy * dy > 36

        target = self.point_to_cell(event.x, event.y)

        self.clear_drag_item()

        self.drag_start = None
        self.press_cell = None
        self.press_position = None

        # Handle drag-and-drop moves.
        if was_drag and start is not None:
            if target is None:
                self.selected_cell = None
                self.draw_board()
                self.update_status("Invalid move: release the peg in an empty hole.")
                return

            end_row, end_col = target
            move = (start[0], start[1], end_row, end_col)

            if make_move(self.board, self.active_board_type, move):
                self.selected_cell = None
                self.draw_board()
                self.update_status("Move completed.")
            else:
                self.selected_cell = None
                self.draw_board()
                self.update_status(
                    "Invalid move. Jump over one peg into an empty hole."
                )

            return

        # Handle ordinary clicks.
        if start_cell is None:
            self.selected_cell = None
            self.draw_board()
            return

        row, col = start_cell

        # Clicking a peg selects it or switches to another peg.
        if self.board[row][col] == PEG:
            self.selected_cell = start_cell
            self.draw_board()
            self.status_text.set(
                f"Peg selected at row {row + 1}, column {col + 1}. "
                "Click an empty hole to move."
            )
            return

        # Clicking an empty hole attempts a move from the selected peg.
        if self.board[row][col] == EMPTY and self.selected_cell is not None:
            start_row, start_col = self.selected_cell
            move = (start_row, start_col, row, col)

            if make_move(self.board, self.active_board_type, move):
                self.selected_cell = None
                self.draw_board()
                self.update_status("Move completed.")
            else:
                # An invalid destination cancels the current selection.
                self.selected_cell = None
                self.draw_board()
                self.update_status(
                    "Invalid move. Selection canceled. "
                    "Jump over one peg into an empty hole."
                )

            return

        # Any other click cancels selection.
        self.selected_cell = None
        self.draw_board()
        self.update_status("Selection canceled.")



    def update_status(self, message):
        if self.board is None:
            self.status_text.set(message)
            return

        pegs = count_pegs(self.board)

        if is_game_over(self.board, self.active_board_type):
            if is_winner(self.board):
                message = "You win! Only one peg remains."
                self.status_text.set(message)
                messagebox.showinfo("Game Over - You Win!", message)
            else:
                message = (
                    f"Game over! No valid moves remain.\n"
                    f"You have {pegs} pegs left."
                )
                self.status_text.set(message)
                messagebox.showinfo("Game Over", message)
        else:
            self.status_text.set(
                f"{message} Pegs remaining: {pegs}."
            )
