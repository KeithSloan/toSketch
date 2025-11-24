# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileNotice: Part of the ToSketch addon.

import FreeCAD
import math
import Sketcher
import Part

def add_parallel_constraints(sketch):


    """
    Scan a FreeCAD Sketch and add Parallel constraints between pairs of lines
    only if there are no existing constraints involving those two elements.
    """
    if not sketch:
        print("No sketch provided")
        return
    
    geo_list = sketch.Geometry
    constraints = sketch.Constraints

    # Helper to check if a constraint involves a given pair of GeoIds
    def constraint_involves(geo_id1, geo_id2):
        for c in constraints:
            if hasattr(c, 'First') and hasattr(c, 'Second'):
                pair = {c.First, c.Second}
                if geo_id1 in pair and geo_id2 in pair:
                    return True
        return False

    # Scan all pairs of lines
    for i, g1 in enumerate(geo_list):
        if not isinstance(g1, (Part.LineSegment,)):
            continue
        for j, g2 in enumerate(geo_list):
            if j <= i:
                continue
            if not isinstance(g2, (Part.LineSegment,)):
                continue

            # Check if already parallel or involved
            if constraint_involves(i, j):
                continue

            # Check if geometrically parallel (within tolerance)
            v1 = g1.EndPoint.sub(g1.StartPoint)
            v2 = g2.EndPoint.sub(g2.StartPoint)
            if abs(v1.getAngle(v2)) < 1e-3 or abs(abs(v1.getAngle(v2)) - math.pi) < 1e-3:
                # Add constraint
                sketch.addConstraint(Sketcher.Constraint('Parallel', i, j))
                print(f"Added Parallel constraint between Geo {i} and Geo {j}")

    FreeCAD.ActiveDocument.recompute()
