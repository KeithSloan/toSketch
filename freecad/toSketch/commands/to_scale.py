# to_scale.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
from .toSObjects import toScale, ViewProvider

class ToScaleFeature:
    """Create a scaled copy of a selected object"""

    def Activated(self):
        for sel in FreeCADGui.Selection.getSelection():
            print(f'Selected object: {sel.Label} ({sel.TypeId})')
            if len(sel.InList) > 0:
                parent = sel.InList[0]
                obj = parent.newObject('Part::FeaturePython', sel.Label + '_Scale')
                toScale(obj, sel.Shape, sel.Shape.BoundBox)
                ViewProvider(obj.ViewObject)
            else:
                obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython', 'Scale')
                toScale(obj, sel.Shape, sel.Shape.BoundBox)
                ViewProvider(obj.ViewObject)

            # Reassign children
            for child in sel.OutList:
                obj.addObject(child)

            FreeCAD.ActiveDocument.removeObject(sel.Name)
            FreeCAD.ActiveDocument.recompute()

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toScale',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toScaleFeature', 'To Scale'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toScaleFeature', 'Create a scaled copy of the selected object')
        }

# Register command
FreeCADGui.addCommand('toScaleCommand', ToScaleFeature())

