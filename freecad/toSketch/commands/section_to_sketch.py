# section_to_sketch.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
import Part
from .vector_utils import vectors_to_numpy, fit_bspline_to_geom

class SectionToSketchFeature:
    """
    Command to convert Part sections or selected geometry into a Sketcher SketchObject.
    """

    def Activated(self):
        print("SectionToSketch Activated")
        for sel in FreeCADGui.Selection.getSelection():
            print(f"Selected: {sel.Label} ({sel.TypeId})")
            if sel.TypeId == 'Part::Feature':
                self.process_feature(sel)
            elif sel.TypeId == 'Sketcher::SketchObject':
                self.process_sketch(sel)
            else:
                print("Unsupported selection type.")

    def process_feature(self, obj):
        # Create a new Sketch in the active document
        new_sketch = FreeCAD.ActiveDocument.addObject(
            "Sketcher::SketchObject",
            f"{obj.Label}_Sketch"
        )
        new_sketch.Placement = obj.Placement

        print(f"Creating sketch: {new_sketch.Label}")

        # Process edges of the shape
        for edge in obj.Shape.Edges:
            print(f"Processing edge: {edge}")
            if edge.Curve.TypeId == 'Part::GeomLine':
                new_sketch.addGeometry(Part.LineSegment(edge.Vertexes[0].Point, edge.Vertexes[1].Point))
            elif edge.Curve.TypeId == 'Part::GeomBSplineCurve':
                # Fit B-spline from edge points
                points = [v.Point for v in edge.Vertexes]
                bsplines = fit_bspline_to_geom(vectors_to_numpy(points), max_error=0.5)
                if bsplines:
                    new_sketch.addGeometry(bsplines)
            else:
                print(f"Unsupported edge curve type: {edge.Curve.TypeId}")

        new_sketch.recompute()
        print(f"Sketch {new_sketch.Label} created from {obj.Label}.")

    def process_sketch(self, sketch):
        # Optionally: copy existing sketch geometry to a new sketch
        new_sketch = FreeCAD.ActiveDocument.addObject(
            "Sketcher::SketchObject",
            f"{sketch.Label}_Copy"
        )
        new_sketch.Placement = sketch.Placement

        for geo in sketch.Geometry:
            new_sketch.addGeometry(geo)

        new_sketch.recompute()
        print(f"Copied sketch {sketch.Label} to {new_sketch.Label}.")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'section2Sketch',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('SectionToSketch', 'Section to Sketch'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('SectionToSketch', 'Convert selected section to Sketch'),
        }

# Register the command
FreeCADGui.addCommand('section2SketchCommand', SectionToSketchFeature())

