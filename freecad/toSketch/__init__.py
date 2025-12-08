# toSketch/__init__.py
"""
New-style FreeCAD 1.0+ workbench: toSketch
"""

import FreeCAD, FreeCADGui

# -------------------------------
# Workbench Metadata
# -------------------------------
Workbench = {
    "Name": "toSketch",
    "Tooltip": "toSketch workbench",
    "Icon": "Resources/icons/toSWorkbench.svg",
}

# -------------------------------
# Setup (runs BEFORE GUI loads)
# -------------------------------
def setup():
    FreeCAD.Console.PrintMessage("[toSketch] Workbench setup loaded\n")

