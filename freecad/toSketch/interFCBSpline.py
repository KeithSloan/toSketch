# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileNotice: Part of the ToSketch addon.

import numpy as np
import FreeCAD as App
import Part

def fit_bspline_to_geom(points, num_points_per_curve=100, max_error=1e-3):
    """
    Fit a set of points to one or more FreeCAD Part::GeomBSplineCurve dynamically.

    Parameters:
        points (np.ndarray): Array of shape (n, 3) with points to fit.
        num_points_per_curve (int): Number of points to sample on each B-spline.
        max_error (float): Maximum allowed error for curve fitting.

    Returns:
        curves (list): A list of Part::GeomBSplineCurve objects.
    """
    curves = []
    n_points = len(points)
    current_start = 0

    while current_start < n_points:
        # Try fitting a curve to all remaining points
        remaining_points = points[current_start:]

        # Fit a B-spline using FreeCAD's Part.BSplineCurve
        spline = Part.BSplineCurve()
        spline.interpolate(remaining_points)

        # Evaluate the error
        errors = []
        for pt in remaining_points:
            projected = spline.projectPointOnCurve(pt)[0]  # Project point onto spline
            errors.append(np.linalg.norm(pt - projected))
        mean_error = np.mean(errors)

        if mean_error > max_error:
            # Split and retry if error exceeds max_error
            split_index = len(remaining_points) // 2
            segment = remaining_points[:split_index]
            spline_segment = Part.BSplineCurve()
            spline_segment.interpolate(segment)
            curves.append(spline_segment)

            current_start += split_index
        else:
            # Acceptable fit, finalize this curve
            curves.append(spline)
            break

    return curves

