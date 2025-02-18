#------------------------------------------------------
# BD_Engineer
# Advanced Backdrop Tool for Nuke
# created by Eric Prochnow
version = '1.0'
releaseDate = 'Feb 16 2025'

#-----------------------------------------------------    

from PySide2 import QtCore, QtGui, QtWidgets
import nuke
import random
import os
import importlib
import re


# ----------------------------------------------
# # 1. Settings
# ----------------------------------------------


# Define the path to your icons folder

# Option 1: Use Nukes default icons
nukePATH = os.path.dirname(nuke.EXE_PATH)
icons_path = f"{nukePATH}/plugins/icons"

# Option 2: Use your own icons
# icons_path = r"C:\link\to\your\icon\folder\goes\here"


# Define Button size (change if needed)
button_width = 50
button_height = 15


# ----------------------------------------------
# 2. Base
# ----------------------------------------------


# import buttons_config.py - if not found, create the file
try:
    import buttons_config
except:
    config_path = os.path.join(os.path.dirname(__file__), "buttons_config.py")
    try:
        # Define the default BUTTONS configuration
        buttons_config_base = "BUTTONS = " + repr([
            {
                'label': '',
                'color': '',
                'tooltip': '',
                'icon': '',
                'text': ''
            }
        ])

    except:
        pass

    # Write to the config file
    with open(config_path, "w") as f:
        f.write(buttons_config_base)

    # Reload the module so changes take effect
    import buttons_config
    importlib.reload(buttons_config)


# activate available_icons variable
available_icons = []


# ----------------------------------------------
# 3. Tool UI
# ----------------------------------------------


# Main UI Class

