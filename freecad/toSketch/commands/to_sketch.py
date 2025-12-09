# to_sketch.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
import Part
from freecad.toSketch.commands import vector_utils  # central vector helper

class ToSketchFeature:
    """
    Command to convert selected geometry into a Sketcher sketch.
    """

    def Activated(self):
        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            print("No object selected.")
            return

        for obj in selection:
            if not hasattr(obj, 'Shape'):
                print(f"Object {obj.Label} has no Shape.")
                continue

            new_sketch = FreeCAD.ActiveDocument.addObject(
                "Sketcher::SketchObject",
                f"{obj.Label}_Sketch"
            )
            new_sketch.Placement = obj.Placement

            # Process edges from the object shape
            edges = obj.Shape.Edges
            print(f"Processing {len(edges)} edges from {obj.Label}")

            for edge in edges:
                if isinstance(edge, Part.Line):
                    new_sketch.addGeometry(Part.LineSegment(edge.Vertexes[0].Point, edge.Vertexes[1].Point))
                elif isinstance(edge, Part.Circle):
                    new_sketch.addGeometry(Part.Circle(edge.Center, edge.Axis, edge.Radius))
                elif isinstance(edge, Part.BSplineCurve):
                    new_sketch.addGeometry(edge)
                elif isinstance(edge, Part.ArcOfCircle):
                    new_sketch.addGeometry(edge)
                else:
                    print(f"Unsupported edge type: {type(edge)}")

            new_sketch.recompute()
            print(f"Sketch created: {new_sketch.Label}")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toSketch',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('ToSketchFeature', 'Convert to Sketch'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('ToSketchFeature', 'Convert selected geometry into a Sketcher sketch'),
        }

# Register the command
FreeCADGui.addCommand('toSketchCommand', ToSketchFeature())

