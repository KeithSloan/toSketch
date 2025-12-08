import FreeCAD, Part
import math

EPS_COINCIDENT = 1e-3
EPS_COLLINEAR  = 1e-4


def is_collinear(l1, l2, tol=EPS_COLLINEAR):
    d1 = l1.EndPoint - l1.StartPoint
    d2 = l2.EndPoint - l2.StartPoint
    if d1.Length == 0 or d2.Length == 0:
        return False
    return abs(d1.normalize().dot(d2.normalize())) > (1.0 - tol)


def merge_connected_lines(lines):
    used = set()
    chains = []

    for i, ln in enumerate(lines):
        if i in used:
            continue

        chain = [ln]
        used.add(i)
        extended = True

        while extended:
            extended = False
            for j, ln2 in enumerate(lines):
                if j in used:
                    continue

                if not is_collinear(chain[-1], ln2):
                    continue

                if chain[-1].EndPoint.distanceToPoint(ln2.StartPoint) < EPS_COINCIDENT:
                    chain.append(ln2); used.add(j); extended = True; continue
                if chain[-1].EndPoint.distanceToPoint(ln2.EndPoint) < EPS_COINCIDENT:
                    chain.append(ln2); used.add(j); extended = True; continue

                if chain[0].StartPoint.distanceToPoint(ln2.EndPoint) < EPS_COINCIDENT:
                    chain.insert(0, ln2); used.add(j); extended = True; continue
                if chain[0].StartPoint.distanceToPoint(ln2.StartPoint) < EPS_COINCIDENT:
                    chain.insert(0, ln2); used.add(j); extended = True; continue

        chains.append(chain)

    return chains


def ordered_vertices(sketch):
    edges = []
    for geo in sketch.Geometry:
        if hasattr(geo, "StartPoint"):
            edges.append((geo.StartPoint, geo.EndPoint))

    if not edges:
        return []

    chain = [edges[0][0], edges[0][1]]
    edges.pop(0)

    while edges:
        last = chain[-1]
        found = False

        for i, (a, b) in enumerate(edges):
            if last.distanceToPoint(a) < EPS_COINCIDENT:
                chain.append(b); edges.pop(i); found = True; break
            if last.distanceToPoint(b) < EPS_COINCIDENT:
                chain.append(a); edges.pop(i); found = True; break

        if not found:
            break

    return chain