class BD_Engineer(QtWidgets.QWidget):
    
    def __init__(self):
        super(BD_Engineer, self).__init__()


        # --- UI Window Settings ---
        self.setWindowTitle("BD_Engineer")
        self.setGeometry(100, 100, 100, 100)
        # Keep window always on top
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)



        # --- Main Layout  ---
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)  # Remove all margins
        self.mainLayout.setSpacing(5)  # Increase space between elements
        



        # --- Main Title  ---
        self.sectionTitle = QtWidgets.QLabel("BD Engineer")
        self.sectionTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.sectionTitle.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.mainLayout.addWidget(self.sectionTitle)




        # --- Subtitle 1 ("Create Backdrop") ---
        self.sectionSubtitle_bd = QtWidgets.QLabel("Create Backdrop")
        self.sectionSubtitle_bd.setAlignment(QtCore.Qt.AlignCenter)
        self.sectionSubtitle_bd.setStyleSheet("font-size: 8px")
        self.mainLayout.addWidget(self.sectionSubtitle_bd)




        # --- Backdrop Button Section ---
        self.bd_button_width = button_width
        self.bd_button_height = button_height
        self.bd_button_spacing = 8
        
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.buttonLayout.setSpacing(self.bd_button_spacing)  
        self.buttonLayout.setAlignment(QtCore.Qt.AlignCenter)  #

        # Add buttons based on config
        for btn in buttons_config.BUTTONS:
            button = QtWidgets.QPushButton(btn["label"])

            button.setStyleSheet(
            f"""
            QPushButton{{background-color: {btn['color']}; color: white; font-size: 8px}}"
            QToolTip {{background: transparent; color: white; border: none}}
            """)

            button.setToolTip(btn["tooltip"])
            button.setFixedSize(self.bd_button_width, self.bd_button_height)
            button.clicked.connect(lambda checked=False, b=btn: self.create_backdrop(b))
            self.buttonLayout.addWidget(button)

        # Create a container widget to center the button layout
        self.buttonContainer = QtWidgets.QWidget()
        self.buttonContainer.setLayout(self.buttonLayout)
        self.buttonContainer.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.mainLayout.addWidget(self.buttonContainer, alignment=QtCore.Qt.AlignCenter)




        # --- Add Seperator Line ---
        self.separator = QtWidgets.QFrame()
        self.separator.setFrameShape(QtWidgets.QFrame.HLine) 
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)  
        self.separator.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.addWidget(self.separator)

        # Add space before Modify Backdrop title
        self.mainLayout.addSpacing(10)




        # --- Subtitle 2 ("Modify Backdrop" ---
        self.sectionSubtitle_modify = QtWidgets.QLabel("Modify Backdrop")
        self.sectionSubtitle_modify.setAlignment(QtCore.Qt.AlignCenter)
        self.sectionSubtitle_modify.setStyleSheet("font-size: 8px")
        self.mainLayout.addWidget(self.sectionSubtitle_modify)
        



        # --- Modify Button Section ---
        self.modifyButtonLayout = QtWidgets.QGridLayout()
        self.modifyButtonLayout.setSpacing(5)  # Spacing between buttons
        self.modifyButtonLayout.setContentsMargins(0, 10, 0, 10)

        # Define button labels and function placeholders
        button_data = [
            ("+", self.up, "Scale up all selected backdrops."),
            ("-", self.down, "Scale down all selected backdrops."),
            ("Label Size",  self.title_size,"Update the label size of all selected backdrops."),
            ("Label Text", self.title,"Update the label text of all selected backdrops."),
            ("Appearance", self.toggleBorder,"Switch the appearance ofall selected backdrops.\nBorder or Fill is possible."),
            ("Color Rand", self.randomizeColor,"Use a randomized color on all selected backdrops."),
        ]

        # Create Modify buttons 
        self.modifyButtons = []
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)] 

        for pos, (label, function, tooltip) in zip(positions, button_data):
            button = QtWidgets.QPushButton(label)
            button.setFixedSize(self.bd_button_width + 5, self.bd_button_height)
            button.setToolTip(tooltip)
            button.clicked.connect(function)
            self.modifyButtonLayout.addWidget(button, *pos)
            self.modifyButtons.append(button)

        # Create a container for modify buttons
        self.modifyButtonContainer = QtWidgets.QWidget()
        self.modifyButtonContainer.setLayout(self.modifyButtonLayout)
        self.modifyButtonContainer.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # Add to main layout
        self.mainLayout.addWidget(self.modifyButtonContainer, alignment=QtCore.Qt.AlignCenter)

        # Add space after modify buttons
        self.mainLayout.addSpacing(10)




        # --- Bottom Layout Section ---

        # Credit text
        self.website = "<a href='https://ericprochnow.com' style='text-decoration:none; color:#ffffff;'>"
        self.creditLabel = QtWidgets.QLabel(f"BD Engineer V01 <br><br> © 2025 by {self.website}Eric Prochnow</a><br>")

        # Ensure rich text format is used
        self.creditLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.creditLabel.setOpenExternalLinks(True)
        self.creditLabel.setStyleSheet("QLabel {font-size:6px; line-height: 12px;}")
        self.creditLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        # Settings Button Layout
        self.settingsButtonLayout = QtWidgets.QVBoxLayout()
        self.settingsButtonLayout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Settings Button
        icon_path = find_nuke_icon("SettingsButton.png")

        self.settingsButton = QtWidgets.QPushButton()
        self.settingsButton.setFixedSize(12,12)
        self.settingsButton.setIcon(QtGui.QIcon(icon_path))
        self.settingsButton.setIconSize(QtCore.QSize( 10,  10))
        self.settingsButton.clicked.connect(self.open_settings)
        self.settingsButtonLayout.addWidget(self.settingsButton)

        # Wrap the settings layout in a Container Layout
        self.settingsContainer = QtWidgets.QWidget()
        self.settingsContainer.setLayout(self.settingsButtonLayout)

        # Add Credit Text and SettingsButtonContainer to MainLayout
        self.mainLayout.addWidget(self.settingsContainer)
        self.mainLayout.addWidget(self.creditLabel)

        # Adjust Window Height Based on Last Layout
        self.adjustSize()  # Let Qt calculate the natural size
        self.setFixedHeight(self.height())  # Lock the vertical size

        # Optionally, allow horizontal resizing
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    def create_backdrop(self, btn_settings):
        """Creates a backdrop using the settings from the config file"""
        createBackdrop(
            icon=btn_settings["icon"],
            text=btn_settings["text"],
            color=btn_settings["color"]
        )

    def title(self):
        updateTitle(nuke.selectedNodes())

    def title_size(self):
        updateTextsize(nuke.selectedNodes())

    def up(self):
        scaleUp(nuke.selectedNodes())

    def down(self):
        scaleDown(nuke.selectedNodes())

    def toggleBorder(self):
        toggleFillBorder(nuke.selectedNodes())

    def randomizeColor(self):
        randomizeBackdropColor(nuke.selectedNodes())

    def open_settings(self):
        open_config_editor()

