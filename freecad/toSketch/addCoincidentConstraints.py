import FreeCAD as App
import Sketcher
import Part
import math

def add_coincident_constraints(sketch, tolerance=1e-5):
    """
    Scan a Sketch and add Coincident constraints between geometry endpoints
    that are at the same position (within tolerance) and not already constrained.
    """
    if sketch is None or sketch.TypeId != 'Sketcher::SketchObject':
        raise ValueError("❌ Must pass a valid Sketcher::SketchObject")

    geo_list = sketch.Geometry
    constraints = sketch.Constraints

    # Build a set of existing coincidence relationships
    existing_pairs = set()
    for c in constraints:
        if c.Type == 'Coincident' and hasattr(c, 'First') and hasattr(c, 'Second'):
            key = tuple(sorted([(c.First, c.FirstPos), (c.Second, c.SecondPos)]))
            existing_pairs.add(key)

    added = 0

    # Collect all endpoints: (GeoIndex, PosIndex, Point)
    # PosIndex = 1 for StartPoint, 2 for EndPoint (FreeCAD convention)
    endpoints = []
    for i, geo in enumerate(geo_list):
        if hasattr(geo, "StartPoint") and hasattr(geo, "EndPoint"):
            endpoints.append((i, 1, geo.StartPoint))
            endpoints.append((i, 2, geo.EndPoint))
        elif hasattr(geo, "Center"):
            # For circles/arcs, optionally include center if useful
            endpoints.append((i, 3, geo.Center))

    # Compare all endpoint pairs
    for a in range(len(endpoints)):
        geo1, pos1, p1 = endpoints[a]
        for b in range(a + 1, len(endpoints)):
            geo2, pos2, p2 = endpoints[b]
            if geo1 == geo2:
                continue  # same geometry element

            if p1.distanceToPoint(p2) <= tolerance:
                key = tuple(sorted([(geo1, pos1), (geo2, pos2)]))
                if key not in existing_pairs:
                    sketch.addConstraint(
                        Sketcher.Constraint('Coincident', geo1, pos1, geo2, pos2)
                    )
                    existing_pairs.add(key)
                    added += 1
                    print(f"✅ Added Coincident constraint between Geo {geo1}.{pos1} and Geo {geo2}.{pos2}")

    if added == 0:
        print("ℹ️  No new coincident constraints added.")
    else:
        print(f"✅ {added} coincident constraint(s) added.")

    App.ActiveDocument.recompute()
