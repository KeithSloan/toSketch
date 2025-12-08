# to_reset_origin.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
from .toSObjects import toResetOrigin, ViewProvider

class ToResetOriginFeature:

    def Activated(self):
        for sel in FreeCADGui.Selection.getSelection():
            print(f'ToResetOrigin Feature Selected: {sel.TypeId}')

            ignore_types = ['App::Part']

            if hasattr(sel, 'Shape') and sel.TypeId not in ignore_types:
                if len(sel.InList) > 0:
                    parent = sel.InList[0]
                    obj = parent.newObject(
                        'Part::FeaturePython',
                        sel.Label + '_Reset_Origin'
                    )
                    toResetOrigin(obj, sel.Shape, sel.Shape.BoundBox)
                    ViewProvider(obj.ViewObject)
                else:
                    obj = FreeCAD.ActiveDocument.addObject(
                        'Part::FeaturePython',
                        sel.Label + '_Reset_Origin'
                    )
                    toResetOrigin(obj, sel.Shape, sel.Shape.BoundBox)
                    ViewProvider(obj.ViewObject)

                # Reassign children objects
                for child in sel.OutList:
                    obj.addObject(child)

                FreeCAD.ActiveDocument.removeObject(sel.Name)
                FreeCAD.ActiveDocument.recompute()

            elif sel.TypeId == "Mesh::Feature":
                print(f"Mesh Center of Gravity: {sel.Mesh.CenterOfGravity}")
                placement = FreeCAD.Placement()
                placement.Base = FreeCAD.Vector(
                    -sel.Mesh.CenterOfGravity.x,
                    -sel.Mesh.CenterOfGravity.y,
                    -sel.Mesh.CenterOfGravity.z
                )

                # Apply transform
                mesh_copy = sel.Mesh.copy()
                mesh_copy.transform(placement.toMatrix())
                sel.Mesh = mesh_copy

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toResetOrigin',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toResetOriginFeature', 'To Reset Origin'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toResetOriginFeature', 'To Reset Origin'),
        }

# --- Register command ---
FreeCADGui.addCommand('toResetOriginCommand', ToResetOriginFeature())