# Settings Window UI Class

class ConfigEditor(QtWidgets.QDialog):

    def __init__(self, config_path, available_icons, icons_path, parent=None):
        super(ConfigEditor, self).__init__(parent)
        self.config_path = config_path
        self.setWindowTitle("Edit Backdrop Buttons")

        # Get available icons from the icons directory
        self.icons_path = icons_path
        self.available_icons = available_icons

        if os.path.exists(self.icons_path):
             self.available_icons = [f for f in os.listdir(self.icons_path) if f.endswith(('.png'))]
        else:
            self.available_icons = []

        self.available_icons.sort() 
        self.available_icons.insert(0, "")

        # Define Size for the icon selection section
        self.ICON_SIZE = 24  # Set the desired icon size
        self.icon_combobox_width = self.ICON_SIZE + 25 
        self.icon_combobox_height = self.ICON_SIZE + 5

        # Create a table to display each button's properties
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Button Text", "Color", "Tooltip", "Icon", "Backdrop Label Text"])


        # Disable resizing of columns and rows
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        # Prevent stretching of last section to keep layout fixed
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setStretchLastSection(False)
                
        
        # Load current configuration from config.py
        self.load_data()
        
        # Buttons for adding, removing, saving, and canceling
        addBtn = QtWidgets.QPushButton("Add")
        removeBtn = QtWidgets.QPushButton("Remove")
        saveBtn = QtWidgets.QPushButton("Save")
        cancelBtn = QtWidgets.QPushButton("Cancel")

        addBtn.clicked.connect(self.add_row)
        removeBtn.clicked.connect(self.remove_selected_row)
        saveBtn.clicked.connect(self.save)
        cancelBtn.clicked.connect(self.reject)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(addBtn)
        btn_layout.addWidget(removeBtn)
        btn_layout.addStretch()
        btn_layout.addWidget(saveBtn)
        btn_layout.addWidget(cancelBtn)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Window size based on table
        self.adjust_window_size()
        
    def load_data(self):
        buttons = buttons_config.BUTTONS
        self.table.setRowCount(len(buttons))
        
        for row, button in enumerate(buttons):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(button.get("label", "")))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(button.get("color", "")))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(button.get("tooltip", "")))

            # Extract filename from stored full path (e.g., ":icons/icon.png" → "icon.png")
            full_icon_path = button.get("icon", "")
            icon_filename = full_icon_path.split("/")[-1] if full_icon_path else ""

            # Create the QComboBox with fixed size
            icon_dropdown = QtWidgets.QComboBox()
            icon_dropdown.setIconSize(QtCore.QSize( self.ICON_SIZE,  self.ICON_SIZE))  # Set icon size
            icon_dropdown.setFixedSize( self.icon_combobox_width,  self.icon_combobox_height)  # Adjust dropdown size

            # Populate dropdown with icons
            for icon_name in self.available_icons:
                icon_path = f"{self.icons_path}/{icon_name}"
                icon = QtGui.QIcon(icon_path)
                icon_dropdown.addItem(icon, "", icon_name)

            # Find the correct icon and select it
            index = icon_dropdown.findData(icon_filename)
            if index >= 0:
                icon_dropdown.setCurrentIndex(index)

            self.table.setColumnWidth(3, self.icon_combobox_width)
            self.table.setCellWidget(row, 3, icon_dropdown)


            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(button.get("text", "")))

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        for col in [0, 1, 2, 4]:  
            self.table.setItem(row, col, QtWidgets.QTableWidgetItem(""))

        # Create the QComboBox with fixed size
            icon_dropdown = QtWidgets.QComboBox()
            icon_dropdown.setIconSize(QtCore.QSize( self.ICON_SIZE,  self.ICON_SIZE))  # Set icon size
            icon_dropdown.setFixedSize( self.icon_combobox_width,  self.icon_combobox_height)  # Adjust dropdown size

        # Populate dropdown with icons
        for icon_name in self.available_icons:
            icon_path = f"{self.icons_path}/{icon_name}"
            icon = QtGui.QIcon(icon_path)
            icon_dropdown.addItem(icon, "", icon_name)  

        # Default selection
        if self.available_icons:
            icon_dropdown.setCurrentIndex(0)

        self.adjust_window_size()

        self.table.setCellWidget(row, 3, icon_dropdown)

    def remove_selected_row(self):
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            self.table.removeRow(row)
            self.adjust_window_size()  # Adjust window size after removing a row

    def save(self):
        buttons = []
        for row in range(self.table.rowCount()):
            icon_widget = self.table.cellWidget(row, 3)  # Get the QComboBox
            selected_icon = icon_widget.currentData() if icon_widget else ""  # Retrieve filename
            full_icon_path = f"{self.icons_path}/{selected_icon}" if selected_icon else ""  # Ensure proper path

            button = {
                "label": self.table.item(row, 0).text() if self.table.item(row, 0) else "",
                "color": self.table.item(row, 1).text() if self.table.item(row, 1) else "",
                "tooltip": self.table.item(row, 2).text() if self.table.item(row, 2) else "",
                "icon": full_icon_path,  # Save the full path so it loads correctly
                "text": self.table.item(row, 4).text() if self.table.item(row, 4) else ""
            }
            buttons.append(button)


        # Write the new configuration to buttons_config.py
        new_config_text = "BUTTONS = " + repr(buttons)
        try:
            with open(self.config_path, "w") as f:
                f.write(new_config_text)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not write config file: {e}")
            return

        # Reload module
        import buttons_config
        importlib.reload(buttons_config)
        self.accept()

    def adjust_window_size(self):
        """Adjust the window size dynamically based on table content."""
        row_height = self.table.verticalHeader().defaultSectionSize()  # Height of one row
        row_count = self.table.rowCount()
        table_height = (row_count * row_height) + 50  # Add some padding

        # Get column widths to determine window width
        total_width = sum(self.table.columnWidth(i) for i in range(self.table.columnCount())) + 50

        # Set fixed size
        self.setFixedSize(total_width, table_height + 20)  # Add extra space for buttons

