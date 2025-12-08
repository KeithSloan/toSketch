import FreeCAD, FreeCADGui
import Part
import math
from .geomutils import ordered_vertices, EPS_COINCIDENT

ANGLE_LIMIT = math.radians(2.0)

class CmdToCurveAuto:
    def GetResources(self):
        return {
            'Pixmap': '',
            'MenuText': 'Convert to curves (auto)',
            'ToolTip': 'Automatically detect curvature and replace segments with BSplines'
        }

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            FreeCAD.Console.PrintError("Select a sketch\n")
            return

        sketch = sel[0]
        doc = sketch.Document
        doc.openTransaction("toSketch toCurveAuto")

        newSketch = doc.addObject("Sketcher::SketchObject", sketch.Name + "_CurvesAuto")

        verts = ordered_vertices(sketch)

        segs = []
        cur = [verts[0]]

        for i in range(1, len(verts) - 1):
            p0, p1, p2 = verts[i - 1], verts[i], verts[i + 1]
            v1 = p1 - p0
            v2 = p2 - p1

            if v1.Length == 0 or v2.Length == 0:
                continue

            ang = v1.getAngle(v2)
            cur.append(p1)

            if ang > ANGLE_LIMIT:
                segs.append(cur)
                cur = [p1]

        cur.append(verts[-1])
        segs.append(cur)

        for pts in segs:
            if len(pts) < 3:
                newSketch.addGeometry(Part.LineSegment(pts[0], pts[-1]), False)
            else:
                spline = Part.BSplineCurve()
                spline.interpolate(pts)
                newSketch.addGeometry(spline.toShape(), False)

        doc.commitTransaction()
        doc.recompute()

    def IsActive(self):
        return True

toSketch_ToCurveAuto = CmdToCurveAuto()

