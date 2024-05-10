from PyQt6.QtWidgets import QGridLayout, QWidget, QMainWindow, QLabel, QProgressBar
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
        self.table = None
        self.falling_ball_label = None
        self.level_label = None
        self.drops_label = None
        self.progress_bar = None
        self.scores_label = None
        self.setWindowTitle("PyQt6 Ball Game")
        self.setMinimumSize(425, 485)  # Set minimum size
        self.setMaximumSize(425, 485)  # Set maximum size
        self.init_ui()

    def init_ui(self):
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
                label.setStyleSheet("background-color: #FFFFFF; border: 1px solid black")  # Styling
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