# Launch ConfigEditor UI Window via settings Button
def open_config_editor():

    config_path = os.path.join(os.path.dirname(__file__), "buttons_config.py")

    dlg = ConfigEditor(config_path,available_icons,icons_path)
    if dlg.exec_():
        print("Backdrop Buttons updated!")


# ----------------------------------------------
# 4. Functions
# ----------------------------------------------


def nodeIsInside(node, backdropNode):
    """
    Calculate top left pos and bottom right pos of all selected Nodes. Base for the createBackdrop() function.
    """
    topLeftNode = [node.xpos(), node.ypos()]
    topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
    bottomRightNode = [node.xpos() + node.screenWidth(),
                    node.ypos() + node.screenHeight()]
    bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(),
                        backdropNode.ypos() + backdropNode.screenHeight()]

    topLeft = ((topLeftNode[0] >= topLeftBackDrop[0]) and
            (topLeftNode[1] >= topLeftBackDrop[1]))
    bottomRight = ((bottomRightNode[0] <= bottomRightBackdrop[0]) and
                (bottomRightNode[1] <= bottomRightBackdrop[1]))

    return topLeft and bottomRight

def createBackdrop(icon, text, color):
    """
    Create Backdrop node based on selected nodes
    """
    sel = nuke.selectedNodes()
    if not sel:
        nuke.alert("Please select at least one node in your nodetree to create a Backdrop!")
        return
    
    bdX = min([node.xpos() for node in sel])
    bdY = min([node.ypos() for node in sel])
    bdW = max([node.xpos() + node.screenWidth() for node in sel]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in sel]) - bdY

    zOrder = 0
    selectedBackdropNodes = nuke.selectedNodes("BackdropNode")

    if selectedBackdropNodes:
        zOrder = min([node.knob("z_order").value() for node in selectedBackdropNodes]) - 1
    else:
        nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
        for nonBackdrop in sel:
            for backdrop in nonSelectedBackdropNodes:
                if nodeIsInside(nonBackdrop, backdrop):
                    zOrder = max(zOrder, backdrop.knob("z_order").value() + 1)

    left, top, right, bottom = (-30, -120, 30, 30)
    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)

    input_text = nuke.getInput('Backdrop Title:', f"{text}" )

    n = nuke.createNode("BackdropNode", inpanel=False)
    n["tile_color"].setValue(hex_to_nuke_color(color))
    n["note_font"].setValue("Arial")
    n["note_font_size"].setValue(50)
    n["z_order"].setValue(zOrder)

    if icon == "": 
        n["label"].setValue(f"<center>{input_text}</center>")
    else:
        icon = icon.replace(os.sep, "/")
        n["label"].setValue(f"<center><img src='{icon}'>{input_text}</center>")

    n['xpos'].setValue(bdX)
    n['ypos'].setValue(bdY)
    n['bdwidth'].setValue(bdW)
    n['bdheight'].setValue(bdH)
    n['selected'].setValue(True)

    for node in sel:
        node['selected'].setValue(True)

