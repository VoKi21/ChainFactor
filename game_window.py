from PyQt6.QtWidgets import QGridLayout, QWidget, QMainWindow, QLabel, QProgressBar, QPushButton, QTextBrowser, \
    QVBoxLayout, QDialog, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.clicked.emit()


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_window = SettingsWindow(self)
        self.table = None
        self.falling_ball_label = None
        self.level_label = None
        self.drops_label = None
        self.progress_bar = None
        self.scores_label = None
        self.setWindowTitle("PyQt6 Chain Factor Game")
        self.setMinimumSize(425, 510)  # Set minimum size
        self.setMaximumSize(425, 510)  # Set maximum size
        self.default_background = "#FFFFFF"
        self.init_ui()

    def init_ui(self):
        self.init_stylesheets()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)
        self.table = []

        # Create the game board
        for row in range(7):  # Example size, adjust as needed
            row_labels = []
            for col in range(7):
                label = ClickableLabel()
                label.setFixedSize(60, 60)  # Set fixed size for consistent layout
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align text
                label.setStyleSheet(f"background-color: {self.default_background}; border: 1px solid black")  # Styling
                layout.addWidget(label, row, col)
                row_labels.append(label)
            self.table.append(row_labels)

        # Add label to show falling ball
        self.falling_ball_label = QLabel()
        self.falling_ball_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.falling_ball_label, 9, 0, 1, 2)

        # Add label for displaying current level
        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.level_label, 9, 2, 1, 2)

        # Add label for displaying remaining drops
        self.drops_label = QLabel()
        self.drops_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.drops_label, 10, 3, 1, 3)

        # Add progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 9, 4, 1, 3)

        # Add label for displaying scores
        self.scores_label = QLabel()
        self.scores_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.scores_label, 10, 0, 1, 2)

        # Add buttons to open settings and rules forms
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button, 11, 0, 1, 2)

        rules_button = QPushButton("Rules")
        rules_button.clicked.connect(self.open_rules)
        layout.addWidget(rules_button, 11, 2, 1, 2)
        self.restart_button = QPushButton("Restart")
        layout.addWidget(self.restart_button, 11, 4, 1, 2)

    def init_stylesheets(self):
        dark_mode_stylesheet = """
            QWidget {
                background-color: #333333;
                color: white;
            }
            
            QPushButton:hover {
                background-color: #666666;
            }
        """
        bright_mode_stylesheet = """
            QWidget {
                background-color: #FFFFFF;
                color: black;
            }
            
            QPushButton:hover {
                background-color: #DDDDDD;
            }
        """
        self.dark_mode_stylesheet = dark_mode_stylesheet
        self.bright_mode_stylesheet = bright_mode_stylesheet

    def apply_dark_mode(self):
        self.setStyleSheet(self.dark_mode_stylesheet)

    def apply_bright_mode(self):
        self.setStyleSheet(self.bright_mode_stylesheet)

    def open_settings(self):
        self.settings_window.exec()

    def open_rules(self):
        rules_window = RulesWindow(self)
        rules_window.exec()


class SettingsWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.color_label = QLabel("Color Scheme:")
        layout.addWidget(self.color_label)
        self.color_checkbox = QCheckBox("Dark Mode")
        layout.addWidget(self.color_checkbox)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_button)

    def save_settings(self):
        color_scheme = "dark" if self.color_checkbox.isChecked() else "bright"

        # Apply color scheme
        if color_scheme == "dark":
            self.parent.default_background = "#333333"
            self.apply_dark_mode()
            self.parent.apply_dark_mode()
        else:
            self.parent.default_background = "#FFFFFF"
            self.apply_bright_mode()
            self.parent.apply_bright_mode()

        # Save settings
        self.close()

    def apply_dark_mode(self):
        for row in self.parent.table:
            for label in row:
                label.setStyleSheet("background-color: #333333; color: white; border: 1px solid black")

    def apply_bright_mode(self):
        for row in self.parent.table:
            for label in row:
                label.setStyleSheet("background-color: #FFFFFF; color: black; border: 1px solid black")


class RulesWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Rules")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setMinimumSize(800, 600)

        rules_text = """
        <h1>Chain Factor Game Rules</h1>
        <p>
            Welcome to the Chain Factor! The objective of the game is to clear balls from the game board and earn points.
        </p>
        <h2>How to Play</h2>
        <p>
            1. Balls fall from the top of the game board. Each ball has a numerical value ranging from 1 to 7.
        </p>
        <p>
            2. Click on an empty cell in the column of the game board to drop the falling ball into that column.
        </p>
        <p>
            3. If the numerical value on the ball is the same as the count of adjacent balls horizontally or vertically, the ball will desappear.
        </p>
        <p>
            4. Protected balls cannot be removed as other balls. You need to remove adjacent balls twice to clear a protection.
        </p>
        <p>
            5. When a certain amount of drops happened, you'll go to the next level.
        </p>
        <p>
            6. With each new level, amount of drops needed to proceed decreases.
        </p>
        <p>
            7. When proceeding to a new level, new row of protected balls pushes from below. If there's not enough place, the game is over.
        </p>
        <h2>Scoring</h2>
        <p>
            - Earn points for each ball removed from the game board.
        </p>
        <p>
            - Each new level gives 100 points.
        </p>
        <p>
            - Additional points are awarded for clearing multiple balls in a single move.
        </p>
        <h2>Game Over</h2>
        <p>
            The game ends when you have balls in the top row when trying to go to the next level.
        </p>
        <p>
            Enjoy the game and aim for a high score!
        </p>
        """
        text_browser = QTextBrowser()
        text_browser.setHtml(rules_text)
        layout.addWidget(text_browser)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

