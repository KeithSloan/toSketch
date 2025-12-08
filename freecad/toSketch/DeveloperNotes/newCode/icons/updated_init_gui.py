import FreeCADGui as Gui
from .preferences import toSketchPreferencesPage

Gui.addPreferencePage(toSketchPreferencesPage(), "toSketch")

