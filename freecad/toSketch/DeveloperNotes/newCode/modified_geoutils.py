# geomutils.py
# Complete replacement module for FreeCAD Workbench utilities
# Provides geometric helpers, logging, and safe shape validation.

import FreeCAD
import Part
import math
import logging

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
logger = logging.getLogger("toSketch.geomutils")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# ---------------------------------------------------------------------------
# Shape Checking Helpers
# ---------------------------------------------------------------------------

def ensure_shape(obj):
    """
    Ensures obj is a valid FreeCAD shape. If obj is a DocumentObject,
    checks obj.Shape, recomputing if needed. If obj is a Part.Shape,
    returns it directly.
    """
    if isinstance(obj, Part.Shape):
        if obj.isNull():
            logger.error("Provided Part.Shape is null.")
        return obj

    if hasattr(obj, "Shape"):
        try:
            if obj.Shape.isNull():
                logger.debug(f"Recomputing null shape for {obj.Name}")
                obj.recompute()
            return obj.Shape
        except Exception as e:
            logger.error(f"ensure_shape() failed: {e}")
    else:
        logger.error("Object has no Shape attribute")

    return None

# ---------------------------------------------------------------------------
# Vector Utilities
# ---------------------------------------------------------------------------

def v(x, y, z):
    """Short-hand FreeCAD vector"""
    return FreeCAD.Vector(x, y, z)


def vec_length(vec):
    return math.sqrt(vec.x**2 + vec.y**2 + vec.z**2)


def vec_normalize(vec):
    length = vec_length(vec)
    if length == 0:
        return FreeCAD.Vector(0,0,0)
    return vec.multiply(1.0/length)

# ---------------------------------------------------------------------------
# BREP Utility Functions
# ---------------------------------------------------------------------------

def fuse_shapes(shapes):
    """
    Fuse a list of Part.Shapes into one.
    Returns None if any shape fails.
    """
    good_shapes = []
    for s in shapes:
        ss = ensure_shape(s)
        if ss is None or ss.isNull():
            logger.error("Cannot fuse: null shape detected.")
            return None
        good_shapes.append(ss)

    try:
        result = good_shapes[0]
        for s in good_shapes[1:]:
            result = result.fuse(s)
        return result
    except Exception as e:
        logger.error(f"Fuse operation failed: {e}")
        return None


def common_shapes(a, b):
    sa = ensure_shape(a)
    sb = ensure_shape(b)
    if not sa or not sb:
        return None
    try:
        return sa.common(sb)
    except Exception as e:
        logger.error(f"Common failed: {e}")
        return None


def cut_shapes(a, b):
    sa = ensure_shape(a)
    sb = ensure_shape(b)
    if not sa or not sb:
        return None
    try:
        return sa.cut(sb)
    except Exception as e:
        logger.error(f"Cut failed: {e}")
        return None

# ---------------------------------------------------------------------------
# Hull / Minkowski Support Functions
# (Non-CGAL fallback for supported cases)
# ---------------------------------------------------------------------------

def can_simplify_hull(shapes):
    """
    Detects whether hull can be approximated by BREP logic.
    Placeholder: extend as needed.
    """
    if len(shapes) == 2:
        return True
    return False


def simple_hull(shapes):
    """Simplified hull for two shapes: convex hull of vertices."""
    if len(shapes) != 2:
        logger.error("simple_hull() expects exactly two shapes")
        return None

    s1 = ensure_shape(shapes[0])
    s2 = ensure_shape(shapes[1])
    if not s1 or not s2:
        return None

    verts = [v.Point for v in s1.Vertexes] + [v.Point for v in s2.Vertexes]
    if not verts:
        logger.error("simple_hull(): no vertices found")
        return None

    try:
        hull = Part.makeShell(Part.makePolygon(verts))
