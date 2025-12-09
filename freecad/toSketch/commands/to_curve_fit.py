# to_curve_fit.py
import FreeCAD
import FreeCADGui
import Part
from PySide import QtCore
from freecad.toSketch.commands import vector_utils as vu

class ToCurveFitFeature:
    """Fits selected sketch geometry to B-spline or line curves."""

    def Activated(self):
        for sel in FreeCADGui.Selection.getSelection():
            if sel.TypeId != 'Sketcher::SketchObject':
                print("Please select a SketchObject.")
                continue

            print(f"Curve fitting sketch: {sel.Label}")
            new_sketch = FreeCAD.ActiveDocument.addObject(
                "Sketcher::SketchObject", f"{sel.Label}_CurveFit"
            )
            new_sketch.Placement = sel.Placement
            self.process_geometry(new_sketch, sel.Geometry)
            new_sketch.recompute()

    def process_geometry(self, new_sketch, geom, angle_threshold=15.0):
        """Process geometry to form fitted curves"""
        import math

        self.new_sketch = new_sketch
        self.vectors = []
        self.last_start = None
        self.last_point = None
        new_line = True

        for g in geom:
            if g.TypeId == 'Part::GeomLineSegment':
                if new_line:
                    self.vectors.append(g.StartPoint)
                    self.last_start = g.StartPoint
                    self.last_point = g.EndPoint
                    new_line = False
                    flush_line = True
                else:
                    contig, new_start, new_end = vu.are_contiguous(
                        g.StartPoint, g.EndPoint, self.last_start, self.last_point
                    )
                    if not contig:
                        self.flush_vectors()
                        self.vectors = []
                        new_line = True

                    angle = vu.angle_between_lines(self.last_start, g.StartPoint, g.EndPoint)
                    delta = math.radians(angle_threshold)
                    if angle > delta and angle < (math.pi - delta):
                        self.new_sketch.addGeometry(Part.LineSegment(self.last_start, self.last_point))
                        self.vectors = [self.last_point]
                        flush_line = False
                        self.last_start = self.last_point
                        self.last_point = g.EndPoint
                        self.vectors.append(g.EndPoint)
                    else:
                        self.last_start = new_start
                        self.last_point = new_end

            elif g.TypeId == 'Part::GeomArcOfCircle':
                self.flush_vectors()
                self.new_sketch.addGeometry(g)
                new_line = True
            else:
                print(f"Unknown TypeId: {g.TypeId}")

        self.flush_vectors()

    def flush_vectors(self):
        """Convert collected vectors into B-spline or lines"""
        if len(self.vectors) < 2:
            return

        if len(self.vectors) < 4:
            for v in self.vectors:
                self.new_sketch.addGeometry(Part.LineSegment(self.last_start, v))
                self.last_start = v
        else:
            points = vu.vectors_to_numpy(self.vectors)
            curves = vu.fit_bspline_to_geom(points)
            for c in curves:
                self.new_sketch.addGeometry(c)

        self.vectors = []

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toCurveFit',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toCurveFitFeature', 'To CurveFit'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toCurveFitFeature', 'Fit sketch geometry to curves')
        }

# Register command with FreeCAD GUI
FreeCADGui.addCommand('toCurveFitCommand', ToCurveFitFeature())

