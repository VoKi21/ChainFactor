import random
import sys

from PyQt6.QtWidgets import QApplication

from ball import Ball
from board import Board
from game_window import GameWindow


class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = GameWindow()
        self.board = Board(rows=8, cols=7)  # Example, adjust as needed
        self.next_ball = None
        self.scores = 0  # Initialize scores
        self.setup_game()

    def setup_game(self):
        self.start_falling_ball()
        # Connect signals and slots
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                button = self.window.table[row - 1][col]
                col1 = col
                button.clicked.connect(lambda checked=False, column=col1: self.handle_button_click(column))

        self.update_info()

        # Run the game
        self.window.show()
        sys.exit(self.app.exec())

    def update_info(self):
        for row in range(1, self.board.rows):
            for col in range(self.board.cols):
                ball = self.board.grid[row][col]
                text = ""
                if ball:
                    if ball.protection == 1:
                        text = "X"
                    elif ball.protection == 2:
                        text = "0"
                    else:
                        text = ball.value
                self.window.table[row - 1][col].setText(str(text))

        # Clear previous text on labels
        self.window.level_label.clear()
        self.window.drops_label.clear()

        # Update level label and drops label
        self.window.level_label.setText(f"Level {self.board.current_level}")
        self.window.drops_label.setText(f"{self.board.drop_count} drops left")
        self.window.progress_bar.setRange(0, self.board.max_drop_count)
        self.window.progress_bar.setValue(self.board.drop_count)

        # Update scores label
        self.window.scores_label.setText(f"Scores: {self.scores}")

    def handle_button_click(self, col):
        if self.board.grid[1][col] is not None:
            return  # Ignore if the top row is occupied

        self.board.drop_ball(self.next_ball, col)

        self.update_scores(self.board.check_matches())  # Update scores based on removed balls
        if self.board.drop_count <= 0:
            self.board.next_level()
            self.update_scores(100 + self.board.check_matches())
        self.start_falling_ball()
        self.update_info()

        # Check for game over
        if self.board.is_game_over():
            print("Game Over!")
            sys.exit()

    def start_falling_ball(self):
        value = random.randint(1, 7)
        protected = random.random() > 0.66
        self.next_ball = Ball(value, protected)
        self.window.falling_ball_label.setText(
            f"Falling ball: {0 if self.next_ball.protection > 0 else self.next_ball.value}"
        )

    def update_scores(self, scores):
        self.scores += scores
        self.window.scores_label.setText(f"Scores: {self.scores}")


if __name__ == "__main__":
    game = Main()
