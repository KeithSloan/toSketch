import FreeCAD, Draft, Part
import math

# Used by toSketch - for Section to Sketch
def shapes2Sketch(shapes, name, auto=False) :
    print(f'shapes2sketch {name}')
    sketch = Draft.makeSketch(shapes, autoconstraints=auto, \
                addTo=None, delete=False, name=name,  \
                         radiusPrecision=-1, tol=1e-3)
    return sketch
    #else:
    #        print(f"No shapes for sketch")

# Function to test if two GeomLineSegments are contiguous
def are_contiguous(line1, line2, tolerance=1e-6):
    """
    Check if two Geom.LineSegment objects are contiguous.

    :param line1: First Geom.LineSegment
    :param line2: Second Geom.LineSegment
    :param tolerance: Maximum distance to consider as contiguous
    :return: True if the lines are contiguous, False otherwise
    """
    # Get the start and end points of the first line
    start1 = line1.StartPoint
    end1 = line1.EndPoint
    
    # Get the start and end points of the second line
    start2 = line2.StartPoint
    end2 = line2.EndPoint
    
    # Check if any endpoint of one line matches the endpoint of the other line
    if (start1.distanceToPoint(start2) <= tolerance or
        start1.distanceToPoint(end2) <= tolerance or
        end1.distanceToPoint(start2) <= tolerance or
        end1.distanceToPoint(end2) <= tolerance):
        return True
    
    return False


def angle_between_lines(v1, v2, v3):
    """
    Calculate the angle between the line from v1 to v2 and the line from v2 to v3.

    Parameters:
        v1, v2, v3 (App.Vector): The three FreeCAD vectors.

    Returns:
        float: The angle in degrees between the two lines.
    """
    import numpy as np
    import math

    print(f"{v1} {v2} {v3}")
    # Direction vectors for the lines
    dir1 = v2 - v1
    dir2 = v3 - v2

    # Normalize the direction vectors
    dir1_normalized = dir1.normalize()
    dir2_normalized = dir2.normalize()

    # Dot product to find cosine of the angle
    cos_theta = dir1_normalized * dir2_normalized  # Dot product
    cos_theta = max(min(cos_theta, 1.0), -1.0)  # Clamp to avoid numerical errors

    # Angle in radians
    angle_radians = np.arccos(cos_theta)
    # Adjust Angle
    adjusted_angle = angle_radians - (1 * math.pi)
    #print(f"Angle in Radians {angle_radians} {adjusted_angle}")

    angle_degrees = np.degrees(angle_radians)

    #print(f"Angle Between Lines {v1} {v2} {v3} angle degrees {angle_degrees}")
    #print(f"Abs angle {angle_degrees} {abs(angle_radians)}")
    return abs(adjusted_angle)

def vectors_to_numpy(vectors):
    """
    Convert a list of FreeCAD.Vector objects to a NumPy array of shape (n, 3).

    Parameters:
        vectors (list of App.Vector): List of FreeCAD.Vector objects.

    Returns:
        np.ndarray: A 2D NumPy array of shape (n, 3), where n is the number of vectors.
    """
    import numpy as np

    return np.array([[v.x, v.y, v.z] for v in vectors])

def remove_duplicates(points, tolerance=1e-6):
    """
    Remove duplicate or near-identical points from a numpy array.

    Parameters:
        points (np.ndarray): Array of shape (n, 3).
        tolerance (float): Tolerance for considering points as duplicates.

    Returns:
        np.ndarray: Filtered array of points.
    """
    import numpy as np
    unique_points = [points[0]]
    for pt in points[1:]:
       if np.linalg.norm(pt - unique_points[-1]) > tolerance:
           unique_points.append(pt)
    return np.array(unique_points)

def create_line_segments_from_vectors(vector_list):
    """
    Create a list of Part::GeomLineSegment objects connecting consecutive vectors.


    Parameters:
       vector_list (list of FreeCAD.Vector): List of n FreeCAD vectors.

    Returns:
       list of Part.GeomLineSegment: List of n-1 line segments.
    """
    import FreeCAD, Part
    if len(vector_list) < 2:
       raise ValueError("The list must contain at least two vectors to create line segments.")

    line_segments = []
    print(vector_list)
    for i in range(len(vector_list) - 1):
       # Create a GeomLineSegment between vector[i] and vector[i+1]
        line_segment = Part.LineSegment(
            FreeCAD.Vector(vector_list[i]),
            FreeCAD.Vector(vector_list[i + 1])
            )   
        line_segments.append(line_segment)

    return line_segments

