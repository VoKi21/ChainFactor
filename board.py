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
        score = 0
        self.check_horizontal_matches()
        self.check_vertical_matches()
        self.remove_marked()
        self.gravitation()
        score += self.balls_removed
        if self.balls_removed > 0:
            self.balls_removed = 0
            score += 2 * self.check_matches()
        return score

    def check_horizontal_matches(self):
        for row in range(self.rows):
            self.check_row(row)

    def check_row(self, row):
        groups = []
        current_group = []
        for col in range(self.cols):
            if self.grid[row][col] is not None:
                current_group.append(col)
            else:
                if len(current_group) > 0:
                    groups.append(current_group.copy())
                    current_group = []
        if len(current_group) > 0:
            groups.append(current_group)
        for group in groups:
            if len(group) > 0:
                self.mark_balls_with_value_in_row(row, group, len(group))

    def check_vertical_matches(self):
        for col in range(self.cols):
            self.check_column(col)

    def check_column(self, col):
        curr_length = 0
        for row in range(self.rows):
            if self.grid[row][col] is not None:
                curr_length += 1
        self.mark_balls_with_value_in_column(col, curr_length)

    def gravitation(self):
        fallen = True
        while fallen:
            fallen = False
            for col in range(self.cols):
                for row in range(self.rows - 1):
                    if self.grid[row][col] is not None and self.grid[row + 1][col] is None:
                        (self.grid[row][col], self.grid[row + 1][col]) = (self.grid[row + 1][col], self.grid[row][col])
                        fallen = True

    def mark_balls_with_value_in_row(self, row, group, value):
        for i in group:
            if (self.grid[row][i].value == value and
                    self.grid[row][i].protection <= 0):
                self.grid[row][i].to_remove = True

    def mark_balls_with_value_in_column(self, col, value):
        for i in range(self.rows):
            if (self.grid[i][col] is not None and
                    self.grid[i][col].value == value and
                    self.grid[i][col].protection <= 0):
                self.grid[i][col].to_remove = True

    def remove_marked(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] is not None and self.grid[row][col].to_remove:
                    self.remove_ball(row, col)

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
