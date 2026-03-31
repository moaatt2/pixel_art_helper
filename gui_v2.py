from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from random import randint

# Setup class for main window
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        # Set window size
        self.setMinimumSize(600, 600)

        # Add button to window
        self.button = QPushButton("Click for new random value: 0")
        self.button.clicked.connect(self.button_pressed)

        self.setCentralWidget(self.button)

    def button_pressed(self):
        self.button.setText(f"Click for new random value: {randint(0, 100)}")


# Testing of directly wiring one widget to another
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


# Testing of overiding mouse event functions
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.label = QLabel()
        self.setCentralWidget(self.label)

    def mouseMovedEvent(self, event):
        self.label.setText("Mouse Moved")

    def mousePressEvent(self, event):
        self.label.setText("Mouse Pressed")

    def mouseReleaseEvent(self, event):
        self.label.setText("Mouse Released")

    def mouseDoubleClickEvent(self, event):
        self.label.setText("Double Clicked")


# Create application instance
app = QApplication([])

# Create an instance of the main window
window = main_window()

# Show the main window instance
window.show()

# Start the application's event loop
app.exec()