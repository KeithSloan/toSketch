import FreeCAD, FreeCADGui
import Part
from .geomutils import merge_connected_lines, EPS_COINCIDENT

class toLineFeature:
    def GetResources(self):
        return {
            'Pixmap': 'toLine',
            'MenuText': 'Convert short segments to long lines',
            'ToolTip': 'Merge collinear short edges into single long lines'
        }

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            FreeCAD.Console.PrintError("Select a sketch\n")
            return
        elif sel.TypeId == 'Sketcher::SketchObject' :
                geometry = sel.Geometry
                self.newSketch = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", \
                           "Fitted_"+sel.Name)
                self.newSketch.Placement = sel.Placement


        sketch = sel[0]
        doc = sketch.Document
        doc.openTransaction("toSketch toLine")

        newSketch = doc.addObject("Sketcher::SketchObject", sketch.Name + "_Lines")

        lines = [
            geo for geo in sketch.Geometry
            if geo.__class__.__name__ == "LineSegment"
        ]

        chains = merge_connected_lines(lines)

        for chain in chains:
            pts = []
            for seg in chain:
                pts.append(seg.StartPoint)
                pts.append(seg.EndPoint)

            p0 = pts[0]
            v = (pts[-1] - pts[0]).normalize()
            projections = [(p - p0).dot(v) for p in pts]
            start = p0 + v * min(projections)
            end   = p0 + v * max(projections)

            newSketch.addGeometry(Part.LineSegment(start, end), False)

        doc.commitTransaction()
        doc.recompute()

    def IsActive(self):
        return True

toSketch_ToLine = toLineFeature()

