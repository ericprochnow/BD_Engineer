import nuke

# --------------------------------------------------------------------------------------------
# # Choose how you want to use the tool in Nuke. Only one option is possible
# --------------------------------------------------------------------------------------------


# Option 1: Install as callable UI floating window

#import BD_Engineer
#nuke.menu("Nuke").findItem("Edit").addCommand("BD_Engineer", 'BD_Engineer.start()', "alt+b")


# Option 2: Install as dockable panel widget

from BD_Engineer import BD_Engineer
import nukescripts
nukescripts.registerWidgetAsPanel("BD_Engineer", "BD_Engineer", "BD_Engineer")