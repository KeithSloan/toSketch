import FreeCAD, FreeCADGui
import Part
from .geomutils import ordered_vertices, EPS_COINCIDENT

class CmdToCurveGuided:
    def GetResources(self):
        return {
            'Pixmap': '',
            'MenuText': 'Convert to curves (guided)',
            'ToolTip': 'Use user-placed coincident points as break markers'
        }

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            FreeCAD.Console.PrintError("Select a sketch\n")
            return

        sketch = sel[0]
        doc = sketch.Document
        doc.openTransaction("toSketch toCurveGuided")

        newSketch = doc.addObject("Sketcher::SketchObject", sketch.Name + "_CurvesGuided")

        verts = ordered_vertices(sketch)

        # collect breakpoints from Coincident constraints
        breakpts = set()
        for c in sketch.Constraints:
            if c.Type == "Coincident":
                try:
                    p = sketch.getPoint(c.GeoId, c.PointPos)
                    breakpts.add(p)
                except:
                    pass

        segments = []
        cur = []

        for v in verts:
            cur.append(v)
            if any(v.distanceToPoint(bp) < EPS_COINCIDENT for bp in breakpts):
                segments.append(cur)
                cur = []

        if cur:
            segments.append(cur)

        for pts in segments:
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

toSketch_ToCurveGuided = CmdToCurveGuided()