def scaleUp(nodes, step=50):
    """
    Search for Backdrop nodes in selected nodes and scale them up.
    """
    backdrop_nodes = [node for node in nodes if node.Class() == "BackdropNode"]

    if not backdrop_nodes:
        nuke.alert("Please select at least one Backdrop node!")
        return

    for i in backdrop_nodes:
        i["xpos"].setValue(i["xpos"].getValue() - step)
        i["ypos"].setValue(i["ypos"].getValue() - step)
        i["bdwidth"].setValue(i["bdwidth"].getValue() + step * 2)
        i["bdheight"].setValue(i["bdheight"].getValue() + step * 2)

def scaleDown(nodes, step=50):
    """
    Search for Backdrop nodes in selected nodes and scale them down.
    """
    backdrop_nodes = [node for node in nodes if node.Class() == "BackdropNode"]

    if not backdrop_nodes:
        nuke.alert("Please select at least one Backdrop node!")
        return

    for i in backdrop_nodes:
        i["xpos"].setValue(i["xpos"].getValue() + step)
        i["ypos"].setValue(i["ypos"].getValue() + step)
        i["bdwidth"].setValue(i["bdwidth"].getValue() - step * 2)
        i["bdheight"].setValue(i["bdheight"].getValue() - step * 2)

def updateTitle(nodes):
    """
    Check label texts of selected backdrop nodes and change them based on new user input.
    """
    backdrop_nodes = [node for node in nodes if node.Class() == "BackdropNode"]

    if not backdrop_nodes:
        nuke.alert("Please select at least one Backdrop node!")
        return
    
    for i in backdrop_nodes:

        text = i["label"].value()
        
        
        match = re.search(r"'>\s*(.*?)\s*</center>", text)
        if match:
            current_title = match.group(1)
        else:
            match = re.search(r"<center>\s*(.*?)\s*</center>", text)
            current_title = match.group(1)
        
        
        match_img = re.search(r"(<img .*?>)", text)
        if match_img:
            icon = match_img.group(1)
        else:
            icon =""
            

        new_title = nuke.getInput(f"Update Label Text ({current_title})", f"{current_title}")

        if icon != "":
            new_title = f"<center>{icon}{new_title}</center>"
        else:
            new_title = f"<center>{new_title}</center>"

        i["label"].setValue(new_title)
        
