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


        ################
        ### Menu Bar ###
        ################

        # Create Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        # Create open button
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.setStatusTip("Open a file")
        file_menu.addAction(open_action)

        # Create save button
        save_action = QAction("&Save", self)
        save_action.triggered.connect(self.save)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.setStatusTip("Save the current file")
        file_menu.addAction(save_action)

        # Create save as button
        save_as_action = QAction("Save &As", self)
        save_as_action.triggered.connect(self.save_as)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.setStatusTip("Save the current file with a new name")
        file_menu.addAction(save_as_action)

        # Add a separator between file actions and palette actions
        file_menu.addSeparator()

        # Create reload button
        reload_action = QAction("&Load Palettes", self)
        reload_action.triggered.connect(self.load_palettes)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.setStatusTip("Reload the color palettes")
        file_menu.addAction(reload_action)


        # Set Status Bar
        self.setStatusBar(QStatusBar(self))
    
    
    # Placeholder for open file functionality
    def open(self):
        print("Open File")


    # Placeholder for save file functionality
    def save(self):
        print("Save File")


    # Placeholder for save as functionality
    def save_as(self):
        print("Save As File")


    # Placeholder for reload palettes functionality
    def load_palettes(self):
        print("Reload Palettes")


# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
