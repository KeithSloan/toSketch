# add_bbox_sketch.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
import Part

class AddBboxFeature:
    """
    Command to create a Sketcher sketch representing the bounding box of a selected object.
    """

    def Activated(self):
        print("AddBboxFeature Activated")

        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            print("No object selected.")
            return

        for obj in selection:
            if not hasattr(obj, 'Shape'):
                print(f"Object {obj.Label} has no Shape.")
                continue

            bbox = obj.Shape.BoundBox
            print(f"Bounding box for {obj.Label}: {bbox}")

            # Create a new Sketch
            sketch = FreeCAD.ActiveDocument.addObject(
                "Sketcher::SketchObject",
                f"{obj.Label}_BBox"
            )

            # Set placement to match object
            sketch.Placement = obj.Placement

            # Define the 4 corner points of the bounding box
            p1 = FreeCAD.Vector(bbox.XMin, bbox.YMin, 0)
            p2 = FreeCAD.Vector(bbox.XMax, bbox.YMin, 0)
            p3 = FreeCAD.Vector(bbox.XMax, bbox.YMax, 0)
            p4 = FreeCAD.Vector(bbox.XMin, bbox.YMax, 0)

            # Add edges of the bounding box as line segments
            sketch.addGeometry(Part.LineSegment(p1, p2))
            sketch.addGeometry(Part.LineSegment(p2, p3))
            sketch.addGeometry(Part.LineSegment(p3, p4))
            sketch.addGeometry(Part.LineSegment(p4, p1))

            sketch.recompute()
            print(f"Bounding box sketch created: {sketch.Label}")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'addBbox',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('AddBboxFeature', 'Add Bounding Box Sketch'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('AddBboxFeature', 'Create a Sketch representing the bounding box of the selected object'),
        }

# Register the command
FreeCADGui.addCommand('addBboxCommand', AddBboxFeature())

