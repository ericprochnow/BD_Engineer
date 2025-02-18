#------------------------------------------------------
# BD_Engineer - UI Settings
# Advanced Backdrop Tool for Nuke
# created by Eric Prochnow (ericprochnow.com)
version = '1.0'
releaseDate = 'Feb 16 2025'
#-----------------------------------------------------    
import nuke
import os
# ----------------------------------------------
# INSTRUCTIONS:
# Modify this file, if you want to change the UI settings or use different icons.
# Place it in your BD_Engineer directory. Do not rename it.
# ----------------------------------------------


# ----------------------------------------------
# 1. Icons 
# ----------------------------------------------

# Option 1: Use Nukes default icons
nukePATH = os.path.dirname(nuke.EXE_PATH)
icons_path = f"{nukePATH}/plugins/icons"

# Option 2: Use your own icons
# icons_path = r"C:\link\to\your\icon\folder\goes\here"


# ----------------------------------------------
# 2. UI Settings
# ----------------------------------------------

# Main Buttons
button_width = 50
button_height = 15
button_spacing = 8

# Text & Titles
main_title_size = 12
title_size = 8