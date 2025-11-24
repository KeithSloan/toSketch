# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileNotice: Part of the ToSketch addon.

import FreeCAD as App, Sketcher
from FreeCAD import Vector
import math

import FreeCAD as App
import Sketcher
import Part
from FreeCAD import Vector

def add_symmetric_constraints(sketch, tol=1e-5):
    """
    Automatically detect and add symmetry constraints in a FreeCAD Sketch.
    Works for symmetry about the X-axis, Y-axis, or any construction line.
    Supports lines, arcs/circles, and points (Part.Point).
    """

    geom = sketch.Geometry
    used_pairs = set()

    # ---------------------------------------------------------------
    # Helper functions
    # ---------------------------------------------------------------
    def almost_equal(a, b):
        return abs(a - b) < tol

    def is_mirror_point(p, q, axis_origin, axis_dir):
        """Return True if q is the mirror of p about an axis."""
        ap = p - axis_origin
        axis_dir_n = axis_dir.normalize()
        proj_len = ap.dot(axis_dir_n)
        proj = axis_origin + axis_dir_n * proj_len
        mirror = proj - (p - proj)
        return (mirror - q).Length < tol

    def get_axis_defs():
        """Return list of (index, origin, direction, label)."""
        axes = [
            (-1, Vector(0, 0, 0), Vector(0, 1, 0), "Y-axis"),
            (-2, Vector(0, 0, 0), Vector(1, 0, 0), "X-axis")
        ]
        for i, g in enumerate(geom):
            # construction line can also be symmetry axis
            if hasattr(g, "StartPoint") and getattr(g, "Construction", False):
                origin = g.StartPoint
                direction = (g.EndPoint - g.StartPoint).normalize()
                axes.append((i, origin, direction, f"line {i}"))
        return axes

    axes = get_axis_defs()

    # ---------------------------------------------------------------
    # Compare all geometry pairs
    # ---------------------------------------------------------------
    for i, g1 in enumerate(geom):
        for j, g2 in enumerate(geom):
            if j <= i or (i, j) in used_pairs:
                continue
            if type(g1) != type(g2):
                continue

            for axis_idx, axis_origin, axis_dir, axis_label in axes:
                # --- Handle lines ---
                if isinstance(g1, Part.LineSegment):
                    a1, b1 = g1.StartPoint, g1.EndPoint
                    a2, b2 = g2.StartPoint, g2.EndPoint
                    if (is_mirror_point(a1, a2, axis_origin, axis_dir) and
                        is_mirror_point(b1, b2, axis_origin, axis_dir)):
                        print(f"Lines {i} and {j} symmetric about {axis_label}")
                        sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 1, j, 1, axis_idx))
                        sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 2, j, 2, axis_idx))
                        used_pairs.add((i, j))
                        break

                # --- Handle arcs and circles ---
                elif isinstance(g1, (Part.ArcOfCircle, Part.Circle)):
                    c1, c2 = g1.Center, g2.Center
                    if (is_mirror_point(c1, c2, axis_origin, axis_dir)
                        and almost_equal(g1.Radius, g2.Radius)):
                        print(f"Arcs/Circles {i} and {j} symmetric about {axis_label}")
                        sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 3, j, 3, axis_idx))
                        used_pairs.add((i, j))
                        break

                # --- Handle points ---
                elif isinstance(g1, Part.Point):
                    p1, p2 = g1.XYZ, g2.XYZ
                    if is_mirror_point(p1, p2, axis_origin, axis_dir):
                        print(f"Points {i} and {j} symmetric about {axis_label}")
                        sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 1, j, 1, axis_idx))
                        used_pairs.add((i, j))
                        break

    App.ActiveDocument.recompute()
    print("✅ Symmetric constraints added where detected.")

#import FreeCAD as App, FreeCADGui as Gui, Sketcher
#from FreeCAD import Vector
#import math

import FreeCADGui as Gui