def updateTextsize(nodes):
    """
    Check label text sizes of selected backdrop nodes and change them based on new user input.
    Ensures input is a valid number.
    """
    backdrop_nodes = [node for node in nodes if node.Class() == "BackdropNode"]

    if not backdrop_nodes:
        nuke.alert("Please select at least one Backdrop node!")
        return

    for i in backdrop_nodes:

        text = i["label"].value()
        
        match = re.search(r"'>\s*(.*?)\s*</center>", text)
        if match:
            current_title = match.group(1)
        else:
            match = re.search(r"<center>\s*(.*?)\s*</center>", text)
            current_title = match.group(1)

        current_size = int(i["note_font_size"].value())  # Ensure it's an integer

        while True: 
            new_size = nuke.getInput(f"Text Size ({current_title})", str(current_size))

            if new_size is None:  
                return

            if new_size.isdigit():  
                i["note_font_size"].setValue(int(new_size))
                break
            else:
                nuke.alert("Invalid input! Please enter a number for the text size.")

def toggleFillBorder(nodes):
    """
    Toggles the 'appearance' knob of selected Backdrop nodes between Fill (0) and Border (1).
    If no Backdrop nodes are selected, an alert is shown.
    """
    backdrop_nodes = [node for node in nodes if node.Class() == "BackdropNode"]

    if not backdrop_nodes:
        nuke.alert("Please select at least one Backdrop node!")
        return

    for node in backdrop_nodes:
        current_value = node["appearance"].value()

        if current_value == "Border":
            node["appearance"].setValue("Fill")

        elif current_value == "Fill":
            node["appearance"].setValue("Border")

def randomizeBackdropColor(nodes):
    """
    Assigns a random color to all selected Backdrop nodes.
    If no Backdrop nodes are selected, an alert is shown.
    """
    backdrop_nodes = [node for node in nodes if node.Class() == "BackdropNode"]

    if not backdrop_nodes:
        nuke.alert("Please select at least one Backdrop node!")
        return

    for node in backdrop_nodes:
        random_color = random.randint(0, 0xFFFFFF)  # Generate a random RGB color
        node["tile_color"].setValue(random_color)

def hex_to_nuke_color(hex_color):
    """
    Convert a hex color string (e.g., "#RRGGBB") to a 32-bit integer in the format Nuke expects.
    Appends an alpha value of FF.
    """
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')
    # Append 'FF' for full opacity (alpha = 255)
    full_hex = hex_color + "FF"
    return int(full_hex, 16)

def find_nuke_icon(icon_name):

    resource_path = ":qrc/images"  # Nuke's default resource folder


    # Get a list of all icons in Nuke's internal resources
    icon_list = QtCore.QResource(':qrc/images').children() 
    icon_list.sort()

    if icon_name in icon_list:

        icon_path = f"{resource_path}/{icon_name}"

        return icon_path

def start():
    global bd_engineer
    bd_engineer = BD_Engineer()
    bd_engineer.show()

nuke.tprint(f'BD Engineer v{version}, built {releaseDate}.\nCopyright (c) 2025-{releaseDate.split()[-1]} Eric Prochnow. All Rights Reserved.')