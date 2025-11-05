import FreeCAD as App
import Sketcher
import Part

def add_vertical_constraints(sketch, tol=1e-6):
    """
    Scan the given Sketch for all vertical lines
    and add Vertical constraints to any not already constrained.

    Parameters:
        sketch (Sketcher::SketchObject)
        tol (float): tolerance for detecting verticality
    """
    doc = App.ActiveDocument
    geom = sketch.Geometry
    cons = sketch.Constraints

    # --------------------------------------------------------
    # Step 1: collect existing horizontal constraints
    # --------------------------------------------------------
    already_constrained = set()
    for c in cons:
        if c.Type == 'Vertical':
            already_constrained.add(c.Geometry1)

    # --------------------------------------------------------
    # Step 2: find Verticak lines
    # --------------------------------------------------------
    added = 0
    for i, g in enumerate(geom):
        if not isinstance(g, Part.LineSegment):
            continue
        dx = g.EndPoint.x - g.StartPoint.x
        dy = g.EndPoint.y - g.StartPoint.y
        if abs(dx) <= tol and abs(dy) > tol:  # Vertical
            if i not in already_constrained:
                sketch.addConstraint(Sketcher.Constraint('Vertical', i))
                added += 1

    doc.recompute()
    print(f"Added {added} Vertical constraints.")
    return added
