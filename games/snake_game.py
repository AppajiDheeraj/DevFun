from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical
from rich.text import Text

from textual import events
import random
import asyncio

class SnakeGameScreen(Screen):
    BINDINGS = [("escape", "quit_game", "Back to Menu")]

    def __init__(self):
        super().__init__()
        self.board_width = 20
        self.board_height = 10
        self.snake = [(self.board_width // 2, self.board_height // 2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.game_loop_task = None
        self.horizontal_speed = 0.1
        self.vertical_speed = 0.18

    def compose(self):
        yield Header()
        with Vertical(id="game-wrapper"):
            yield Static(f"🎯 Score: {self.score}", id="score_display", classes="game-info")
            yield Static(self.render_board(), id="game_board")
            yield Static("Play as if the game is yours!!", classes="game-info")
        yield Footer()

    def on_mount(self):
        self.query_one(Header).title = "🐍 Snake Game"
        self.game_loop_task = self.set_interval(self.horizontal_speed, self.update_game)

    def generate_food(self):
        while True:
            fx = random.randint(0, self.board_width - 1)
            fy = random.randint(0, self.board_height - 1)
            if (fx, fy) not in self.snake:
                return (fx, fy)

    def update_game(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if not (0 <= new_head[0] < self.board_width and 0 <= new_head[1] < self.board_height):
            self.end_game("💥 Hit a wall!")
            return

        if new_head in self.snake[1:]:
            self.end_game("😵 Bit yourself!")
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            self.query_one("#score_display", Static).update(f"🎯 Score: {self.score}")
        else:
            self.snake.pop()

        self.query_one("#game_board", Static).update(Text(self.render_board(), justify="center"))

    def render_board(self):
        board = [[" " for _ in range(self.board_width)] for _ in range(self.board_height)]
        for i, (x, y) in enumerate(self.snake):
            board[y][x] = "@" if i == 0 else "O"
        fx, fy = self.food
        board[fy][fx] = "●"
        lines = ["╔" + "═" * self.board_width + "╗"]
        for row in board:
            lines.append("║" + "".join(row) + "║")
        lines.append("╚" + "═" * self.board_width + "╝")
        return "\n".join(lines)

    def on_key(self, event: events.Key):
        if self.game_over:
            if event.key == "escape":
                self.action_quit_game()
            return

        previous_direction = self.direction

        if event.key == "up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif event.key == "down" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif event.key == "left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif event.key == "right" and self.direction != (-1, 0):
            self.direction = (1, 0)

        is_vertical = self.direction[0] == 0
        was_vertical = previous_direction[0] == 0

        if is_vertical != was_vertical:
            # --- CHANGE START ---
            # Corrected the method call from .cancel() to .stop()
            self.game_loop_task.stop()
            # --- CHANGE END ---
            new_speed = self.vertical_speed if is_vertical else self.horizontal_speed
            self.game_loop_task = self.set_interval(new_speed, self.update_game)

    def end_game(self, message: str):
        self.game_over = True
        # --- CHANGE START ---
        # Stop the timer when the game ends to prevent further updates
        if self.game_loop_task:
            self.game_loop_task.stop()
        # --- CHANGE END ---
        self.query_one("#score_display", Static).update(f"{message} Final Score: {self.score}")
        async def return_to_menu():
            await asyncio.sleep(3)
            await self.app.pop_screen()
        asyncio.create_task(return_to_menu())

    def action_quit_game(self):
        # --- CHANGE START ---
        # Also ensure the timer is stopped when quitting manually
        if self.game_loop_task:
            self.game_loop_task.stop()
            self.game_loop_task = None
        # --- CHANGE END ---
        self.dismiss()

