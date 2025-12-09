# to_curve_guided.py
import FreeCAD
import FreeCADGui
import Part
from freecad.toSketch.commands.vector_utils import EPS_COINCIDENT
from freecad.toSketch.commands.geomutils import ordered_vertices

class ToCurveGuidedFeature:
    """
    Convert a sketch to curves using user-placed coincident points as break markers.
    """

    def Activated(self):
        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            FreeCAD.Console.PrintError("Select a sketch to convert.\n")
            return

        sketch = selection[0]
        if sketch.TypeId != 'Sketcher::SketchObject':
            FreeCAD.Console.PrintError("Selected object is not a Sketch.\n")
            return

        doc = sketch.Document
        doc.openTransaction("toSketch toCurveGuided")

        new_sketch_name = sketch.Name + "_CurvesGuided"
        newSketch = doc.addObject("Sketcher::SketchObject", new_sketch_name)
        newSketch.Placement = sketch.Placement

        # Ordered vertices of the sketch
        verts = ordered_vertices(sketch)

        # Collect breakpoints from Coincident constraints
        breakpoints = set()
        for c in sketch.Constraints:
            if c.Type == "Coincident":
                try:
                    pt = sketch.getPoint(c.GeoId, c.PointPos)
                    breakpoints.add(pt)
                except Exception:
                    pass

        # Split vertices into segments at breakpoints
        segments = []
        current = []
        for v in verts:
            current.append(v)
            if any(v.distanceToPoint(bp) < EPS_COINCIDENT for bp in breakpoints):
                segments.append(current)
                current = []

        if current:
            segments.append(current)

        # Add geometry to new sketch
        for pts in segments:
            if len(pts) < 2:
                continue  # ignore degenerate
            elif len(pts) == 2:
                newSketch.addGeometry(Part.LineSegment(pts[0], pts[1]), False)
            else:
                spline = Part.BSplineCurve()
                spline.interpolate(pts)
                newSketch.addGeometry(spline.toShape(), False)

        doc.commitTransaction()
        doc.recompute()
        FreeCAD.Console.PrintMessage(f"Created guided curve sketch: {new_sketch_name}\n")

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': '',
            'MenuText': 'Convert to Curves (Guided)',
            'ToolTip': 'Use user-placed coincident points as break markers'
        }


# Register command
FreeCADGui.addCommand('toCurveGuidedCommand', ToCurveGuidedFeature())

