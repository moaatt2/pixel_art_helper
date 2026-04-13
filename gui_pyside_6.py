import glob
import json
from pprint import pprint

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QStatusBar, QMessageBox, QFileDialog, QSplitter, QFrame, QScrollArea, QSizePolicy
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QKeySequence
from PySide6.QtCore import Qt, QSize


# Helper class to display a solid color window
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        pallette = self.palette()
        pallette.setColor(QPalette.Window, QColor(color))
        self.setPalette(pallette)


# Custom Label class overwriting min size hint so the splitter can make the image smaller
class ImageLabel(QLabel):
    def minimumSizeHint(self):
        return QSize(0,0)


# Helper accordian widget
class Accordian(QWidget):
    def __init__(self, title):
        super().__init__()

        # Create color section
        self.content_section = QWidget()
        self.content_section.setVisible(False)

        # Set a fixed layout to add widgets to the content section
        self.content_layout = QVBoxLayout(self.content_section)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)

        # Add button
        button = QPushButton(title)
        button.clicked.connect(self.toggle_section)

        # Create layout and add content
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.content_section)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Apply layout to self
        self.setLayout(layout)


    def toggle_section(self):
        self.content_section.setVisible(not self.content_section.isVisible())


    def set_content(self, content:QWidget):
        while self.content_layout.count() > 0:
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            
        self.content_layout.addWidget(content)


