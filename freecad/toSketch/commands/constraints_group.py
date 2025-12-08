# constraints_group.py
import FreeCAD
import FreeCADGui
from PySide import QtCore

# --- Main Group Command ---
class ConstraintsGroupFeature:
    """Group of Constraints Commands"""

    def GetCommands(self):
        """Tuple of command names included in the group"""
        return (
            "CheckSymmetryCmd",
            "CheckCoincidentCmd",
            "CheckHorizontalCmd",
            "CheckVerticalCmd",
            "AddParallelCmd",
        )

    def GetResources(self):
        return {
            "Pixmap": "Constraints_Group",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("Constraints Group", "Constraints Group"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "Constraints Group", "Group of Constraints Commands"
            ),
        }

    def IsActive(self):
        return True


# --- Individual Constraints Commands ---

# Check Symmetry
class CheckSymmetryFeature:
    def Activated(self):
        from freecad.toSketch.symmetricConstraints import add_symmetric_constraints

        for sel in FreeCADGui.Selection.getSelection():
            if sel.TypeId == 'Sketcher::SketchObject':
                add_symmetric_constraints(sel, tol=1e-5)
            else:
                print("Please select a Sketch first.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            "Pixmap": "CheckSymmetry",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("CheckSymmetry", "Check & Add Symmetry Command"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("CheckSymmetry", "Check & Add Symmetry Command"),
        }

# Check Coincident
class CheckCoincidentFeature:
    def Activated(self):
        from freecad.toSketch.addCoincidentConstraints import add_coincident_constraints

        sel = FreeCADGui.Selection.getSelection()
        if sel and sel[0].TypeId == 'Sketcher::SketchObject':
            add_coincident_constraints(sel[0])
        else:
            print("Please select a Sketch first.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            "Pixmap": "CheckCoincident",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("CheckCoincident", "Check & Add Coincident Command"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("CheckCoincident", "Check & Add Coincident Command"),
        }

# Check Horizontal
class CheckHorizontalFeature:
    def Activated(self):
        from freecad.toSketch.addHorizontalConstraints import add_horizontal_constraints

        sel = FreeCADGui.Selection.getSelection()
        if sel and sel[0].TypeId == 'Sketcher::SketchObject':
            add_horizontal_constraints(sel[0])
        else:
            print("Please select a Sketch first.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            "Pixmap": "CheckHorizontal",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("CheckHorizontal", "Check & Add Horizontal Command"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("CheckHorizontal", "Check & Add Horizontal Command"),
        }

# Check Vertical
class CheckVerticalFeature:
    def Activated(self):
        from freecad.toSketch.addVerticalConstraints import add_vertical_constraints

        sel = FreeCADGui.Selection.getSelection()
        if sel and sel[0].TypeId == 'Sketcher::SketchObject':
            add_vertical_constraints(sel[0])
        else:
            print("Please select a Sketch first.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            "Pixmap": "CheckVertical",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("CheckVertical", "Check & Add Vertical Command"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("CheckVertical", "Check & Add Vertical Command"),
        }

# Add Parallel
class AddParallelConstraintsFeature:
    def Activated(self):
        from freecad.toSketch.addParallelConstraints import add_parallel_constraints

        sel = FreeCADGui.Selection.getSelection()
        if sel and sel[0].TypeId == 'Sketcher::SketchObject':
            add_parallel_constraints(sel[0])
        else:
            print("Please select a Sketch first.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            "Pixmap": "AddParallelCmd",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("AddParallelCmd", "Add Parallel Constraints Command"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("AddParallelCmd", "Add Parallel Constraints Command"),
        }


# --- Register commands ---
FreeCADGui.addCommand('ConstraintsGroupCmd', ConstraintsGroupFeature())
FreeCADGui.addCommand('CheckSymmetryCmd', CheckSymmetryFeature())
FreeCADGui.addCommand('CheckCoincidentCmd', CheckCoincidentFeature())
FreeCADGui.addCommand('CheckHorizontalCmd', CheckHorizontalFeature())
FreeCADGui.addCommand('CheckVerticalCmd', CheckVerticalFeature())
FreeCADGui.addCommand('AddParallelCmd', AddParallelConstraintsFeature())

