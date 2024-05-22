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
        self.board = Board(rows=8, cols=7)
        self.next_ball = None
        self.scores = 0
        self.game_over = False
        self.colors = ["#FF0000", "#FF8800", "#FFFF00", "#00FF00", "#00FFFF", "#6666FF", "#FF00FF"]
        self.setup_game()

    def setup_game(self):
        self.start_falling_ball()
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                button = self.window.table[row - 1][col]
                col1 = col
                button.clicked.connect(lambda checked=False, column=col1: self.handle_button_click(column))

        self.update_info()
        self.window.restart_button.clicked.connect(lambda checked: self.restart())
        self.window.settings_window.finished.connect(lambda checked: self.update_info())

        self.window.show()
        sys.exit(self.app.exec())

    def update_info(self):
        for row in range(1, self.board.rows):
            for col in range(self.board.cols):
                ball = self.board.grid[row][col]
                text = ""
                style = f"background-color: {self.window.default_background}; border: 1px solid black;"
                if ball:
                    if ball.protection == 1:
                        style = "background-color: gray; border-radius: 30%;"
                    elif ball.protection == 2:
                        style = "background-color: black; border-radius: 30%;"
                    else:
                        text = ball.value
                        style = (f"background-color: {self.colors[ball.value - 1]};"
                                 f" border: 1px solid black; border-radius: 30%; color: black")
                self.window.table[row - 1][col].setText(str(text))
                self.window.table[row - 1][col].setStyleSheet(style)

        self.window.level_label.clear()
        self.window.drops_label.clear()

        self.window.level_label.setText(f"Level {self.board.current_level}")
        self.window.drops_label.setText(f"{self.board.drop_count} drops left")
        self.window.progress_bar.setRange(0, self.board.max_drop_count)
        self.window.progress_bar.setValue(self.board.drop_count)

        self.window.scores_label.setText(f"Scores: {self.scores}")

    def handle_button_click(self, col):
        if self.board.grid[1][col] is not None or self.game_over:
            return

        self.board.drop_ball(self.next_ball, col)

        self.update_scores(self.board.check_matches())
        if self.board.drop_count <= 0:
            self.board.next_level()
            self.update_scores(100 + self.board.check_matches())
        self.start_falling_ball()
        self.update_info()

        if self.board.is_game_over():
            self.window.restart_button.setText("Game over. Restart")
            self.window.restart_button.setStyleSheet(f"background-color: {self.colors[0]};")
            self.game_over = True

    def start_falling_ball(self):
        value = random.randint(1, 7)
        protected = random.random() > 0.66
        self.next_ball = Ball(value, protected)
        self.window.falling_ball_label.setText(
            f"Falling ball: {0 if self.next_ball.protection > 0 else self.next_ball.value}"
        )
        self.window.falling_ball_label.setStyleSheet(
            f"background-color: {self.colors[self.next_ball.value - 1] if self.next_ball.protection == 0 else ""};")

    def update_scores(self, scores):
        self.scores += scores
        self.window.scores_label.setText(f"Scores: {self.scores}")

    def restart(self):
        self.board = Board(rows=8, cols=7)
        self.window.restart_button.setText("Restart")
        self.window.restart_button.setStyleSheet("")
        self.game_over = False
        self.scores = 0
        self.start_falling_ball()
        self.update_info()


if __name__ == "__main__":
    game = Main()