# Main Window Class
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()                      # Initialize super class
        self.setWindowTitle("Pixel Art Helper") # Set Window title
        self.setMinimumSize(900, 600)           # Set Window Size

        # Intialize instance variables
        self.palettes = dict()


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
        reload_action = QAction("&Reload Palettes", self)
        reload_action.triggered.connect(self.load_palettes)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.setStatusTip("Reload the color palettes")
        file_menu.addAction(reload_action)

        # Add Exit action
        file_menu.addSeparator()
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.exit)
        exit_action.setShortcut(QKeySequence("Ctrl+W"))
        exit_action.setStatusTip("Exit the application")
        file_menu.addAction(exit_action)

        # Add Exit action
        # TODO: Remove from production
        file_menu.addSeparator()
        show_state = QAction("&Print Palette State", self)
        show_state.triggered.connect(self.print_palette_state)
        show_state.setShortcut(QKeySequence("Ctrl+P"))
        show_state.setStatusTip("Show the internal palette state")
        file_menu.addAction(show_state)


        #################
        ### Side Menu ###
        #################

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setContentsMargins(0,0,0,0)
        menu_layout.setSpacing(0)

        self.palette_accordion = Accordian("Palette Selection")
        menu_layout.addWidget(self.palette_accordion)
        self.palette_accordion.set_content(QLabel("Palette content goes here"))

        image_accordion = Accordian("Image Options")
        menu_layout.addWidget(image_accordion)
        # image_accordion.set_content(QLabel("Image options go here"))

        self.pattern_accordion = Accordian("Pattern Options")
        menu_layout.addWidget(self.pattern_accordion)
        self.pattern_accordion.set_content(QLabel("Pattern options go here"))

        # Create Side Menu
        self.side_menu = QFrame()
        self.side_menu.setLayout(menu_layout)
        self.side_menu.setLineWidth(2)
        self.side_menu.setFrameShape(QFrame.Box)


        #####################
        ### Image Options ###
        #####################

        # Create widget for image options
        image_options = QWidget()
        image_options_layout = QVBoxLayout(image_options)
        image_options_layout.setContentsMargins(20,0,0,0)
        image_options_layout.setSpacing(0)

        # Resize
        resize_accordian = Accordian("Resize Image")
        image_options_layout.addWidget(resize_accordian)
        resize_accordian.set_content(QLabel("Resize options go here"))

        # Rotate
        rotate_accordian = Accordian("Rotate Image")
        image_options_layout.addWidget(rotate_accordian)
        rotate_accordian.set_content(QLabel("Rotate options go here"))

        # Apply Palette
        palette_application_accordian = Accordian("Apply Palette to Image")
        image_options_layout.addWidget(palette_application_accordian)
        palette_application_accordian.set_content(QLabel("Palette Application options go here"))

        # Set Image accordian content
        image_accordion.set_content(image_options)


        ######################
        ### Resize Section ###
        ######################

        # TODO


        ######################
        ### Rotate Section ###
        ######################

        # TODO


        ###################################
        ### Palette Application Section ###
        ###################################

        # Create Appliation widget
        palette_application = QWidget()
        palette_application_layout = QVBoxLayout(palette_application)
        palette_application_layout.setContentsMargins(20,0,0,0)
        palette_application_layout.setSpacing(0)

        # Euclidian Distance
        ed = QPushButton("Apply Palette Using Euclidean Distance")
        palette_application_layout.addWidget(ed)

        # CIE LAB ΔE 1976
        de_76 = QPushButton("Apply Palette Using ΔE 1976")
        palette_application_layout.addWidget(de_76)

        # CIE LAB ΔE 2000
        de_00 = QPushButton("Apply Palette Using ΔE 2000")
        palette_application_layout.addWidget(de_00)

        # Add Buttons to accordian
        palette_application_accordian.set_content(palette_application)


        #############################
        ### Setup Image Container ###
        #############################

        # Create Frame for image
        self.image_frame = QFrame()
        self.image_frame.setLineWidth(2)
        self.image_frame.setFrameShape(QFrame.Box)

        # Create Layout for image
        image_layout = QVBoxLayout(self.image_frame)
        image_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        self.image_container = ImageLabel("Press Ctrl+O to open an image", self.image_frame)
        self.image_container.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_container)


        ##########################
        ### Create Main Layout ###
        ##########################

        # Create Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.side_menu)
        splitter.addWidget(self.image_frame)

        # Set an inital 1:3 ratio
        splitter.setSizes([200,600])

        # Set splitter stretch factors to maintain 1:3 ratio
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,3)

        # When the splitter moves update the image size
        splitter.splitterMoved.connect(self.update_image)

        # Set splitter as central widget
        self.setCentralWidget(splitter)

        # Instantiate Data
        self.load_palettes()

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
            self.update_image()


    # Placeholder for save file functionality
    def save(self):
        print("Save File")


    # Placeholder for save as functionality
    def save_as(self):
        print("Save As File")


    # Placeholder for reload palettes functionality
    def load_palettes(self):
        print("Reload Palettes")
    
        # Load data model
        for path in glob.glob("palettes/*.json"):
            palette_name = path.split("/")[-1].split("\\")[-1].split(".")[0]

            # Load palette files
            with open(path, "r") as f:
                raw = json.load(f)
            
            # Create dict in palettes dict for current palette
            self.palettes[palette_name] = {
                "enabled": False,
                "colors": dict(),
            }

            # Convert hex color codes to RGB tuples and store in palette dict
            for k, v in raw.items():
                r = int(v[0:2], 16)
                g = int(v[2:4], 16)
                b = int(v[4:6], 16)
                self.palettes[palette_name]["colors"][k] = {
                    "rgb": (r, g, b),
                    "hexstring": v,
                    "enabled": True,
                }
        
        
        # Alert User if no palettes were found
        if len(self.palettes) == 0:
            QMessageBox.warning(self, "No Palettes Found", "No palette files were found in the palettes directory. Please add some .json palette files and try again.")


        # Create container for all palette options sections
        palette_options = QWidget()
        palette_options_layout = QVBoxLayout(palette_options)
        palette_options_layout.setContentsMargins(20,0,0,0)
        palette_options_layout.setSpacing(0)

        # Create Palette Widget for each palette
        for palette_name in self.palettes.keys():
            name_clean = " ".join(palette_name.split("_")).title()


            ############
            ### Body ###
            ############

            # Create color section widget & Layout
            color_section = QWidget()
            color_section_layout = QVBoxLayout(color_section)
            color_section_layout.setContentsMargins(3,3,0,0) # 30
            color_section_layout.setSpacing(3)

            # Create list of checkboxes affected by parent
            color_checkboxes = list()

            # Itterate over colors
            for color_name in self.palettes[palette_name]["colors"].keys():
                color_name_clean = " ".join(color_name.split("_")).title()
                color_hex = self.palettes[palette_name]["colors"][color_name]["hexstring"]

                # Instantiate Color Row
                color_row = QWidget()
                color_layout = QHBoxLayout(color_row)
                color_layout.setContentsMargins(0,0,0,0)
                color_layout.setSpacing(0)

                # Create Color Swatch
                swatch = QWidget()
                swatch.setFixedSize(25,25)
                swatch.setStyleSheet(f"background-color: #{color_hex}; border: none; border-radius: 3px;")
                color_layout.addWidget(swatch)

                # Create Color Checkbox
                checkbox = QCheckBox(color_name_clean)
                checkbox.setChecked(True)
                checkbox.setDisabled(True)
                checkbox.toggled.connect(lambda checked, c=checkbox, p=palette_name, cn=color_name: self.toggle_color_checkbox(c, p, cn))
                color_layout.addWidget(checkbox)

                # Add to Color Section
                color_section_layout.addWidget(color_row)
                color_checkboxes.append(checkbox)
            
            # Create Scroll area widget
            color_scroll = QScrollArea()
            color_scroll.setWidget(color_section)

            # Scroll area settings
            color_scroll.setFixedHeight(120)
            color_scroll.setWidgetResizable(True)
            color_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            color_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            color_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            # Set Horizontal offset of scroll area and header
            scroll_container = QWidget()
            scroll_layout = QVBoxLayout(scroll_container)
            scroll_layout.setContentsMargins(30,0,0,0)
            scroll_layout.setSpacing(0)
            scroll_layout.addWidget(color_scroll)

            # Set default visibility to false
            scroll_container.setVisible(False)


            ##############
            ### Header ###
            ##############

            # Create header widget and its layout
            header =  QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0,0,0,0)
            header_layout.setSpacing(0)

            # Setup color section collapse/expand button
            arrow = QPushButton("▸")
            arrow.setFixedWidth(30)
            arrow.clicked.connect(lambda checked, a=arrow, s=scroll_container: self.palette_button_clicked(a, s))

            # Setup Checkbox
            checkbox = QCheckBox(name_clean)
            checkbox.toggled.connect(lambda checked, c=checkbox, p=palette_name, cc=color_checkboxes: self.toggle_palette_checkbox(c, p, cc))
            header_layout.addWidget(arrow)
            header_layout.addWidget(checkbox)


            ##########################
            ### Join Header & Body ###
            ##########################

            palette_widget = QWidget()
            palette_layout = QVBoxLayout(palette_widget)
            palette_layout.setContentsMargins(0,0,0,0)
            palette_layout.setSpacing(0)

            palette_layout.addWidget(header)
            palette_layout.addWidget(scroll_container)

            palette_options_layout.addWidget(palette_widget)

        self.palette_accordion.set_content(palette_options)


    # Show/hide Given container and change button text when it is clicked
    def palette_button_clicked(self, button, container):
        print("Palette Visibility Toggle Button Clicked")

        # Change button text
        if button.text() == "▸":
            button.setText("▾")
        else:
            button.setText("▸")
        
        # Change color section visibility
        container.setVisible(not container.isVisible())


    # Toggle Palette checkbox
    def toggle_palette_checkbox(self, checkbox: QCheckBox, palette_name: str, children: list[QCheckBox]) -> None:
        # Update palettes dict
        self.palettes[palette_name]["enabled"] = checkbox.isChecked()

        # Enable/Disable Children
        for child in children:
            child.setDisabled(not checkbox.isChecked())


    # Toggle Color Checkbox
    def toggle_color_checkbox(self, checkbox: QCheckBox, palette_name: str, color_name: str) -> None:
        self.palettes[palette_name]["colors"][color_name]["enabled"] = checkbox.isChecked()


    # Custom Resize Event to rescale image when window is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()


    # TODO: Remove from production
    # Testing Function to print palette state
    def print_palette_state(self):
        pprint(self.palettes)


    # Function to safely quit the application
    def exit(self):
        # TODO: Check for unsaved work and ask if user is sure
        QApplication.instance().quit()


    # Resize image preview based on available space
    def update_image(self):
        if hasattr(self, "image"):
            size = self.image_container.size()

            if size.width() > 0 and size.height() > 0:
                self.image_container.setPixmap(
                    self.image.scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )


# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