def reduce_list_by_percentage(lst, percentage):
    """
    Retain first and last items of list, reduce the rest the list by a given fraction.

    Args:
        lst (list): The original list to be reduced.
        percentage (int): The percentagen

    Note: There is no check on validity of percentage value, comes from ComboBox
   
   Returns:
        list: A reduced list with first and last items and  specified percentage of intervening elements retained.

    """
    # list without first and last items
    to_reduce = lst[1:-1]
    length = len(to_reduce)
    
    # Calculate the skip number to retain percentage of a list
    target_length = length * percentage

    skip = int(length / target_length)
    int(100 / percentage - 1)  # skip = 1 (every 2nd element retained)
    print(f"Percentage {percentage} Skip {skip}")

    # Select evenly spaced items from the list
    reduced_list = to_reduce[::skip]
    #reduced_list = to_reduce[::3]

    # Prepend the skipped items back to the reduced list
    return [lst[0]] + reduced_list + [lst[-1]]

def fit_bspline_to_geom(method, points, tolerance, max_error):
    # Remove duplicates and validate points
    points = remove_duplicates(points)
    print(f"fit_bspline_to_geom method {method}")
    if method == "PartBSpline":
        curves = fit_bspline_to_geom_PartBSpline(points, tolerance, max_error)
        return curves
    elif method == "Scipy":
        curves = fit_bspline_to_geom_scipy(points, tolerance, max_error)
        return curves
    elif method == "Geomdl":
        curves = fit_bspline_to_geom_geomdl(points, tolerance, max_error)
        return curves
    print("Invalid Method")    

def fit_bspline_to_geom_PartBSpline(points, tolerance, max_error):
    """
    Fit a set of points to one or more FreeCAD Part::GeomBSplineCurve dynamically.

    Parameters:
        points (np.ndarray): Array of shape (n, 3) with points to fit.
        num_points_per_curve (int): Number of points to sample on each B-spline.
        max_error (float): Maximum allowed error for curve fitting.

    Returns:
        curves (list): A list of Part::GeomBSplineCurve objects.
    """
    import FreeCAD
    import numpy as np
    import Part
    curves = []
    n_points = len(points)
    current_start = 0

    print(f"fit bspline to geom : points {len(points)}")
    while current_start < n_points:
        # Try fitting a curve to all remaining points
        remaining_points = points[current_start:]

        if len(remaining_points) < 4:
            #raise ValueError("Not enough points to fit a B-spline.")
            print(f"Not enough points to fit a B-spline.")
            return create_line_segments_from_vectors(remaining_points)

        # Fit a B-spline using FreeCAD's Part.BSplineCurve
        spline = Part.BSplineCurve()
        #spline.interpolate(remaining_points.tolist())
        spline.approximate(Points = remaining_points.tolist(), 
            DegMin=3,
            DegMax=5,       # DegMax=8
            Tolerance = 1e-4,
            ParamType="Centripetal",
            Continuity = 'C0',  #C0 point, C1 tangent, C2 Curvature, C3 rate of C
            #LengthWeight =
            #CurvatureWeight =
            #TorsiorWeight
            )

        # Convert spline to a shape for distance calculations
        spline_shape = spline.toShape()

        # Evaluate the error
        errors = []
        for pt in remaining_points:
            vertex = Part.Vertex(FreeCAD.Vector(*pt))  # Create a vertex for the point
            distance = spline_shape.distToShape(vertex)[0]
            errors.append(distance)
        mean_error = np.mean(errors)

        if mean_error > max_error:
            print(f"Mean Error {mean_error} > Max Error {max_error}") 
            # Split and retry if error exceeds max_error
            split_index = len(remaining_points) // 2
            segment = remaining_points[:split_index]
            spline_segment = Part.BSplineCurve()
            #spline_segment.interpolate(segment.tolist())
            spline_segment.approximate(Points = segment.tolist(), DegMin=3)
            curves.append(spline_segment)

            current_start += split_index
        else:
            # Acceptable fit, finalize this curve
            curves.append(spline)
            break

    return curves

def fit_bspline_to_geom_scipy(points, tolerance, max_error):
    print(f"fit_bspline_to_geom_scipy")

