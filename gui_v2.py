from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# Setup class for main window
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pixel Art Helper")

        button = QPushButton("Click me")

        self.setCentralWidget(button)


# Create application instance
app = QApplication([])

# Create an instance of the main window
window = main_window()

# Show the main window instance
window.show()

# Start the application's event loop
app.exec()