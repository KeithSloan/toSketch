# to_shape_info.py
import FreeCAD
import FreeCADGui
from PySide import QtCore

class ToShapeInfoFeature:
    """Display detailed shape information of selected object"""

    def Activated(self):
        for sel in FreeCADGui.Selection.getSelection():
            print(f"Selected Object: {sel.Label}")
            print(f"TypeId: {sel.TypeId}")

            if hasattr(sel, 'Shape'):
                shape = sel.Shape
                print(f"Number of Faces    : {len(shape.Faces)}")
                print(f"Number of Edges    : {len(shape.Edges)}")
                print(f"Number of Vertexes : {len(shape.Vertexes)}")
                print(f"Number of Wires    : {len(shape.Wires)}")

                print(f"InList  : {[obj.Label for obj in sel.InList]}")
                print(f"OutList : {[obj.Label for obj in sel.OutList]}")

                if len(shape.Faces) > 0:
                    print("Face Properties:")
                    for i, f in enumerate(shape.Faces):
                        print(f"  Face {i}: Area = {f.Area}, Center = {f.CenterOfMass}")

                if len(shape.Edges) > 0:
                    print("Edge Properties:")
                    for i, e in enumerate(shape.Edges):
                        print(f"  Edge {i}: Length = {e.Length}")
            else:
                print("Selected object has no shape attribute")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toShapeInfo',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toShapeInfo', 'Shape Info'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toShapeInfo', 'Display detailed information about the shape')
        }

# Register command
FreeCADGui.addCommand('toShapeInfoCommand', ToShapeInfoFeature())

