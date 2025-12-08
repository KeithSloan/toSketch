# b_spline_to_arc.py
import FreeCAD
import FreeCADGui
import Part
from PySide import QtCore
import math

class BSpline2ArcFeature:
    """Check B-splines in a sketch and convert segments to arcs if possible"""

    def Activated(self):
        select_ex = FreeCADGui.Selection.getSelectionEx()
        for sel in select_ex:
            obj = sel.Object
            if obj.TypeId == 'Sketcher::SketchObject':
                print(f'Checking sketch "{obj.Label}" for splines convertible to arcs')

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'BSpline2Arc',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature', 'BSpline → Arc'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature', 'Convert B-splines in a sketch to arcs')
        }

    def check_bspline_close_to_circle(self, bspline, tolerance=1e-3):
        """Check if B-spline points are close to a circle"""
        num_samples = 100
        points = [
            bspline.value(bspline.ParameterRange[0] +
                          i * (bspline.ParameterRange[1] - bspline.ParameterRange[0]) / (num_samples - 1))
            for i in range(num_samples)
        ]

        try:
            circle = Part.Circle()
            circle.fitThroughPoints(points)
            deviations = [abs(circle.Center.distanceToPoint(p) - circle.Radius) for p in points]
            max_deviation = max(deviations)

            if max_deviation <= tolerance:
                return True, {"center": circle.Center, "radius": circle.Radius, "deviation": max_deviation}
            else:
                return False, {"max_deviation": max_deviation}
        except Exception as e:
            return False, {"error": str(e)}

    def subdivide_bspline(self, bspline, num_segments=5, arc_tolerance=1e-3):
        """Split a B-spline into sub-segments and arcs if possible"""
        parameter_range = bspline.ParameterRange
        step = (parameter_range[1] - parameter_range[0]) / num_segments
        segments = []

        for i in range(num_segments):
            start_param = parameter_range[0] + i * step
            end_param = start_param + step
            segment = bspline.trim(start_param, end_param)

            is_arc, details = self.check_bspline_close_to_circle(segment, tolerance=arc_tolerance)
            if is_arc:
                circle = Part.Circle()
                circle.Center = details["center"]
                circle.Radius = details["radius"]
                arc = circle.toShape(segment.startPoint(), segment.endPoint())
                segments.append(arc)
            else:
                segments.append(segment)

        return segments


# Register command
FreeCADGui.addCommand('bSpline2ArcCommand', BSpline2ArcFeature())

