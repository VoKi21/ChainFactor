import random

from ball import Ball


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.max_drop_count = 30
        self.drop_count = self.max_drop_count
        self.current_level = 1
        self.balls_removed = 0

    def check_matches(self):
        count = 0
        score = 0
        count += self.check_horizontal_matches()
        count += self.check_vertical_matches()
        self.gravitation()
        if count > 0:
            score += 2 * self.check_matches()
        score += max(0, 2 ** self.balls_removed - 1)
        self.balls_removed = 0
        return score

    def check_horizontal_matches(self):
        count = 0
        for row in range(self.rows):
            while self.check_row(row):
                count += 1
        return count

    def check_row(self, row):
        curr_length = 0
        cleared = False
        for col in range(self.cols + 1):
            if col < self.cols and self.grid[row][col] is not None:
                curr_length += 1
            elif curr_length != 0:
                cleared = self.remove_balls_with_value_in_row(row, col - curr_length, col, curr_length)
                curr_length = 0
        return cleared

    def check_vertical_matches(self):
        count = 0
        for col in range(self.cols):
            while self.check_column(col):
                count += 1
        return count

    def check_column(self, col):
        curr_length = 0
        cleared = False
        for row in range(self.rows + 1):
            if row < self.rows and self.grid[row][col] is not None:
                curr_length += 1
            elif curr_length != 0:
                cleared = self.remove_balls_with_value_in_column(col, row - curr_length, row, curr_length)
                curr_length = 0
        return cleared

    def gravitation(self):
        fallen = True
        while fallen:
            fallen = False
            for col in range(self.cols):
                for row in range(self.rows - 1):
                    if self.grid[row][col] is not None and self.grid[row + 1][col] is None:
                        (self.grid[row][col], self.grid[row + 1][col]) = (self.grid[row + 1][col], self.grid[row][col])
                        fallen = True

    def remove_balls_with_value_in_row(self, row, start, end, value):
        removed = False
        for i in range(start, end):
            if self.grid[row][i].value == value and self.grid[row][i].protection <= 0:
                self.remove_ball(row, i)
                removed = True
        return removed

    def remove_balls_with_value_in_column(self, col, start, end, value):
        removed = False
        for i in range(start, end):
            if self.grid[i][col].value == value and self.grid[i][col].protection <= 0:
                self.remove_ball(i, col)
                removed = True
        return removed

    def remove_ball(self, row, col):
        self.grid[row][col] = None
        self.balls_removed += 1
        for r, c in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] is not None:
                self.grid[r][c].protection -= 1

    def next_level(self):
        self.current_level += 1
        self.max_drop_count -= 1
        self.drop_count = self.max_drop_count
        for r in range(self.rows - 1):
            self.grid[r] = self.grid[r + 1]
        self.grid[self.rows - 1] = [Ball(random.randint(1, 7), True) for _ in range(self.cols)]

    def is_game_over(self):
        for col in range(self.cols):
            if self.grid[0][col] is not None:
                return True
        for col in range(self.cols):
            if self.grid[1][col] is None:
                return False
        return True

    def drop_ball(self, ball, col):
        if self.grid[0][col] is None:
            latest_empty = 0
            for i in range(1, self.rows):
                if self.grid[i][col] is None:
                    latest_empty += 1
                else:
                    break
            self.grid[latest_empty][col] = ball
        self.drop_count -= 1
