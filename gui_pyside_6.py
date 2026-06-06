import glob
import json
from PIL import Image
from pprint import pprint

# Enable reload of functions from test
import test
import importlib

from calculate_cost import rings_by_color, convert_to_palette, calculate_cost
from test import resize_image, apply_palette, closest_color_euclidean, closest_color_cie_76, closest_color_cie_00, estimate_size, rotate_image, convert_to_inlay, create_check_image

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QStatusBar, QMessageBox, QFileDialog, QSplitter, QFrame, QScrollArea, QSizePolicy, QSpinBox, QButtonGroup
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QKeySequence, QImage, QIcon
from PySide6.QtCore import Qt, QSize


# Helper function for converting a pil image to a pixmap
def pil_to_pixmap(image: Image.Image) -> QPixmap:
    image = image.convert("RGB")
    data = image.tobytes("raw", "RGB")
    qi = QImage(data, image.size[0], image.size[1], image.size[0]*3, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qi)


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
        self.image = None
        self.image_preview = None

        #######################
        ### Set Window Icon ###
        #######################

        icon = QIcon()
        icon.addFile("assets/images/icon.ico")
        self.setWindowIcon(icon)


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


        # Create Extras menu
        extra_menu = menu.addMenu("&Extras")

        # Add Estimate Size
        estimate_size = QAction("Estimate &Size", self)
        estimate_size.triggered.connect(self.run_estimate_size)
        estimate_size.setShortcut("Ctrl+E+S")
        estimate_size.setStatusTip("Estimate Physical Size of completed inlay")
        extra_menu.addAction(estimate_size)

        # Add Estimate Cost
        estimate_cost = QAction("Estimate &Cost", self)
        estimate_cost.triggered.connect(self.run_estimate_cost)
        estimate_cost.setShortcut("Ctrl+E+C")
        estimate_cost.setStatusTip("Estimate cost of inlay materials")
        extra_menu.addAction(estimate_cost)


        # Create Dev menu
        dev_menu = menu.addMenu("&Dev")

        # Add Reload Inlay Function
        reload_inlay = QAction("&Reload Inlay Function", self)
        reload_inlay.triggered.connect(self.reload_inlay_function)
        reload_inlay.setShortcut("Ctrl+Shift+R")
        reload_inlay.setStatusTip("Reload the inlay generation function")
        dev_menu.addAction(reload_inlay)


        #################
        ### Side Menu ###
        #################

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setContentsMargins(0,0,0,0)
        menu_layout.setSpacing(0)

        palette_accordian = Accordian("Palette Options")
        menu_layout.addWidget(palette_accordian)

        image_accordion = Accordian("Image Options")
        menu_layout.addWidget(image_accordion)

        pattern_accordion = Accordian("Pattern Options")
        menu_layout.addWidget(pattern_accordion)

        # Create Side Menu
        self.side_menu = QFrame()
        self.side_menu.setLayout(menu_layout)
        self.side_menu.setLineWidth(2)
        self.side_menu.setFrameShape(QFrame.Box)


        #######################
        ### Palette Options ###
        #######################

        # Create Widget for image options
        palette_options = QWidget()
        palette_options_layout = QVBoxLayout(palette_options)
        palette_options_layout.setContentsMargins(20,0,0,0)
        palette_options_layout.setSpacing(0)

        # Add palette Selection Accordian
        self.palette_selection_accordion = Accordian("Palette Selection")
        palette_options_layout.addWidget(self.palette_selection_accordion)

        # Apply Palette
        palette_application_accordian = Accordian("Palette Application Methods")
        palette_options_layout.addWidget(palette_application_accordian)

        # Set Palette accordian content
        palette_accordian.set_content(palette_options)


        ###################################
        ### Palette Application Section ###
        ###################################

        # Create Appliation widget
        palette_application = QWidget()
        palette_application_layout = QVBoxLayout(palette_application)
        palette_application_layout.setContentsMargins(20,0,0,0)
        palette_application_layout.setSpacing(0)

        # Create Button Group
        self.palette_application_button_group = QButtonGroup()
        self.palette_application_button_group.setExclusive(True)
        self.palette_application_button_group.buttonClicked.connect(self.redraw_image)

        # No Palette
        np = QPushButton("No Palette")
        np.setCheckable(True)
        np.setChecked(True)
        self.palette_application_button_group.addButton(np)
        palette_application_layout.addWidget(np)

        # Euclidean Distance
        ed = QPushButton("Euclidean Distance")
        ed.setCheckable(True)
        self.palette_application_button_group.addButton(ed)
        palette_application_layout.addWidget(ed)

        # CIE LAB ΔE 1976
        de_76 = QPushButton("Delta E 1976")
        de_76.setCheckable(True)
        self.palette_application_button_group.addButton(de_76)
        palette_application_layout.addWidget(de_76)
    
        # CIE LAB ΔE 2000
        de_00 = QPushButton("Delta E 2000")
        de_00.setCheckable(True)
        self.palette_application_button_group.addButton(de_00)
        palette_application_layout.addWidget(de_00)

        # Add Buttons to accordian
        palette_application_accordian.set_content(palette_application)



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

        # Rotate
        rotate_accordian = Accordian("Rotate Image")
        image_options_layout.addWidget(rotate_accordian)

        # Set Image accordian content
        image_accordion.set_content(image_options)


        ######################
        ### Resize Section ###
        ######################

        # Create Resize Section Widget
        resize_section = QWidget()
        resize_section_layout = QVBoxLayout(resize_section)
        resize_section_layout.setContentsMargins(20,0,0,0)
        resize_section_layout.setSpacing(0)

        # Height Multiplier
        height_mult = QWidget()
        height_mult_layout = QHBoxLayout(height_mult)
        height_mult_layout.setContentsMargins(0,0,0,0)
        height_mult_layout.addWidget(QLabel("Height Multiplier:"))
        self.height_mult_val = QSpinBox()
        self.height_mult_val.setMinimum(1)
        self.height_mult_val.valueChanged.connect(self.redraw_image)
        height_mult_layout.addWidget(self.height_mult_val)
        resize_section_layout.addWidget(height_mult)

        # Width Multiplier
        width_mult = QWidget()
        width_mult_layout = QHBoxLayout(width_mult)
        width_mult_layout.setContentsMargins(0,0,0,0)
        width_mult_layout.addWidget(QLabel("Width Multiplier: "))
        self.width_mult_val = QSpinBox()
        self.width_mult_val.setMinimum(1)
        self.width_mult_val.valueChanged.connect(self.redraw_image)
        width_mult_layout.addWidget(self.width_mult_val)
        resize_section_layout.addWidget(width_mult)

        # Add resize section to accordian
        resize_accordian.set_content(resize_section)


        ######################
        ### Rotate Section ###
        ######################
        
        rotate_section = QWidget()
        rotate_section_layout = QVBoxLayout(rotate_section)
        rotate_section_layout.setContentsMargins(20,0,0,0)
        rotate_section_layout.setSpacing(0)

        # Rotate Right Button
        rotate_right = QPushButton("Rotate 90° Right")
        rotate_right.clicked.connect(lambda: self.rotate_image(clockwise=True))
        rotate_section_layout.addWidget(rotate_right)

        # Rotate Left Button
        rotate_left = QPushButton("Rotate 90° Left")
        rotate_left.clicked.connect(lambda: self.rotate_image(clockwise=False))
        rotate_section_layout.addWidget(rotate_left)

        # Add rotate section to accordian
        rotate_accordian.set_content(rotate_section)


        ###############################
        ### Pattern Options Section ###
        ###############################

        # Create Pattern Options widget
        pattern_options = QWidget()
        pattern_options_layout = QVBoxLayout(pattern_options)
        pattern_options_layout.setContentsMargins(20,0,0,0)
        pattern_options_layout.setSpacing(0)

        # Create Button Group
        self.pattern_button_group = QButtonGroup()
        self.pattern_button_group.setExclusive(True)
        self.pattern_button_group.buttonClicked.connect(self.redraw_image)

        # No Pattern
        no_pattern = QPushButton("No Pattern")
        no_pattern.setCheckable(True)
        no_pattern.setChecked(True)
        self.pattern_button_group.addButton(no_pattern)
        pattern_options_layout.addWidget(no_pattern)

        # Half Stretch
        half_stretch = QPushButton("Half Stretch")
        half_stretch.setCheckable(True)
        self.pattern_button_group.addButton(half_stretch)
        pattern_options_layout.addWidget(half_stretch)

        # Right Way
        right_way = QPushButton("Right Way")
        right_way.setCheckable(True)
        self.pattern_button_group.addButton(right_way)
        pattern_options_layout.addWidget(right_way)

        # Wrong Way
        wrong_way = QPushButton("Wrong Way")
        wrong_way.setCheckable(True)
        self.pattern_button_group.addButton(wrong_way)
        pattern_options_layout.addWidget(wrong_way)

        # Check Image
        check_image = QPushButton("Check Image")
        check_image.setCheckable(True)
        self.pattern_button_group.addButton(check_image)
        pattern_options_layout.addWidget(check_image)

        # Add Pattern Options to accordian
        pattern_accordion.set_content(pattern_options)


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
            self.image = Image.open(file_name)
            self.image = self.image.convert("RGB")
            self.image_preview = QPixmap(file_name)
            self.image_path = file_name
            self.update_image()


    # Placeholder for save file functionality
    def save(self):
        print("Save File")


    # Placeholder for save as functionality
    def save_as(self) -> None:
        print("Save As File")

        if self.image is None:
            return

        # Create File Dialog
        file_dialog = QFileDialog(self)

        # File Dialog Settings
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("BMP (*.bmp *.dib)")
 
        # Execute File Dialog and get selected file
        if file_dialog.exec():
            file_name = file_dialog.selectedFiles()[0]
            print(f"Selected file: {file_name}")
            self.image.save(file_name)


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

        self.palette_selection_accordion.set_content(palette_options)


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
        if self.image_preview is not None:
            size = self.image_container.size()

            if size.width() > 0 and size.height() > 0:
                self.image_container.setPixmap(
                    self.image_preview.scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )


    # Estimate size of completed inlay
    def run_estimate_size(self) -> None:

        # Exit early if there is no image
        if self.image is None:
            return

        # Estimate size
        size = estimate_size(self.image, 16, "SWG", 0.25, "inches")

        # Draft the message
        message = f'If made with 16 SWG rings with an ID of 0.25" with one pixel per ring the expected size is {size[0]}" x {size[1]}"'

        # The the user the message
        QMessageBox.information(self, "Size Estimate", message)


    # Estimate cost of completed inlay
    def run_estimate_cost(self) -> None:

        # Exit early if no image exists
        if self.image is None:
            return

        # Create palette
        palette = dict()
        for palette_name in self.palettes.keys():
            if not self.palettes[palette_name]["enabled"]:
                continue
            for color in self.palettes[palette_name]["colors"].keys():
                if not self.palettes[palette_name]["colors"][color]["enabled"]:
                    continue
                palette[f"{palette_name}_{color}"] = self.palettes[palette_name]["colors"][color]["hexstring"]

        # Warn user if palette is empty
        if len(palette) < 1:
            QMessageBox.critical(self, "Empty Palette", "Your palette doesn't have any colors, please select at least one to continue.")
            return None
        
        # Get a count of pixels by color
        color_count = rings_by_color(self.image)

        # Convert to palette counts
        rings_by_palette = convert_to_palette(color_count, palette)

        # Get total cost and breakdown
        cost, breakdown = calculate_cost(rings_by_palette)

        # Intialize accumulators
        t_bags = 0
        t_rings = 0

        # Generate message
        message = f"The estimated total cost for the project is: ${cost:.2f}\nSpent on the following resources:\n\n"
        for key, v in breakdown.items():
            clean_name = key.replace("_", " ").title()
            message += f"\t* {clean_name}:\n"
            message += f"\t\t* Rings: {v["rings"]}\n"
            message += f"\t\t* Bags:  {v["bags"]}\n"
            message += f"\t\t* Extra Rings: {v["bags"]*300 - v["rings"]}\n"

            t_rings += v["rings"]
            t_bags  += v["bags"]

        # Add total
        message += f"\t* Total:\n"
        message += f"\t\t* Rings: {t_rings}\n"
        message += f"\t\t* Bags:  {t_bags}\n"
        message += f"\t\t* Extra Rings: {t_bags*300 - t_rings}\n"

        # Show user message
        QMessageBox.information(self, "Cost Estimate", message)
        print(message)


    # Function to rotate image
    def rotate_image(self, clockwise):

        # Ensure that image exists before trying to rotate
        if self.image is None:
            return

        # Rotate image
        self.image = rotate_image(self.image, 90, clockwise)

        # Update the image after changing it
        self.redraw_image()


    # Redraw the image preview based on selected options
    def redraw_image(self):

        # Confirm image exists
        if self.image is None:
            QMessageBox.warning(self, "No Image", "Please load an image before modifing one.")
            return
        
        # Create a temp copy of the image
        img_copy = self.image.copy()


        #####################
        ### Apply Palette ###
        #####################

        # Find selected option
        palette_option = self.palette_application_button_group.checkedButton().text()
        print(f"Palette Option: {palette_option}")

        # Skip logic if palette option is no palette
        if palette_option != "No Palette":

            # Get Palette
            palette = dict()
            for palette_name in self.palettes.keys():
                if self.palettes[palette_name]["enabled"]:
                    for color in self.palettes[palette_name]["colors"].keys():
                        if self.palettes[palette_name]["colors"][color]["enabled"]:
                            palette[f"{palette_name}_{color}"] = self.palettes[palette_name]["colors"][color]["rgb"]

            # Warn user if palette is empty - but only skip palette application
            if len(palette) < 1:
                QMessageBox.warning(self, "Empty Palette", "Your palette doesn't have any colors, please select at least one or apply 'No Palette'.")

            # Apply palettes if a valid option is selected
            elif palette_option == "Euclidean Distance":
                img_copy = apply_palette(palette, img_copy, closest_color_euclidean, "rgb")
            elif palette_option == "Delta E 1976":
                img_copy = apply_palette(palette, img_copy, closest_color_cie_76, "cielab")
            elif palette_option == "Delta E 2000":
                img_copy = apply_palette(palette, img_copy, closest_color_cie_00, "cielab")


        ####################
        ### Resize Image ###
        ####################

        # Get height
        h_mult = self.height_mult_val.value()

        # Get width
        w_mult = self.width_mult_val.value()

        # Modify Image
        img_copy = resize_image(img_copy, w_mult, h_mult)
        print(f"Resizing to: {w_mult} x {h_mult}")


        #############################
        ### Apply Pattern Options ###
        #############################

        # Find selected option
        pattern_option = self.pattern_button_group.checkedButton().text()
        print(f"Pattern Option: {pattern_option}")

        # Revert back to no chainmail pattern if selected
        if pattern_option == "No Pattern":
            pass

        # Apply half stretch pattern
        elif pattern_option == "Half Stretch":
            img_copy = convert_to_inlay(img_copy, "Half Stretch")

        # Apply right way pattern
        elif pattern_option == "Right Way":
            img_copy = convert_to_inlay(img_copy, "Right Way")
 
        # TODO - Implement function to create wrong way pattern
        elif pattern_option == "Wrong Way":
            img_copy = convert_to_inlay(img_copy, "Wrong Way")

        # Apply check image pattern
        elif pattern_option == "Check Image":
            img_copy = create_check_image(img_copy)

        # Warning if unknown pattern is somehow selected
        else:
            QMessageBox.critical(self, "Unknown Pattern", f"An unknown pattern was selected: {pattern_option}. This should never happen, please report this bug to the developer.")


        ######################
        ### Update Preview ###
        ######################

        # Copy the drawn image to the preview
        self.image_preview = pil_to_pixmap(img_copy)

        # Delete the temp image copy
        del img_copy

        # Update the preview image
        self.update_image()
    

    # Reload the inlay generation function and redraw the image
    def reload_inlay_function(self):

        print("Reloading Inlay Function")

        # Ensure that I am using the global convert_to_inlay function
        global convert_to_inlay

        # Reload the module and replace the function with the update version
        importlib.reload(test)
        convert_to_inlay = test.convert_to_inlay

        # Redraw the image
        self.redraw_image()
 

# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
