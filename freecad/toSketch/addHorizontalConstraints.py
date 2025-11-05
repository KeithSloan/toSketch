import FreeCAD as App
import Sketcher
import Part
import math

def add_horizontal_constraints(sketch, angle_tolerance_deg=0.5):
    """
    Add Horizontal constraints to nearly horizontal line segments
    in a Sketch that do not already have one.
    """
    if sketch is None or sketch.TypeId != 'Sketcher::SketchObject':
        raise ValueError("❌ Must pass a valid Sketcher::SketchObject")

    geo_list = sketch.Geometry
    constraints = sketch.Constraints

    # Find which geometry indices already have a Horizontal constraint
    has_horizontal = set()
    for c in constraints:
        if c.Type == 'Horizontal' and hasattr(c, 'First'):
            has_horizontal.add(c.First)

    added = 0
    tolerance_rad = math.radians(angle_tolerance_deg)

    for i, geo in enumerate(geo_list):
        if not isinstance(geo, Part.LineSegment):
            continue

        if i in has_horizontal:
            continue  # Already horizontal

        # Compute line vector
        dx = geo.EndPoint.x - geo.StartPoint.x
        dy = geo.EndPoint.y - geo.StartPoint.y
        length = math.hypot(dx, dy)
        if length == 0:
            continue

        # Compute angle to X-axis
        angle = abs(math.atan2(dy, dx))
        if angle < tolerance_rad or abs(angle - math.pi) < tolerance_rad:
            sketch.addConstraint(Sketcher.Constraint('Horizontal', i))
            print(f"✅ Added Horizontal constraint to line {i}")
            added += 1
        else:
            print(f"Line {i} not horizontal (angle={math.degrees(angle):.2f}°)")

    if added == 0:
        print("ℹ️  No new horizontal constraints added.")
    else:
        print(f"✅ {added} horizontal constraint(s) added.")

    App.ActiveDocument.recompute()
