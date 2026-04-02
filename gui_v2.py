from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QCheckBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
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
        if event.button() == Qt.LeftButton:
            self.label.setText("Left Button Released")
        elif event.button() == Qt.RightButton:
            self.label.setText("Right Button Released")
        elif event.button() == Qt.MiddleButton:
            self.label.setText("Middle Button Released")
        else:
            self.label.setText("Other Button Released")

    def mouseDoubleClickEvent(self, event):
        self.label.setText("Double Clicked")


# Test Displaying an image
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.label = QLabel()
        self.label.setPixmap(QPixmap("test_images/source_images/exdeath.bmp"))
        self.setCentralWidget(self.label)


# Test Checkboxes
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.checkbox1 = QCheckBox("Option 1")
        self.checkbox2 = QCheckBox("Option 2")
        self.checkbox3 = QCheckBox("Option 3")

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)

        self.checkbox1.setCheckState(Qt.CheckState.PartiallyChecked)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


# Create application instance
app = QApplication([])

# Create an instance of the main window
window = main_window()

# Show the main window instance
window.show()

# Start the application's event loop
app.exec()