def detect_and_preview_symmetric_constraints(sketch, tol=1e-5):
    doc = App.ActiveDocument
    view = Gui.ActiveDocument.ActiveView

    geom = sketch.Geometry
    used_pairs = set()
    candidate_pairs = []   # store tuples (i, j, axis_idx)

    def almost_equal(a, b): return abs(a - b) < tol

    def is_mirror_point(p, q, origin, dir):
        ap = p - origin
        d = dir.normalize()
        proj = origin + d * ap.dot(d)
        mirror = proj - (p - proj)
        return (mirror - q).Length < tol

    def get_axes():
        axes = [(-1, Vector(0,0,0), Vector(0,1,0), "Y-axis"),
                (-2, Vector(0,0,0), Vector(1,0,0), "X-axis")]
        for i,g in enumerate(geom):
            if hasattr(g,"StartPoint") and getattr(g,"Construction",False):
                axes.append((i,g.StartPoint,(g.EndPoint-g.StartPoint).normalize(),f"line {i}"))
        return axes

    axes = get_axes()

    # -------- find symmetry pairs --------
    for i,g1 in enumerate(geom):
        for j,g2 in enumerate(geom):
            if j<=i or (i,j) in used_pairs or type(g1)!=type(g2): continue
            for axis_idx, origin, direction, axis_label in axes:
                if hasattr(g1,"StartPoint") and hasattr(g2,"StartPoint"):
                    a1,b1,a2,b2 = g1.StartPoint,g1.EndPoint,g2.StartPoint,g2.EndPoint
                    if (is_mirror_point(a1,a2,origin,direction) and
                        is_mirror_point(b1,b2,origin,direction)):
                        candidate_pairs.append((i,j,axis_idx))
                        used_pairs.add((i,j))
                        break
                elif hasattr(g1,"Center") and hasattr(g2,"Center"):
                    if (is_mirror_point(g1.Center,g2.Center,origin,direction)
                        and almost_equal(g1.Radius,g2.Radius)):
                        candidate_pairs.append((i,j,axis_idx))
                        used_pairs.add((i,j))
                        break

    if not candidate_pairs:
        Gui.showMainWindow()
        App.Console.PrintMessage("No symmetric pairs detected.\n")
        return

    # -------- highlight candidate pairs --------
    temp_objs = []
    for i,j,axis_idx in candidate_pairs:
        for idx,color in [(i,(1.0,0.0,0.0)),(j,(0.0,1.0,0.0))]:
            g = geom[idx]
            shape = g.toShape()
            obj = doc.addObject("Part::Feature","SymPreview")
            obj.Shape = shape
            view_color = (color[0],color[1],color[2],0.5)
            obj.ViewObject.LineColor = view_color[:3]
            obj.ViewObject.Transparency = 70
            obj.ViewObject.DisplayMode = "Wireframe"
            temp_objs.append(obj)
    doc.recompute()

    # -------- confirmation dialog --------
    from PySide import QtWidgets
    msg = f"Detected {len(candidate_pairs)} symmetric pairs.\nApply constraints?"
    reply = QtWidgets.QMessageBox.question(None, "Add Symmetry Constraints",
                                           msg,
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    if reply == QtWidgets.QMessageBox.Yes:
        for i,j,axis_idx in candidate_pairs:
            if hasattr(geom[i],"StartPoint"):
                sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 1, j, 1, axis_idx))
                sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 2, j, 2, axis_idx))
            elif hasattr(geom[i],"Center"):
                sketch.addConstraint(Sketcher.Constraint('Symmetric', i, 3, j, 3, axis_idx))
        App.Console.PrintMessage(f"✅ Added {len(candidate_pairs)} symmetry constraints.\n")
        App.ActiveDocument.recompute()
    else:
        App.Console.PrintMessage("Cancelled — no constraints added.\n")

    # -------- cleanup highlights --------
    for obj in temp_objs:
        doc.removeObject(obj.Name)
    doc.recompute()

