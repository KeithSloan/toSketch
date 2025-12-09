# -*- coding: utf-8 -*-
"""
FreeCAD Workbench: toSketch
Automatically loads all commands from the commands directory
"""

# Workbench metadata
WorkbenchName = "toSketch"
WorkbenchAuthor = "Keith Sloan"
WorkbenchIcon = ""  # path to icon if needed
WorkbenchMenuText = "toSketch"
WorkbenchToolTip = "toSketch Workbench - Sketch and Geometry Tools"

import FreeCAD
import FreeCADGui

# Import all commands
#from .commands.to_sketch import toSketchFeature
#from .commands.section_to_sketch import section2SketchFeature
#from .commands.to_plane import toSPlaneFeature, toPlane2PartFeature
#from .commands.to_curve_fit import toCurveFitFeature
#from .commands.to_line_curve_fit import toLineCurveFitFeature
#from .commands.to_curve_guided import toSketch_ToCurveGuided
#from .commands.to_macro import toMacroFeature
#from .commands.to_scale import toScaleFeature
#from .commands.to_reset_origin import toResetOriginFeature
#from .commands.to_shape_info import toShapeInfoFeature
#from .commands.to_line import toLineFeature
#from .commands.remove_outer_box import removeOuterBoxFeature
#from .commands.add_bbox_sketch import addBboxFeature
#from .commands.b_spline_to_arc import bSpline2ArcFeature
#from .commands.constraints_group import (
#    ConstraintsGroupFeature,
#    CheckSymmetryFeature,
#    CheckCoincidentFeature,
#    CheckHorizontalFeature,
#    CheckVerticalFeature,
#    addParallelConstraintsFeature
#    )

from .commands import section_to_sketch
from .commands import to_reset_origin
from .commands import add_bbox_sketch
from .commands import to_curve_fit
from .commands import to_scale
from .commands import b_spline_to_arc
from .commands import to_curve_guided
from .commands import to_shape_info
from .commands import constraints_group
from .commands import to_line_curve_fit
from .commands import to_sketch
from .commands import to_line
from .commands import to_macro
from .commands import remove_outer_box
from .commands import to_plane

# Define the Workbench class
class toSketchWorkbench(FreeCADGui.Workbench):
    MenuText = WorkbenchMenuText
    ToolTip = WorkbenchToolTip
    Icon = WorkbenchIcon

    def Initialize(self):
        """Register all commands with FreeCADGui"""
        FreeCAD.Console.PrintMessage("Initializing toSketch Workbench...\n")
        '''
        FreeCADGui.addCommand('toSketchCommand', toSketchFeature())
        FreeCADGui.addCommand('section2SketchCommand', section2SketchFeature())
        FreeCADGui.addCommand('Plane2PartPlaneCommand', toPlane2PartFeature())
        FreeCADGui.addCommand('toSPlaneCommand', toSPlaneFeature())
        FreeCADGui.addCommand('toCurveFitCommand', toCurveFitFeature())
        FreeCADGui.addCommand('toLineCurveFitCommand', toLineCurveFitFeature())
        FreeCADGui.addCommand('toCurveGuidedCommand', toSketch_ToCurveGuided)
        FreeCADGui.addCommand('toMacroCommand', toMacroFeature())
        FreeCADGui.addCommand('toScaleCommand', toScaleFeature())
        FreeCADGui.addCommand('toResetOriginCommand', toResetOriginFeature())
        FreeCADGui.addCommand('toShapeInfoCommand', toShapeInfoFeature())
        FreeCADGui.addCommand('toLineCommand', toLineFeature())
        FreeCADGui.addCommand('removeOuterBoxCommand', removeOuterBoxFeature())
        FreeCADGui.addCommand('addBboxCommand', addBboxFeature())
        FreeCADGui.addCommand('bSpline2ArcCommand', bSpline2ArcFeature())
        FreeCADGui.addCommand('ConstraintsGroupCmd', ConstraintsGroupFeature())
        FreeCADGui.addCommand('CheckSymmetryCmd', CheckSymmetryFeature())
        FreeCADGui.addCommand('CheckCoincidentCmd', CheckCoincidentFeature())
        FreeCADGui.addCommand('CheckVerticalCmd', CheckVerticalFeature())
        FreeCADGui.addCommand('CheckHorizontalCmd', CheckHorizontalFeature())
        FreeCADGui.addCommand('addParallelCmd', addParallelConstraintsFeature())
        '''

    def Activated(self):
        """Called when the workbench is activated"""
        FreeCAD.Console.PrintMessage("toSketch Workbench Activated\n")

    def Deactivated(self):
        """Called when the workbench is deactivated"""
        FreeCAD.Console.PrintMessage("toSketch Workbench Deactivated\n")

    def ContextMenu(self, recipient):
        """Optional context menu"""
        return []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# Register the workbench
FreeCADGui.addWorkbench(toSketchWorkbench)

