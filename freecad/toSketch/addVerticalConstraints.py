# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileNotice: Part of the ToSketch addon.

import FreeCAD as App
import Sketcher
import Part
import math

def add_vertical_constraints(sketch, angle_tolerance_deg=0.5):
    """
    Add Vertical constraints to nearly vertical line segments
    in a Sketch that do not already have one.
    """
    if sketch is None or sketch.TypeId != 'Sketcher::SketchObject':
        raise ValueError("❌ Must pass a valid Sketcher::SketchObject")

    geo_list = sketch.Geometry
    constraints = sketch.Constraints

    # Find which geometry indices already have a Vertical constraint
    has_vertical = set()
    for c in constraints:
        if c.Type == 'Vertical' and hasattr(c, 'First'):
            has_vertical.add(c.First)

    added = 0
    tolerance_rad = math.radians(angle_tolerance_deg)

    for i, geo in enumerate(geo_list):
        if not isinstance(geo, Part.LineSegment):
            continue

        if i in has_vertical:
            continue  # Already vertical

        # Compute line vector
        dx = geo.EndPoint.x - geo.StartPoint.x
        dy = geo.EndPoint.y - geo.StartPoint.y
        length = math.hypot(dx, dy)
        if length == 0:
            continue

        # Compute angle from X-axis (π/2 for vertical)
        angle = abs(math.atan2(dy, dx))
        if abs(angle - math.pi/2) < tolerance_rad:
            sketch.addConstraint(Sketcher.Constraint('Vertical', i))
            print(f"✅ Added Vertical constraint to line {i}")
