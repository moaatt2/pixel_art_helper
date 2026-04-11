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


# Helper accordian widget
class Accordian(QWidget):
    def __init__(self, title):
        super().__init__()

        # Create color section
        self.content_section = QWidget()
        self.content_section.setVisible(False)

        # Add button
        button = QPushButton(title)
        button.clicked.connect(lambda: self.toggle_section(self.content_section))

        # Create layout and add content
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.content_section)

        # Apply layout to self
        self.setLayout(layout)


    def toggle_section(self, section:QWidget):
        section.setVisible(not section.isVisible())


    def set_content(self, content:QWidget):
        layout = QVBoxLayout()
        layout.addWidget(content)
        self.content_section.setLayout(layout)


# Main Window Class
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()                      # Initialize super class
        self.setWindowTitle("Pixel Art Helper") # Set Window title
        self.setMinimumSize(600, 600)           # Set Window Size


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


        #################
        ### Side Menu ###
        #################

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignTop)

        palette_accordion = Accordian("Palettes")
        menu_layout.addWidget(palette_accordion)
        palette_accordion.set_content(QLabel("Palette content goes here"))

        palette_accordion = Accordian("Image Options")
        menu_layout.addWidget(palette_accordion)
        palette_accordion.set_content(QLabel("Image options go here"))

        palette_accordion = Accordian("Pattern Options")
        menu_layout.addWidget(palette_accordion)
        palette_accordion.set_content(QLabel("Pattern options go here"))


        # Create Side Menu
        self.side_menu = QWidget(self)
        self.side_menu.setLayout(menu_layout)




        #############################
        ### Setup Image Container ###
        #############################

        self.image_container = QLabel("Press Ctrl+O to open an image", self)
        self.image_container.setAlignment(Qt.AlignCenter)


        ##########################
        ### Create Main Layout ###
        ##########################

        main_layout = QHBoxLayout()                    # Initialize Layout
        main_layout.addWidget(self.side_menu, 1)       # Add side menu and make it take 1/4 of the space
        main_layout.addWidget(self.image_container, 3) # Add image container and make it take 3/4 of the space

        # Add Widget with layout to window
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(main_layout)

        # Set Status Bar
        self.setStatusBar(QStatusBar(self))


    # On open button, create file dialog, load selected image, display image in container
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
            self.image_path = file_name
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
    

    # Custom Resize Event to rescale image when window is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "image"):
            self.image_container.setPixmap(self.image.scaled(self.image_container.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
