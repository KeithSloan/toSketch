# remove_outer_box.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
import Part

class RemoveOuterBoxFeature:
    """
    Remove outer bounding box edges from selected sketch or shape.
    """

    def Activated(self):
        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            print("No object selected.")
            return

        for obj in selection:
            if hasattr(obj, "Shape") and obj.Shape.Edges:
                bbox = obj.Shape.BoundBox
                edges_to_remove = []

                for edge in obj.Shape.Edges:
                    # Check if edge is on the bounding box
                    sp = edge.Vertexes[0].Point
                    ep = edge.Vertexes[1].Point

                    if (vector_on_bbox(sp, bbox) and vector_on_bbox(ep, bbox)):
                        edges_to_remove.append(edge)

                if edges_to_remove:
                    print(f"Removing {len(edges_to_remove)} outer edges from {obj.Label}")
                    new_shape = obj.Shape.copy()
                    for edge in edges_to_remove:
                        try:
                            new_shape.removeGeometry(edge)
                        except Exception as e:
                            print(f"Could not remove edge: {e}")
                    obj.Shape = new_shape
                    obj.recompute()
                else:
                    print(f"No outer bounding edges detected for {obj.Label}")
            else:
                print(f"{obj.Label} has no shape or edges to process.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'removeOuterBox',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('RemoveOuterBoxFeature', 'Remove Outer Box'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('RemoveOuterBoxFeature', 'Remove outer bounding edges from selected shape or sketch'),
        }

# Utility function
def vector_on_bbox(v, bbox, tol=1e-6):
    """
    Check if a vector is on the bounding box.
    """
    return (
        abs(v.x - bbox.XMin) < tol or abs(v.x - bbox.XMax) < tol or
        abs(v.y - bbox.YMin) < tol or abs(v.y - bbox.YMax) < tol or
        abs(v.z - bbox.ZMin) < tol or abs(v.z - bbox.ZMax) < tol
    )

# Register the command
FreeCADGui.addCommand('removeOuterBoxCommand', RemoveOuterBoxFeature())