def scripy_fit_bspline(points, num_points_per_curve=100, max_error=1e-3):
    """
    Fit a set of points to one or more B-spline curves dynamically.

    Parameters:
               points (np.ndarray): Array of shape (n, 2) with points to fit.
        num_points_per_curve (int): Number of points to sample on each B-spline.
        max_error (float): Maximum allowed error for curve fitting.

    Returns:
        curves (list): A list of fitted curves, each containing sampled points.
    """
    from scipy.interpolate import splprep, splev
    import numpy as np
    curves = []
    n_points = len(points)
    current_start = 0

    while current_start < n_points:
        # Try fitting a curve to all remaining points
        remaining_points = points[current_start:]

        # Fit a B-spline to the remaining points
        tck, u = splprep(remaining_points.T, s=0)  # s=0 for interpolating the points
        fitted_points = np.array(splev(u, tck)).T

        # Calculate error
        error = np.linalg.norm(remaining_points - fitted_points, axis=1).mean()

        if error > max_error:
            # If error exceeds max_error, split the segment and refit
            split_index = len(remaining_points) // 2
            segment = remaining_points[:split_index]

            tck_segment, u_segment = splprep(segment.T, s=0)
            sampled_points = np.array(splev(np.linspace(0, 1, num_points_per_curve), tck_segment)).T
            curves.append(sampled_points)

            # Move the start point for next curve
            current_start += split_index

        else:
            # If error is acceptable, finalize the current curve
            sampled_points = np.array(splev(np.linspace(0, 1, num_points_per_curve), tck)).T
            curves.append(sampled_points)
            break

    return curves

def geomdl_bspline_to_Part_BSplineCurve(curve):
    """
    Convert geomdl BSpline to Part_BSPline
    """
    # Extract control points (poles) and weights
    poles = curve.ctrlpts  # Control points
    weights = curve.weights  # Weights
    print(f"weights {weights}")
    #if weights is None:         # non rational
    #    #weights = 1.0
    #    weights = 1
    #    #weights = [1] * len(poles)
    knots = curve.knotvector  # Knot vector
    print(f"knots {len(knots)}")
    print(f"Start knots {knots[:4]} End knots {knots[-4:]}")
    degree = curve.degree     # Curve degree
    print(f"degree {degree}")
    start_point = curve.evaluate_single(0.0)
    end_point = curve.evaluate_single(1.0)
    is_closed = start_point == end_point

    print(f"len knots {len(knots)}")
    print(f"check {len(poles) + degree + 1}")

    # Convert poles to FreeCAD Vectors
    poles_fc = [FreeCAD.Vector(pt[0], pt[1], 0) for pt in poles]
    print(f"FC poles {len(poles_fc)}")

    # Compute Multiplicities
    #internal_mults = [1] * (len(knots) - 2 * (degree + 1))
    #start_mults = [3] * (degree + 1)
    #end_mults = [3] * (degree + 1)
    #mults = [degree + 1] + [1] * internal_mults + [degree + 1]
    #mults = start_mults + internal_mults + end_mults
    mults = [1] * len(poles)
    print(f"FC mults {len(mults)} sum {sum(mults)}")
    print(f" mults first {mults[:4]} last {mults[-4:]}")

    # Create a BSpline geometry using poles, knots, weights, and degree
    bspline = Part.BSplineCurve()
    # Build the curve from the poles, multiplicities, knots, and degree
    #bspline_fc.buildFromPolesMultsKnots(poles=poles_fc, multiplicities=multiplicities_fc,
    #                                knots=knots_geomdl, degree=degree_geomdl)
    if weights is None:     # Non Rational
        print(f"lens mults {len(mults)} sum {sum(mults)} poles {len(poles_fc)}")
        #bspline.buildFromPolesMultsKnots(
        #        poles_fc,       # Poles (Control points)
        #        mults,          # Multiplicities
        #        knots,          # knot vector
        #        False,          #is_closed,      # Open {False} or Close {True}
        #        degree,         # Degree
        #        )
        bspline.buildFromPoles(
            poles_fc
            )
    else:
        bspline.buildFromPolesMultsKnots(
                poles_fc,       # Poles (Control points)
                mults,          # Multiplicities
                knots,          # knot vector
                is_closed,      # Open {False} or Close {True}
                #degree,        # Degree
                weights         # Weights
                )
    return bspline

def fit_bspline_to_geom_geomdl(points, tolerance, max_error):
    """
    BSpline fit using geomdl library
    """
    from geomdl import fitting
    print(f"fit_bspline_to_geom_geomdl")
    print(points[1:3])
    # Convert to list of tuples
    tuple_list = [tuple(point) for point in points]

    try:
        curve = fitting.approximate_curve(tuple_list, 3)

    except ValueError as e:
        print(f"Error: {e}")

    is_rational = curve.rational
    if is_rational:
        print("The curve is Rational (NURBS).")
    else:
        print("The curve is Non-Rational (B-Spline).")    

    bspline = geomdl_bspline_to_Part_BSplineCurve(curve)     
    return bspline

