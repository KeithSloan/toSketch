# vector_utils.py
# Central utility functions for vectors, lines, and B-spline operations
import FreeCAD
import Part
import math
import numpy as np


def vectors_to_numpy(vectors, plane="XY"):
    """
    Convert a list of FreeCAD vectors into a 2D NumPy array for a specified plane.
    
    Parameters:
        vectors (list of FreeCAD.Vector)
        plane (str): "XY", "XZ", "YZ"
        
    Returns:
        np.ndarray: Shape (n,2)
    """
    plane_map = {
        "XY": lambda v: (v.x, v.y),
        "XZ": lambda v: (v.x, v.z),
        "YZ": lambda v: (v.y, v.z)
    }
    if plane not in plane_map:
        raise ValueError(f"Invalid plane {plane}, must be XY, XZ, or YZ.")
    return np.array([plane_map[plane](v) for v in vectors])


def distance_between_points(p1, p2):
    """Return Euclidean distance between two FreeCAD vectors."""
    return (p2 - p1).Length


def are_contiguous(start_point, end_point, last_start, last_end, tolerance=1e-6):
    """
    Check if a line segment is contiguous with previous segment.
    
    Returns:
        (bool, FreeCAD.Vector, FreeCAD.Vector)
    """
    if last_end.distanceToPoint(start_point) <= tolerance:
        return True, last_start, end_point
    if last_start.distanceToPoint(end_point) <= tolerance:
        return True, start_point, end_point
    if last_start.distanceToPoint(start_point) <= tolerance:
        return True, end_point, start_point
    if last_end.distanceToPoint(end_point) <= tolerance:
        return True, end_point, start_point
    return False, last_start, last_end


def angle_between_lines(p0, p1, p2):
    """
    Compute angle between two lines: p0->p1 and p1->p2
    Returns angle in radians
    """
    v1 = p1 - p0
    v2 = p2 - p1
    dot = v1.dot(v2)
    norm = v1.Length * v2.Length
    if norm == 0:
        return 0.0
    angle = math.acos(max(min(dot / norm, 1.0), -1.0))
    return angle


def fit_bspline_to_geom(points, tolerance=1e-4, max_error=0.5):
    """
    Fit a B-spline to a sequence of FreeCAD vectors (or numpy array shape Nx2)
    Returns Part.BSplineCurve
    """
    if isinstance(points, np.ndarray):
        pts = [FreeCAD.Vector(p[0], p[1], 0) for p in points]
    else:
        pts = points
    if len(pts) < 2:
        return []
    curve = Part.BSplineCurve()
    curve.interpolate(pts)
    return [curve.toShape()]


def subdivide_bspline(bspline, num_segments=5, arc_tolerance=1e-3):
    """
    Subdivide B-spline into smaller B-splines or arcs if possible.
    Returns list of Part.Shape (BSplines or arcs)
    """
    parameter_range = bspline.ParameterRange
    step = (parameter_range[1] - parameter_range[0]) / num_segments
    segments = []
    for i in range(num_segments):
        start_param = parameter_range[0] + i * step
        end_param = start_param + step
        segment = bspline.trim(start_param, end_param)
        # Attempt circle fit
        is_arc, details = check_bspline_close_to_circle(segment, arc_tolerance)
        if is_arc:
            circle = Part.Circle()
            circle.Center = details["center"]
            circle.Radius = details["radius"]
            arc = circle.toShape(segment.startPoint(), segment.endPoint())
            segments.append(arc)
        else:
            segments.append(segment.toShape())
    return segments


def check_bspline_close_to_circle(bspline, tolerance=1e-3):
    """
    Check if a B-spline can be approximated as a circular arc.
    Returns (bool, dict)
    """
    num_samples = 50
    points = [bspline.value(bspline.ParameterRange[0] +
                            i * (bspline.ParameterRange[1] -
                            bspline.ParameterRange[0]) / (num_samples - 1))
              for i in range(num_samples)]
    try:
        circle = Part.Circle()
        circle.fitThroughPoints(points)
        deviations = [abs(circle.Center.distanceToPoint(p) - circle.Radius) for p in points]
        max_dev = max(deviations)
        if max_dev <= tolerance:
            return True, {"center": circle.Center, "radius": circle.Radius, "deviation": max_dev}
        else:
            return False, {"max_deviation": max_dev}
    except Exception as e:
        return False, {"error": str(e)}

