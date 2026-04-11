from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QMenu, QGridLayout, QStackedLayout, QTabWidget, QStatusBar, QToolBar, QDialog, QDialogButtonBox, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize


# Helper class to display a solid color window
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        pallette = self.palette()
        pallette.setColor(QPalette.Window, QColor(color))
        self.setPalette(pallette)


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


        # Create Side Menu
        self.side_menu = QWidget(self)

        # Initialize Image Container
        self.image_container = QLabel("Press Ctrl+O to open an image", self)
        self.image_container.setAlignment(Qt.AlignCenter)

        # Create Main Layout
        main_layout = QHBoxLayout()

        # Add side menu and make it take 1/4 of the space
        main_layout.addWidget(self.side_menu, 1)

        # Add image container and make it take 3/4 of the space
        main_layout.addWidget(self.image_container, 3)


        # Add Widget with layout to window
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(main_layout)

        # Set Status Bar
        self.setStatusBar(QStatusBar(self))
    
    
    # Placeholder for open file functionality
    def open(self):
        print("Open File")

        # Create File Dialog
        file_dialog = QFileDialog(self)

        # File Dialog Settings
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
 
        # Execute File Dialog and get selected file
        if file_dialog.exec():
            file_name = file_dialog.selectedFiles()[0]
            print(f"Selected file: {file_name}")

            # Load the selected image into the image container
            self.image = QPixmap(file_name)
            self.image_container.setPixmap(self.image.scaled(self.image_container.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


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
