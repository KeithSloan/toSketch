# to_plane.py
import FreeCAD
import FreeCADGui
from PySide import QtCore

class ToSPlaneFeature:
    """Create a custom toPlane Part::FeaturePython object"""

    def Activated(self):
        from .toSObjects import toSPlane, ViewProvider

        obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython', 'toPlane')
        toSPlane(obj)
        ViewProvider(obj.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        # Set transparency for visual distinction
        obj.ViewObject.Transparency = 20

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toPlane',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature', 'Create toPlane'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature', 'Create a toPlane feature')
        }


class ToPlane2PartFeature:
    """Convert a toPlane object into a Part Plane"""

    def Activated(self):
        select_ex = FreeCADGui.Selection.getSelectionEx()
        for sel in select_ex:
            obj = sel.Object
            if obj.TypeId == 'Part::FeaturePython':
                if obj.Label.startswith('toPlane') or obj.Label.startswith('Plane'):
                    part_plane = FreeCAD.ActiveDocument.addObject("Part::Plane", "PartPlane")
                    # Set plane orientation
                    part_plane.Placement.Rotation.Axis = [0.0, 1.0, 0.0]
                    part_plane.Placement.Rotation.Angle = 1.5708  # 90 degrees
                    part_plane.Placement.Base = [-50, 0, -50]
                    part_plane.Length = 100
                    part_plane.Width = 100

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'Plane2Part',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature', 'toPlane → PartPlane'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature', 'Convert a toPlane object to a Part Plane')
        }


# Register commands
FreeCADGui.addCommand('toSPlaneCommand', ToSPlaneFeature())
FreeCADGui.addCommand('Plane2PartPlaneCommand', ToPlane2PartFeature())

