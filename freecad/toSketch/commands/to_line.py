# to_line.py
import FreeCAD
import FreeCADGui
from PySide import QtCore
import Part
from freecad.toSketch import vector_utils  # central vector helper

class ToLineFeature:
    """
    Convert selected sketch geometry into straight lines or line-fitted segments.
    """

    def Activated(self):
        selection = FreeCADGui.Selection.getSelection()
        if not selection:
            print("No sketch selected.")
            return

        for obj in selection:
            if obj.TypeId != 'Sketcher::SketchObject':
                print(f"{obj.Label} is not a Sketch.")
                continue

            new_sketch = FreeCAD.ActiveDocument.addObject(
                "Sketcher::SketchObject",
                f"{obj.Label}_LineFit"
            )
            new_sketch.Placement = obj.Placement

            vectors = []
            last_point = None

            for geom in obj.Geometry:
                if geom.TypeId == 'Part::GeomLineSegment':
                    start = geom.StartPoint
                    end = geom.EndPoint

                    if last_point is None:
                        vectors.append(start)
                        last_point = end
                    else:
                        if vector_utils.is_contiguous(last_point, start):
                            vectors.append(end)
                            last_point = end
                        else:
                            self._flush_vectors(new_sketch, vectors)
                            vectors = [start, end]
                            last_point = end

                elif geom.TypeId == 'Part::GeomArcOfCircle':
                    # Flush any accumulated vectors before adding arc
                    self._flush_vectors(new_sketch, vectors)
                    vectors = []
                    new_sketch.addGeometry(geom)
                else:
                    print(f"Skipping unsupported geometry: {geom.TypeId}")

            # Flush any remaining vectors
            self._flush_vectors(new_sketch, vectors)
            new_sketch.recompute()
            print(f"Line-fitted sketch created: {new_sketch.Label}")

    def _flush_vectors(self, sketch, vectors):
        if len(vectors) < 2:
            return
        for i in range(len(vectors) - 1):
            sketch.addGeometry(Part.LineSegment(vectors[i], vectors[i + 1]))

    def IsActive(self):
        return FreeCAD.ActiveDocument is not None

    def GetResources(self):
        return {
            'Pixmap': 'toLine',
            'MenuText': QtCore.QT_TRANSLATE_NOOP('ToLineFeature', 'Convert to Lines'),
            'ToolTip': QtCore.QT_TRANSLATE_NOOP('ToLineFeature', 'Convert selected sketch geometry into straight lines'),
        }

# Register the command
FreeCADGui.addCommand('toLineCommand', ToLineFeature())

