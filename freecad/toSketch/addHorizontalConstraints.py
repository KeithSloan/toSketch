import FreeCAD as App, FreeCADGui as Gui
import Sketcher, Part

def add_horizontal_constraints(sketch, tol=1e-6):
    """
    Scan the given Sketch for all horizontal lines
    and add Horizontal constraints to any not already constrained.

    Parameters:
        sketch (Sketcher::SketchObject)
        tol (float): tolerance for detecting horizontality
    """
    doc = App.ActiveDocument
    geom = sketch.Geometry
    cons = sketch.Constraints

    # --------------------------------------------------------
    # Step 1: collect existing horizontal constraints
    # --------------------------------------------------------
    already_constrained = set()
    for c in cons:
        if c.Type == 'Horizontal':
            already_constrained.add(c.Geometry1)

    # --------------------------------------------------------
    # Step 2: find horizontal lines
    # --------------------------------------------------------
    added = 0
    for i, g in enumerate(geom):
        if not isinstance(g, Part.LineSegment):
            continue
        dx = g.EndPoint.x - g.StartPoint.x
        dy = g.EndPoint.y - g.StartPoint.y
        if abs(dy) <= tol and abs(dx) > tol:  # horizontal
            if i not in already_constrained:
                sketch.addConstraint(Sketcher.Constraint('Horizontal', i))
                added += 1

    doc.recompute()
    print(f"Added {added} Horizontal constraints.")
    return added
