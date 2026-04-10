from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QMenu, QGridLayout, QStackedLayout, QTabWidget, QStatusBar, QToolBar, QDialog, QDialogButtonBox, QMessageBox
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize

# Main Window Class
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()  

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        # Set Window Size
        self.setMinimumSize(600, 600)


# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
