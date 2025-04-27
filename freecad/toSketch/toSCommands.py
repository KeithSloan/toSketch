#**************************************************************************
#*                                                                        *
#*   Copyright (c) 2021 Keith Sloan <keith@sloan-home.co.uk>              *
#*                                                                        *
#*   This program is free software; you can redistribute it and/or modify *
#*   it under the terms of the GNU Lesser General Public License (LGPL)   *
#*   as published by the Free Software Foundation; either version 2 of    *
#*   the License, or (at your option) any later version.                  *
#*   for detail see the LICENCE text file.                                *
#*                                                                        *
#*   This program is distributed in the hope that it will be useful,      *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
#*   GNU Library General Public License for more details.                 *
#*                                                                        *
#*   You should have received a copy of the GNU Library General Public    *
#*   License along with this program; if not, write to the Free Software  *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
#*   USA                                                                  *
#*                                                                        *
#*   Acknowledgements :                                                   *
#*                                                                        *
#**************************************************************************

__title__="FreeCAD Face2Sketch Workbench - GUI Commands"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

'''
This Script includes the GUI Commands of the 2S module
'''

import FreeCAD,FreeCADGui, Part, Sketcher, Show
from PySide import QtCore, QtWidgets

# Used by toSketch - for Section to Sketch
from .toSharedFunc import shapes2Sketch, angle_between_lines, vectors_to_numpy, fit_bspline_to_geom


class section2SketchFeature:

   def Activated(self):
        #   for obj in FreeCADGui.Selection.getSelection():
        selectEx = FreeCADGui.Selection.getSelectionEx()
        for sel in selectEx :
            print(f"Selected-Ex {sel.ObjectName} {sel.Object.TypeId}")
            if sel.Object.TypeId == "Mesh::Feature":
                shapes2Sketch(sel.Object.Mesh, sel.ObjectName+"Sketch")
            else:
                if hasattr(sel.Object, "Shape"):
                    shapes2Sketch(sel.Object.Shape, sel.ObjectName+"Sketch")


   def IsActive(self):
        if FreeCAD.ActiveDocument is None:
           return False
        else:
           return True

   def GetResources(self):
       return {'Pixmap'  : 'section2Sketch', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toSketchFeature',\
                'Section | Wire To Sketch'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSketchFeature',\
                'Section | Wire To Sketch')}


class toSketchDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # Set the dialog title
        self.setWindowTitle("Parameters")

        # Main vertical layout for the dialog
        main_layout = QtWidgets.QVBoxLayout()

        # Group box for Mesh Parameters
        group_box = QtWidgets.QGroupBox("Mesh Parameters")
        group_layout = QtWidgets.QVBoxLayout()  # Vertical layout for rows

        # Row 1: LinearDeflection
        linear_layout = QtWidgets.QHBoxLayout()
        linear_label = QtWidgets.QLabel("LinearDeflection:")
        self.linear_input = QtWidgets.QLineEdit("0.1")  # Initial value 0.1
        linear_layout.addWidget(linear_label)
        linear_layout.addWidget(self.linear_input)

        # Row 2: AngularDeflection
        angular_layout = QtWidgets.QHBoxLayout()
        angular_label = QtWidgets.QLabel("AngularDeflection:")
        self.angular_input = QtWidgets.QLineEdit("0.523599")  # Initial value 0.523599
        angular_layout.addWidget(angular_label)
        angular_layout.addWidget(self.angular_input)

        # Add rows to the vertical group layout
        group_layout.addLayout(linear_layout)
        group_layout.addLayout(angular_layout)

        # Set the group layout for the group box
        group_box.setLayout(group_layout)

        # Add the group box to the main dialog layout
        main_layout.addWidget(group_box)

        # Add OK and Cancel buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout.addWidget(button_box)

        # Set the main layout for the dialog
        self.setLayout(main_layout)

    def get_AngularDeflection(self):
        """

        Return the value for AngularDeflections.
        """
        return self.angular_input.text()

    def get_LinearDeflection(self):
        """
        Return the values for LinearDeflection

        """
        return self.linear_input.text()


class toSketchFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def buildTargetObjects(self, selection):
        objs = []
        excludeTypeIds = ['PartDesign::Plane','Part::Offset2D']
        print(f"buildTargetObjects {selection}")
        #print(dir(selection))
        for sel in selection:
            if hasattr(sel, 'Object'):
                obj = sel.Object
                if obj.TypeId not in excludeTypeIds:
                    if obj.TypeId == 'Part::FeaturePython':
                        if obj.Label[:7] != 'toPlane' and obj.Label[:5] != 'Plane':
                            objs.append(obj)
                    else:
                       objs.append(obj)

        return objs                        


    def Activated(self):
        #   for obj in FreeCADGui.Selection.getSelection():
        selectEx = FreeCADGui.Selection.getSelectionEx()
        for sel in selectEx :
            print(f"Selected-Ex {sel.ObjectName} {sel.TypeId}")
            #print(dir(sel))
            #print(sel.ObjectName)
            #print(sel.FullName)
            if sel.HasSubObjects:  # Not sure what this does?
               print('SubObjects')
               if hasattr(sel.SubObjects[0],'Surface') :
                  if str(sel.SubObjects[0].Surface) == '<Plane object>' :
                     print('Planar')
                     face = sel.SubObjects[0]
                     # move face to origin
                     face.translate(face.Placement.Base.negative())
                     sketch = self.toSketchShapes2Sketch([face],'Sketch'+sel.ObjectName)
                     # Pop the Plane parts of sketch
                     self.addConstraints(sketch)
                     #print(dir(sketch))
                     sketch.MapMode ='FlatFace'
                     sketch.MapReversed = False    # ????
                     #print(sketch.MapReversed)
                     #print('dir face')
                     #print(dir(face))
                     #print(face.TypeId)
                     #print(face.ShapeType)
                     #print(sel.FullName)
                     sketch.Support = [(sel.FullName[0],sel.FullName[1][0])]
                     nVector = face.normalAt(1,1)
                     pVector = face.findPlane().Position
                     dVector = nVector.multiply(nVector.dot(pVector))
                     sketch.Placement.move(dVector) 
                     #pl = FreeCAD.Placement()
                     #print(dir(sketch.AttachmentOffset))
                     #sketch.AttachmentOffset.Base = pl.Base
                     #sketch.AttachmentOffset.Rotation = pl.Rotation

        objs = self.buildTargetObjects(selectEx)
        print(f"Target Objs {objs}")
        for sel in FreeCADGui.Selection.getSelection():
            # Look for Plane to pass to ActionSection
            # which will loop through all Objects to section
            print(f"Selected {sel.Name} {sel.TypeId}")
            #print(dir(sel))
            if sel.TypeId == 'PartDesign::Plane' :
               #print(dir(sel))
               #print(dir(sel.Shape))
               sketch = self.actionSectionDialog(sel.Shape, objs)
               nVector = sel.Shape.Faces[0].normalAt(1,1)
               pVector = sel.Placement.Base
               dVector = nVector.multiply(nVector.dot(pVector))
               sketch.Placement.move(dVector)
            elif sel.TypeId == 'Part::FeaturePython' and \
                    (sel.Label[:7] == 'toPlane' or \
                    sel.Label[:5] == "Plane"):
               print(f"Part FeaturePython Plane")
               sketch = self.actionSectionDialog(sel.Shape, objs)
            elif sel.TypeId == 'Part::Plane' :
                print(f"Part Plane")
                self.actionSectionDialog(sel, objs)
            #elif sel.TypeId == 'Part::Feature' :
            #   sketch = self.shapes2Sketch(sel.Shape,'Sketch')

            elif sel.TypeId == 'Part::Offset2D':
                print(f"Part::Offset2D")
                sketch = self.toSketchShapes2Sketch(sel.Shape,'Sketch')

            #elif sel.TypeId == 'Mesh::Feature':
            #    print(f"Mesh Feature")
            #    print(dir(sel.Mesh))
            #    sketch = self.shapes2Sketch(sel.Mesh.Shape,'Sketch')

            #print(sel.ViewObject.Visibility)
            #sel.ViewObject.Visibility = False

        try :
            FreeCADGui.ActiveDocument.setEdit(sketch,0)
        except :
            pass


    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toSketch', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toSketchFeature',\
                'To Sketch'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSketchFeature',\
                'To Sketch')}

    def actionSectionDialog(self, plane, objs):
        print(f'Action Section Dialog')
        dialog = toSketchDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            linearDeflection = dialog.get_LinearDeflection()
            angularDeflection = dialog.get_AngularDeflection()
            return self.actionSection(plane, objs, linearDeflection, angularDeflection)
                

    def actionSection(self, plane, objs, linearDef, angularDef):
        print(f'Action Section {objs}')
        edges = []
        # If no target Objs - Use all Objects
        if len(objs) == 0:
            objs = FreeCAD.ActiveDocument.Objects

        for obj in objs :
            sect = None
            #print(obj.Label)
            #print(obj.TypeId)
            if hasattr(obj,'Mesh') :
                print(f"Meshed Object {obj.Label}")
                import Draft, MeshPart, Part
                shpPlane = MeshPart.meshFromShape(
                    plane,
                    float(linearDef),
                    AngularDeflection=float(angularDef),
                    Relative=False
                    )
                for edge in obj.Mesh.section(shpPlane):
                    #print(f"edge {edge}")
                    #print(dir(edge))
                    wire = Part.makePolygon(edge)
                    edges.append(Part.Shape(wire))

            if hasattr(obj,'Shape') and \
                  obj.TypeId != 'Sketcher::SketchObject' and \
                  obj.TypeId != 'PartDesign::Body' : # Otherwise Body & Content
               if obj.Shape.Volume > 0 :
                  print(obj.Label+' : Has shape')
                  sect = obj.Shape.section(plane)
            if sect is not None:
               #print(sect)
               print(sect.ShapeType)
               if len(sect.SubShapes) > 0 :
                  print('Intersect : '+obj.Label)
                  print(len(sect.SubShapes))
                  for e in sect.SubShapes :
                         edges.append(e)
               obj.ViewObject.Visibility = False
               #print(dir(sect))
        if len(objs) == 1:
            name = "Sketch_"+objs[0].Label
        else:
            name = 'Sketch'
        sketch = self.toSketchShapes2Sketch(edges,name)
        #self.addConstraints(sketch)
        return sketch

    def addConstraints(self, sketch) :
        print('Add Constraints')
        geoList = sketch.Geometry
        Lines = []
        Arcs  = []
        Circles = []
        for i in range(sketch.GeometryCount):
            if geoList[i].TypeId == 'Part::GeomLineSegment':
               Lines.append([i,geoList[i]])
            elif geoList[i].TypeId == 'Part::GeomArcOfCircle':
               Arcs .append([i,geoList[i]])
            elif geoList[i].TypeId == 'Part::GeomCircle':
               Circles.append([i,geoList[i]])
        print('Sketch has ',len(Lines)+len(Arcs)+len(Circles), \
                ' entities of which:')
        print(len(Lines),'--> LineSegment')
        print(len(Circles),'--> Circle')
        print(len(Arcs),'--> ArcOfCircle')
        for i in range(len(Circles)):
            print(Circles[i])
            print('Circle radius: ',Circles[i][1].Radius)
            sketch.addConstraint(Sketcher.Constraint('Radius', \
                 Circles[i][0],Circles[i][1].Radius))
        #sketch.addConstraint(Sketcher.Constraint('Point',10,10,10))

    def toSketchShapes2Sketch(self, shapes, name) :
        print(f'shapes2sketch {name}{len(shapes)}')
        if len(shapes) > 0:
            # Use shared function
            shapes2Sketch(shapes, name, auto=False)
        else:
            print(f"No shapes for sketch")


class removeOuterBoxFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        for sel in FreeCADGui.Selection.getSelection():
            print(f"Selected {sel.Name} {sel.TypeId}")
            #print(dir(sel))
            print(sel.TypeId)
            if sel.TypeId == "Sketcher::SketchObject":
                self.removeOuterBox(sel)

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
           return False
        else:
           return True
          
    def removeOuterBox(self, sketch):
        decPlace = 4
        sketch.recompute()
        print(sketch.GeometryCount)
        print(f"Remove Outer {sketch.GeometryCount}")
        print(f"BoundingBox {sketch.Shape.BoundBox}")
        print(dir(sketch.Shape.BoundBox))
        xMin = round(sketch.Shape.BoundBox.XMin, decPlace)
        xMax = round(sketch.Shape.BoundBox.XMax, decPlace)
        yMin = round(sketch.Shape.BoundBox.YMin, decPlace)
        yMax = round(sketch.Shape.BoundBox.YMax, decPlace)
        boundBox = [(xMin, yMin), (xMin, yMax), (xMax, yMin), (xMax, yMax)]
        print(f"Boundbox {boundBox}")
        delList = []
        for i, g in enumerate(sketch.Geometry):
            if g.TypeId == "Part::GeomLineSegment":
                 print(g.StartPoint)
                 print(g.EndPoint)
                 start = (round(g.StartPoint.x, decPlace), \
                        round(g.StartPoint.y, decPlace))
                 end = (round(g.EndPoint.x, decPlace), \
                        round(g.EndPoint.y, decPlace))
                 print(f"line {start} {end}")
                 if start in boundBox and end in boundBox :
                    print(f"Found {i} {g}")
                    #sketch.delGeometry(i)
                    delList.append(i)
        print(delList)
        if len(delList) > 0:
            for i in reversed(delList):
                sketch.delGeometry(i)
        sketch.recompute()        
        print(f"After Remove {sketch.GeometryCount}")
        print(sketch.GeometryCount)
        FreeCADGui.ActiveDocument.setEdit(sketch,0)


    def GetResources(self):
        return {'Pixmap'  : 'removeOuterBox', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('removeOuterBoxFeature',\
                'Remove outer Box of Sketch'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('removeOuterBoxFeature',\
                'Remove outer Box of Sketch')}


class addBboxFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        for sel in FreeCADGui.Selection.getSelection():
            print(f"Selected {sel.Name} {sel.TypeId}")
            print(dir(sel))
            print(sel.TypeId)
            sketch = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", "BboxSketch")
            self.createBboxSketch(sketch, sel)



    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
           return False
        else:
           return True

    def createBboxSketch(self, sketch, obj):
        decPlace = 4
        #print(dir(sketch.Shape.BoundBox))
        xMin = round(obj.Shape.BoundBox.XMin, decPlace)
        xMax = round(obj.Shape.BoundBox.XMax, decPlace)
        xLength = round(obj.Shape.BoundBox.XLength, decPlace)
        xMax = round(obj.Shape.BoundBox.XMax, decPlace)
        yMin = round(obj.Shape.BoundBox.YMin, decPlace)
        yMax = round(obj.Shape.BoundBox.YMax, decPlace)
        yLength = round(obj.Shape.BoundBox.YLength, decPlace)
        boundBox = [(xMin, yMin), (xMin, yMax), (xMax, yMin), (xMax, yMax)]
        print(f"Boundbox {boundBox}")
        line = Part.LineSegment()
        line.StartPoint = (xMin, yMin, 0)
        line.EndPoint = (xMax, yMin, 0)
        sketch.addGeometry(line)
        line = Part.LineSegment()
        line.StartPoint = (xMax, yMin, 0)
        line.EndPoint = (xMax, yMax, 0)
        sketch.addGeometry(line)
        #line = Part.LineSegment()
        #line.StartPoint = (xMax, yMax, 0)
        #line.EndPoint = (xMax, yMin, 0)
        #sketch.addGeometry(line)
        line = Part.LineSegment()
        line.StartPoint = (xMax, yMax, 0)
        line.EndPoint = (xMin, yMax, 0)
        sketch.addGeometry(line)
        line = Part.LineSegment()
        line.StartPoint = (xMin, yMax, 0)
        line.EndPoint = (xMin, yMin, 0)
        sketch.addGeometry(line)
        sketch.addConstraint(
            Sketcher.Constraint("DistanceX", 2,2,1,2, xLength))
        sketch.addConstraint(
            Sketcher.Constraint("DistanceY", 0,1,2,2,yLength))
        if hasattr(obj, "ViewObject"):
            obj.ViewObject.hide()
        sketch.recompute()
        #FreeCADGui.ActiveDocument.setEdit(sketch,0)


    def GetResources(self):
        return {'Pixmap'  : 'addBboxSketch', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('addBboxSketch',\
                'Create Sketch from Bbox'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('addBboxSketch',\
                'Create Sketch from Bbox')}


class lineBuffer :
    def __init__(self, sketch):
        self.sketch = sketch
        self.shortCount = 0
        self.straightCount = 0 
        self.buffer = []
        self.lineCount = 0
        self.sp = None
        self.ep = None
        self.slope = None
        self.slopeTolerance = 5


    def eqSlope(self, slope):    
        from math import inf, isclose
        return isclose(slope, self.slope, abs_tol = 0.01)


    def checkSlope(self, slope):
        if self.slope is not None:
            if abs(slope - self.slope) < self.slopeTolerance:
                return True
        return False


    def checkCont(self, sp):
        # Check if still a continous line if not flush
        print(f'checkCont {self.ep} {sp}')
        if self.ep == sp:
            return
        else:
            print(f'Not continous')
            if self.straightCount > 1:
                self.flushStraight(self.straightCount)
            if self.lineCount > 0:
                self.flushLine()
            if self.shortCount > 0:
                self.flushCurve(self.shortCount)    


    def addLine(self, sp, ep, slope):
        print(f'add-LINE shortCount {self.shortCount} lineCount {self.lineCount} straightCount {self.straightCount}')
        if self.shortCount == 1:
            self.shortCount = 0
            self.lineCount += 1
            if self.eqSlope(slope):
                print(f'Same Slope - Extend short line')
                self.ep = ep
            else:
                print(f'====> Add short line segment')
                self.sketch.addGeometry(Part.LineSegment(self.sp, self.ep))
                # Start point is now previous short line end point
                self.sp = self.ep
            return

        if self.lineCount == 0:
            self.sp = sp
            self.ep = ep
        else:
            if not self.eqSlope(slope): 
                print(f'====> Add line segment')
                self.sketch.addGeometry(Part.LineSegment(self.sp, self.ep))
                self.sp = self.ep
                self.lineCount = 0
            self.ep = ep
        print(f'End Point {self.ep}')    
        self.slope = slope
        self.lineCount += 1     


    def addShortLine(self, sp, ep, slope):
        # Do we have a short line following a normal line
        print(f'   add-SHORT shortCount {self.shortCount} lineCount {self.lineCount} straightCount {self.straightCount}')
        if self.lineCount != 0:
            if self.eqSlope(slope):
                print(f'==> Extend line {ep}')
                self.ep = ep
                return
            else:    
                print(f'==> Flush Long {self.ep} then add Short Line')
                if self.sp != self.ep:
                    self.sketch.addGeometry(Part.LineSegment(self.sp, self.ep))
                else:
                    print(f"Both points are equal - ignore")
            self.lineCount = 0
            self.shortCount = 0
            self.buffer = []
            #self.sp = sp
            #self.ep = ep

        elif self.shortCount != 0:
        #    self.sp = sp
        #    self.ep = ep
        #else:
            print(f'test slope {self.slope} {slope}')
            if self.eqSlope(slope):
                print(f'====> Short Line Same Slope : shortCount {self.shortCount} straightCount {self.straightCount}\n')
                if self.shortCount - self.straightCount == 1:
                    self.straightCount += 1
                    self.ep = ep
                    # Could be same slope in a number of short lines
                    # making a curve so do not flush
                    # Test file Throttle-Lock-short-Curve-Test
                    #    self.flushCurve(self.shortCount)
            else:        
                if self.straightCount > 1:
                    self.flushStraight(self.straightCount)
        self.shortCount += 1
        self.sp = sp
        self.ep = ep
        self.slope = slope
        self.buffer.append(sp)
        self.buffer.append(ep)

    def addArcOfCircle(self, g):
        print(f"Add Arc Of Circle")
        self.sketch.addGeometry(g)
        self.lineCount = 0
        self.sp = g.StartPoint 
        self.ep = g.EndPoint

    def addSegment(self, g):
        print(f"Untested {g.TypeId}")
        self.sketch.addGeometry(g)
        self.lineCount = 0
        self.sp = g.StartPoint 
        self.ep = g.EndPoint

    def flushLine(self):
        if self.lineCount > 0:
           print(f'==> Flush line segment')
           self.sketch.addGeometry(Part.LineSegment(self.sp, self.ep))
           self.lineCount = 0
           self.sp = self.ep


    def flushStraight(self, cnt):
        print(f'==> Flush Straight {cnt}')
        idx = 1 + 2 * cnt
        #print(self.buffer)
        print(f'{self.buffer[0]} {self.buffer[idx]}')
        print(f'sp {self.sp}')
        print(f'ep {self.ep}')
        self.sketch.addGeometry(Part.LineSegment(self.buffer[0], self.buffer[idx]))
        self.sp = self.buffer[idx]
        self.shortCount = self.shortCount - cnt - 1
        self.buffer = self.buffer[idx:]
        self.straightCount = 0
        print(f'shortCount {self.shortCount}')
        return self.shortCount

    def calcHausdorff(self, npPointBuff, curve):
        print(f"Calc Hausdorff")
        import numpy as np
        import hausdorff

        #print(dir(hausdorff))
        # Create evaluated points
        curve.evaluate()
        curvePoints = curve.evalpts
        dist = hausdorff.hausdorff_distance(npPointBuff,np.asarray(curvePoints))
        print(f"Hausdorf dist {dist}")
        return dist

    def fitCurve(self, npPointBuff, numControlPoints):
        from geomdl import fitting
        print(f"evaluate Curve number of control points {numControlPoints}")
        degree = 3
        #curve = fitting.approximate_curve(pointBuff, degree, \
        curve = fitting.approximate_curve(npPointBuff, degree, \
                centripetal=True, ctrlpts_size = numControlPoints)
        return curve


    def curveFit(self, curveCnt):

        import numpy as np
        # fit points for last curveCnt points in buffer
        print(f'==> Curve Fit buffer len {len(self.buffer)} start {self.straightCount} curveCount {curveCnt}')
        # Is there enought points to curveFit#
        if self.shortCount < 3:
            # No just output short lines
            print(f'Short Count {self.shortCount}')
            print(self.buffer)
            # Buffer is n times sp then ep so increment 2
            for i in range(0, self.shortCount, 2):
                print(f'{self.buffer[i]} {self.buffer[i+1]}')
                self.sketch.addGeometry(Part.LineSegment(self.buffer[i],
                                self.buffer[i+1]))
        else:
            print(f'Fit Curve {self.shortCount}') 
            #    points = tuple(pointBuffer)
            
            print(self.buffer[0])
            print(self.buffer[1:self.shortCount*2:2])
            pointBuff = [self.buffer[0]]+self.buffer[1:self.shortCount*2:2]
            #hausValue = 0.1
            numControlPoints = 4
            npPointBuff =np.asarray(pointBuff)
            # get acceptabale fit#
            curve = self.fitCurve(pointBuff, numControlPoints)
            hausValue = self.calcHausdorff(npPointBuff, curve)
            tst = True
            while (tst):
                try:
                    tstCurve = self.fitCurve(pointBuff, numControlPoints+1)
                    tstHause = self.calcHausdorff(npPointBuff, tstCurve)
                    if tstHause < hausValue:
                        tst = True
                        curve = tstCurve
                        hausValue = tstHause
                        numControlPoints += 1
                    else:
                        tst = False   
                except:
                    tst = False
                    #pass    

            print(f'Control Points {numControlPoints}')
            fcCp = []
            for cp in curve._control_points :
                print(f'cp {cp}')
                fcCp.append(FreeCAD.Vector(cp[0],cp[1],0))
            print(curve.degree)
            print(curve._geometry_type)
            print(f"Number of Control points : {len(curve._control_points)}")
            print(f"Knot Vector : {curve.knotvector}")
            print(f"Weights : {curve.weights}")
            self.sketch.addGeometry(Part.BSplineCurve(fcCp,None,None,False,\
                    curve.degree,None,False))


    def flushCurve(self, slope):
        if self.shortCount == 1:
            if slope is not None :
                if self.eqSlope(slope):
                    return
            else:        
                print(f"slop {slope}")
                print(f"self slope {self.slope}")
                return

        if self.shortCount > 0:
            print(f'Flush Curve shortCount {self.shortCount} straightCount {self.straightCount}')
            if self.straightCount > 1:
                if self.flushStraight(self.straightCount) > 0:
                    self.curveFit(self.shortCount)
                self.straightCount = 0

            elif self.shortCount <= 2:
                 print(f'Short Count {self.shortCount}')
                 print(self.buffer)
                 # Buffer is n times sp then ep so increment 2
                 for i in range(0, self.shortCount, 2):
                     print(f'{self.buffer[i]} {self.buffer[i+1]}')
                     if self.buffer[i] != self.buffer[i+1]:
                        self.sketch.addGeometry(Part.LineSegment(self.buffer[i],
                                self.buffer[i+1]))
            else:
                 # straightCount is one or less so ignore
                 self.straightCount = 0
                 self.curveFit(self.shortCount)

            self.shortCount = 0
            self.buffer = []


class toLineCurveDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(toLineCurveDialog, self).__init__(parent)
        from PySide2.QtWidgets import QRadioButton

        # Set dialog title
        self.setWindowTitle("Parameters")

        # Create layout 2
        layout = QtWidgets.QVBoxLayout()

        # Create layout
        #layout2 = QtWidgets.QHBoxLayout()

        # Create label
        #self.label = QtWidgets.QLabel("Break Angle in Degrees")
        #layout2.addWidget(self.label)

        # Create text input
        #self.text_edit = QtWidgets.QLineEdit()
        #self.text_edit.setPlaceholderText("Enter Angle")
        #self.text_edit.setText("15")
        #layout2.addWidget(self.text_edit)

        #layout.addLayout(layout2)

        # Create layout 3
        layout3 = QtWidgets.QHBoxLayout()

        # Create label
        #self.label = QtWidgets.QLabel("Break at Coincident Constraints")
        #layout3.addWidget(self.label)

        #self.Coincident = QtWidgets.QRadioButton("Break at Coincident Constraints", Null)
        self.use_coincidents = QRadioButton("Break at Coincident Constraints")
        layout3.addWidget(self.use_coincidents)
        layout.addLayout(layout3)

        # Add buttons (optional)
        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Combine layouts
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

    def get_angle(self):
        """Retrieve the angle entered by the user."""
        try:
            return float(self.text_edit.text())
        except ValueError:
            return None

    def get_use_coincidents(self):
        """Retrieve the coincidents radio button."""
        try:
            return self.use_coincidents.isChecked()

        except ValueError:
            return None


class toCurveFitFeature :
    
    def Activated(self) :
        dialog = toLineCurveDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            #angle = dialog.get_angle()
            #if angle is not None:
            #    print(f"Break Angle: {angle} degrees")
            #else:
            #    print("Invalid input: Angle set to 15")
            angle = 15
            useCoincidents = dialog.get_use_coincidents()
        else:
            print("Dialog canceled.")
            angle = 15
        for sel in FreeCADGui.Selection.getSelection() :
            print('toCurveFit')
            print(sel.TypeId)
            if sel.TypeId == 'Sketcher::SketchObject' :
                geometry = sel.Geometry
                self.newSketch = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", \
                           "Fitted_"+sel.Name)
                self.newSketch.Placement = sel.Placement
                if useCoincidents:
                    self.processWithBreakPoints(sel, angle)
                else:
                    self.processGeometry(geometry, angle)


    def processWithBreakPoints(self, sketch, angle):
        # break points not really use angle but maybe whole of geometry
        geometry = sketch.Geometry
        if self.findGeomBreakPoints(sketch) > 0:
            bp = self.breakPoints
            # process ranges
            for r in range(0,len(bp)-1):
            #for r in range(0, 1):
                print(f"r {r}")
                print(f" process geometry {bp[r]} to {bp[r+1]}")
                print(f" len bp {len(bp)} bp {bp} bp[-1] {bp[-1]}")
                self.processGeometry(geometry[bp[r]:bp[r+1]], angle)
                #g = geometry[bp[-1]:]+geometry[:bp[0]]

                #g = geometry[bp[-1]-1:]+geometry[:bp[0]]
                #self.processGeometry(g, angle)

        else:  # process whole geometry
            self.processGeometry(geometry, angle)

    def findGeomBreakPoints(self, sketch):
        
        self.breakPoints = []
        # break points at set by user with a coincident constraint
        #self.newSketch.Constraints = sketch.Constraints
        # Does not work as geometry will be different
        # Just copy any GeomPoints in processGeometry
        for i, constraint in enumerate(sketch.Constraints):
            if constraint.Type == 'Coincident':
                print(f"Coincident Constraint {i}:")
                
            # Indices of the geometry involved
            geom1_index = constraint.First
            geom2_index = constraint.Second

            # Points on the respective geometry
            point1_index = constraint.FirstPos
            point2_index = constraint.SecondPos

            print(f"  Geometry {geom1_index}, Point {point1_index}")
            print(f"  Geometry {geom2_index}, Point {point2_index}")

            print(f" Point 1 - Type {sketch.Geometry[geom1_index].TypeId}")
            print(f" Point 2 - Type {sketch.Geometry[geom2_index].TypeId}")

            if sketch.Geometry[geom1_index].TypeId != 'Part::GeomPoint':
                self.breakPoints.append(geom1_index)
                #print(dir(sketch.Geometry[point2_index]))
                g = sketch.Geometry[geom1_index]
                print(f" TypeId {g.TypeId} \n Start {g.StartPoint} EndPoint {g.EndPoint}")
                g = sketch.Geometry[point2_index]
                print(f" TypeId {g.TypeId} \n Start {g.StartPoint} EndPoint {g.EndPoint}")
                #print(dir(sketch.Geometry[point2_index]))
                #print(dir(sketch.Geometry[geom1_index]))
            elif sketch.Geometry[geom2_index].TypeId != 'Part::GeomPoint':
                self.breakPoints.append(geom2_index)
                g = sketch.Geometry[geom2_index]
                print(f" TypeId {g.TypeId} \n Start {g.StartPoint} EndPoint {g.EndPoint}")
                g = sketch.Geometry[point2_index]
                print(f" TypeId {g.TypeId} \n Start {g.StartPoint} EndPoint {g.EndPoint}")

                #print(dir(sketch.Geometry[point1_index]))
                #print(dir(sketch.Geometry[geom2_index]))

        print(f" BreakPoints {self.breakPoints}")
        self.breakPoints.sort()
        print(f" Sorted BreakPoints {self.breakPoints}")
        return len(self.breakPoints)


    def debugSketch(self, geometry, name="Debug"):
        sketchDbg = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", name)
        sketchDbg.Geometry = geometry
        print(f" {name} length {len(geometry)}")


    def processCurveBuffer(self, pointBuffer):
        from geomdl import fitting
        lenPB = len(pointBuffer)
        print(f'Process Curve Buffer {lenPB}')
        # Buffer may not contain enough points for curve
        if lenPB < 3:
            self.insertLines(lenPB, pointBuffer)
        else:
            self.curveFit(lenPB, pointBuffer)


    def insertLines(self, lenPb, pointBuffer):
        print(pointBuffer)

        print(f'Insert Lines {lenPb}')
        for i in pointBuffer:
             self.newSketch.addGeometry(Part.LineSegment(i))


    def processGeometry(self, geom, angle=15):          # toCurveFit
        # UPDATE FOR CURVE ONLY
        import math
        import numpy as np
        import Draft
        # Initialize an empty NumPy array
        print(f"Process Geometry len {len(geom)}")
        self.vectors = []
        self.LastPoint = None
        newLine = True
        tolerance=1e-6
        angleRadians = math.radians(angle)
        for g in geom:
            if g.TypeId == 'Part::GeomLineSegment':
                #print(f'\t\tTypeId : {g.TypeId} Start {g.StartPoint} End {g.EndPoint}')
                if newLine == True:
                    self.vectors.append(g.StartPoint)
                    self.LastStart = g.StartPoint
                    newLine = False
                else:
                    if (g.StartPoint-self.LastPoint).Length >= tolerance:
                        print(f"StartPoint != LastPoint StartPoint {g.StartPoint} LastPoint {self.LastPoint}")
                        print(f" Length {(g.StartPoint-self.LastPoint).Length}")
                        self.processVectorPoints()
                        #self.vectors.append(g.StartPoint)
                        self.vectors = []
                        newLine = True

                    #if self.angle_between_lines(self.LastStart, g.StartPoint, g.EndPoint) >= angleRadians:
                    #    print(f" Large change of angle")
                    #    self.processVectorPoints()
                    #    #self.vectors.append(g.StartPoint)
                    #    newLine = True

                # Last Start should be EndPoint of previous Line
                self.LastStart = g.StartPoint
                self.LastPoint = g.EndPoint
                #print(f"Last Point {self.LastPoint}")
                self.vectors.append(g.EndPoint)

            elif g.TypeId == 'Part::GeomArcOfCircle':
                print(f"Part::GeomArcOfCircle")
                print(f'\t\tTypeId : {g.TypeId} Start {g.StartPoint} End {g.EndPoint}')
                self.processVectorPoints()
                self.newSketch.addGeometry(g)
                newline = True

            else:
                print(f"TypeId {g.TypeId}")

        print(f" FlushVectorPoints")
        self.processVectorPoints()


    def processVectorPoints(self):
        import numpy
        from freecad.toSketch.toSharedFunc import check3PointsOneLine
        print(f" processVectorPoints {len(self.vectors)}")
        for v in self.vectors:
            print(v)
        if len(self.vectors) > 3:
            #points = self.vectors_to_2d_array(self.vectors)
            points = vectors_to_numpy(self.vectors)
            #bSplines = self.fit_bspline(points)
            print(f"First three Points")
            print(f"{points[0]} {points[1]} {points[2]}")
            print(f"Last three Points")
            print(f"{points[-1]} {points[-2]} {points[-3]}")
            bSplines = fit_bspline_to_geom(points,
                    tolerance=1e-4,
                     max_error=0.5
                     )
            if len(bSplines) > 0:
                self.newSketch.addGeometry(bSplines)
        else:
            # less than three in vectors
            vecLen = len(self.vectors)
            print(f" Len Vectors {vecLen} not enough for curve")
            if vecLen == 1:     # length = 1, must be checked first
                self.newSketch.addGeometry(
                    Part.LineSegment(
                        self.LastStart, self.vectors))
                self.LastStart = self.vectors  
            elif vecLen == 2 or check3PointsOneLine(self.vectors):
                #   Use first and last
                self.newSketch.addGeometry(
                                Part.LineSegment(
                                    self.vectors[0],
                                    self.vectors[-1]
                                ))
            else: # vecLen == 3:   # len = 3
                self.newSketch.addGeometry(
                                Part.LineSegment(
                                    self.vectors[0],
                                    self.vectors[1]
                                ))
                self.newSketch.addGeometry(
                                Part.LineSegment(
                                    self.vectors[1],
                                    self.vectors[2]
                                ))
            
                  

    def vectors_to_2d_array(self, vectors, plane="XY"):
        """
        Converts a list of FreeCAD vectors into a NumPy 2D array for a specified plane.

        Parameters:
            vectors (list of App.Vector): List of FreeCAD vectors.
            plane (str): The plane of projection ("XY", "XZ", "YZ").

        Returns:
            np.ndarray: A 2D NumPy array of shape (n, 2), where n is the number of vectors.
        """
        import numpy as np
        # Map plane to corresponding coordinate extraction
        plane_map = {
            "XY": lambda v: (v.x, v.y),
            "XZ": lambda v: (v.x, v.z),
            "YZ": lambda v: (v.y, v.z)
        }

        # Ensure the specified plane is valid
        if plane not in plane_map:
            raise ValueError(f"Invalid plane '{plane}'. Valid options are 'XY', 'XZ', 'YZ'.")

        # Extract the 2D coordinates based on the plane
        array = np.array([plane_map[plane](v) for v in vectors])

        return array


    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True


    def GetResources(self):
        return {'Pixmap'  : 'toCurveFit', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toCurveFitFeature',\
                'to CurveFit'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toCurveFitFeature',\
                'to CurveFit')}


class toLineCurveFitFeature :

    def Activated(self) :
        for sel in FreeCADGui.Selection.getSelection() :
            print('toLineCurveFit')
            print(sel.TypeId)
            if sel.TypeId == 'Sketcher::SketchObject' :
               #print(dir(sel))
               newSketch = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", \
                           "Fitted Sketch")
               newSketch.Placement = sel.Placement
               print('Geometry Count : '+str(sel.GeometryCount))
               self.processGeometry(newSketch, sel.Geometry)
               newSketch.recompute()

    #def insertLines(self, newSketch, lenPb, pointBuffer):
    #      print(pointBuffer)
        
    #    print(f'Insert Lines {lenPb}')
    #    for i in pointBuffer:
    #         newSketch.addGeometry(Part.LineSegment(i))

    # Function to test if two GeomLineSegments are contiguous
    def are_contiguous(self, startPoint, endPoint, tolerance=1e-6):
        """
        Check if two Geom.LineSegment objects are contiguous.

        :param line1: First Geom.LineSegment
        :param line2: Second Geom.LineSegment
        :param tolerance: Maximum distance to consider as contiguous
        :return: True if the lines are contiguous, False otherwise
        """
    
        # Check if any endpoint of one line matches the endpoint of the other line
        print(f"Are_contig? start {startPoint} end {endPoint}")
        print(f"LastStart {self.LastStart} LastPoint {self.LastPoint}")
        if  self.LastPoint.distanceToPoint(startPoint) <= tolerance:
            print(f"LastPoint = nextstart")
            return 1, self.LastStart, endPoint

        if  self.LastStart.distanceToPoint(endPoint) <= tolerance:
            # need to swap ??
            return 1, startPoint, endPoint

        if  self.LastStart.distanceToPoint(startPoint) <= tolerance:
            # need to swap ??
            return 1, endPoint, startPoint

        if  self.LastPoint.distanceToPoint(endPoint) <= tolerance:
            # need to swap ??
            return 1, endPoint, startPoint

        return 0, self.LastStart, self.LastPoint

    def processGeometry(self, newSketch, geom, angle=15.0):     # LineCurve
        # UPDATE FOR CURVE ONLY
        import math 
        import numpy as np
        import Draft
        # Initialize an empty NumPy array
        self.newSketch = newSketch
        self.vectors = []
        self.LastPoint = None
        newLine = True
        flushLine = False
        tolerance=1e-6
        #print(f"Angle {angle}")
        angleRadians = math.radians(angle)
        #geom.sort()
        for g in geom:
            if g.TypeId == 'Part::GeomLineSegment':
                print(f'\t\tTypeId : {g.TypeId} Start {g.StartPoint} End {g.EndPoint}')
                if newLine == True:
                    self.vectors.append(g.StartPoint)
                    self.LastStart = g.StartPoint
                    self.LastPoint = g.EndPoint
                    newLine = False
                    flushLine = True
                else:
                    contig, newStart, newEnd = self.are_contiguous(
                        g.StartPoint,
                        g.EndPoint
                        )
                    print(f"Are Contig Results : {contig} newLastStart {newStart} newLastPoint {newEnd}")
                    if contig == 0:
                        print(f"Not contigous")
                        print(f"StartPoint != LastPoint StartPoint {g.StartPoint} LastPoint {self.LastPoint}")
                        self.processVectorPoints()
                        #self.vectors.append(g.StartPoint)
                        self.vectors = []
                        newLine = True

                    angle = angle_between_lines(self.LastStart, g.StartPoint, g.EndPoint)
                    print(f"Angle {angle}")
                    delta = 0.012
                    if angle > delta and angle < (3.142 - delta):
                        if flushLine == True:
                            print(f"\n\nFlush line {self.LastStart} {self.LastPoint}")
                            self.newSketch.addGeometry(
                                Part.LineSegment(
                                    self.LastStart,
                                    self.LastPoint
                                    )
                                )
                            self.vectors = []
                            self.vectors.append(self.LastPoint)
                            flushLine = False
                        # No - Straight Line no change Last Start or End
                        # Last Start should be EndPoint of previous Line
                        self.LastStart = self.LastPoint
                        self.LastPoint = g.EndPoint
                        self.vectors.append(g.EndPoint)
                    else:    
                        self.LastStart = newStart
                        self.LastPoint = newEnd

            elif g.TypeId == 'Part::GeomArcOfCircle':
                print(f"Part::GeomArcOfCircle")
                print(f'\t\tTypeId : {g.TypeId} Start {g.StartPoint} End {g.EndPoint}')
                self.processVectorPoints()

                self.newSketch.addGeometry(g)
                newline = True

            else:
                print(f"TypeId {g.TypeId}")

        print(f" End Flush Vector Points")
        self.processVectorPoints()

    def processVectorPoints(self):
        print(f" processVectorPoints {len(self.vectors)}")
        if len(self.vectors) < 4:
            print(f"Vectors {self.vectors}")
            for v in self.vectors:
                self.newSketch.addGeometry(
                                Part.LineSegment(self.LastStart, v)
                                )
                self.LastStart = v
        else:        
            #points = self.vectors_to_2d_array(self.vectors)
            points = vectors_to_numpy(self.vectors)
            #bSplines = self.fit_bspline(points)
            bSplines = fit_bspline_to_geom(points, len(points), max_error=0.5)
            if len(bSplines) > 0:
                self.newSketch.addGeometry(bSplines)

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toLineCurveFit', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toLineCurveFitFeature',\
                'to LineCurveFit'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toLineCurveFitFeature',\
                'to LineCurveFit')}

    def processLines(self, sketch, start, end, gL, dL) :
        import numpy

        threshold = 3 * numpy.median(dL)
        print('Processing series of Lines : '+str(start)+' : '+str(end))
        print('Threshold : '+str(threshold))
        print('Average : '+str(numpy.average(dL)))
        for i in range(start,end) :
            if dL[i] > threshold :
               #print('Adding long line : '+str(i))
               sketch.addGeometry(gL[i], False)
               #print('Curve Fit ? : '+str(start)+' upto '+str(i))
               self.curveFit(sketch, gL[start:i])
               start = i + 1
        # Process Tail
        self.curveFit(sketch, gL[start:i])

class toMacroFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        print('ToMacro') 
        for sel in FreeCADGui.Selection.getSelection() :
            print("Selected")
            print(sel.TypeId)
            #print(dir(sel))
            if sel.TypeId == 'Sketcher::SketchObject' :
               self.actionToMacro(sel)

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toMacro', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toMacroFeature',\
                'To Macro'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toMacroFeature',\
                'To Macro')}

    def wrtVector(self, fp, v, comma) :
        if comma :
           fp.write('FreeCAD.Vector('+str(v[0])+','+str(v[1])+',' \
                       +str(v[2])+'), ')
        else :
           fp.write('FreeCAD.Vector('+str(v[0])+','+str(v[1])+',' \
                       +str(v[2])+')')

    def wrtVectorList(iself, fp, list) :
        print(list)
        fp.write('[')
        for i in range(len(list)-1) :
           print(i)
           fp.write('FreeCAD.Vector('+str(list[i][0])+','+str(list[i][1])+',' \
                       +str(list[i][2])+'), ')
        i += 1
        fp.write('FreeCAD.Vector('+str(list[i][0])+','+str(list[i][1])+',' \
                       +str(list[i][2])+')]')
          
    def wrtRotation(self, fp, r) :
        fp.write('FreeCAD.Rotation('+str(r[0])+','+str(r[1])+',' \
                       +str(r[2])+','+str(r[3]))

    def wrtIdentity(self, fp, comma) :
        if comma :
           fp.write('FreeCAD.Vector(0,0,1),')
        else  :
           fp.write('FreeCAD.Vector(0,0,1)')

    def getRadians(self, A, B) :
        import math

        delX = A[0] - B[0]
        delY = A[1] - B[1]
        return(math.atan2(delY,delX))

    def actionToMacro(self,sketch):
        import math

        print('Action To Macro : '+sketch.Label)
        print('Geometry Count : '+str(sketch.GeometryCount))
        geo = sketch.Geometry
        # macro path
        param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
        path = param.GetString("MacroPath","") + "/"
        path = path.replace("\\","/")
        print("Path for Macros : " , path)
        fp = open(path+sketch.Label+'.FCMacro','w+')
        #fp = open('/tmp/'+sketch.Label,'w+')
        fp.write('# This Macro was created using toSketch Macro facility - (c) Keith Sloan\n')
        fp.write('sketch = FreeCAD.ActiveDocument.ActiveObject\n')
        fp.write('newSketch = True\n')
        fp.write('if sketch is not None :\n')
        fp.write('   if hasattr(sketch,"TypeId") :\n')  
        fp.write('      if sketch.TypeId == "Sketcher.SketchObject" : \n')
        fp.write('         newSketch = False\n')
        fp.write('if newSketch :\n')
        fp.write('   sketch = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject","Sketch")\n')
        fp.write('print("Active Sketch is : "+sketch.Label+" In Document : "+FreeCAD.ActiveDocument.Label)\n')
        for i in range(sketch.GeometryCount):
            print(geo[i].TypeId)
            #print(dir(geo[i]))
            if geo[i].TypeId == 'Part::GeomLineSegment':
               print('Line Segment')
               fp.write('sketch.addGeometry(Part.LineSegment(')
               self.wrtVector(fp, geo[i].StartPoint, True) 
               self.wrtVector(fp, geo[i].EndPoint, False)
               fp.write('),False)\n')

            elif geo[i].TypeId == 'Part::GeomArcOfCircle':
               print('Arc of circle')
               #print(dir(geo[i]))
               startX = geo[i].StartPoint[0] - geo[i].Center[0]
               startY = geo[i].StartPoint[1] - geo[i].Center[1]
               endX = geo[i].EndPoint[0] - geo[i].Center[0]
               endY = geo[i].EndPoint[1] - geo[i].Center[1]
               #from math import atan
               import math
               startRad = math.atan2(startY,startX)
               #print(startRad)
               endRad = math.atan2(endY,endX)
               #print(endRad)
               fp.write('sketch.addGeometry(Part.ArcOfCircle(Part.Circle(')
               self.wrtVector(fp, geo[i].Center, True)
               fp.write('FreeCAD.Vector(0,0,1),'+str(geo[i].Radius)+'),')
               fp.write(str(startRad)+','+str(endRad))
               fp.write('), False)\n')
            
            elif geo[i].TypeId == 'Part::GeomCircle':
               print('GeomCircle')
               fp.write('sketch.addGeometry(Part.Circle(')
               self.wrtVector(fp, geo[i].Center, True)
               self.wrtIdentity(fp,True)
               fp.write(str(geo[i].Radius)+'), False)\n')
            
            elif geo[i].TypeId == 'Part::GeomPoint':
               print('GeomPoint')
               fp.write('sketch.addGeometry(Part.Point(FreeCAD.Vector('+str(geo[i].X) +','+str(geo[i].Y)+','+str(geo[i].Z)+')),False)\n')
            
            elif geo[i].TypeId == 'Part::GeomEllipse' :
               print('GeomEllipse')
               #print(dir(geo[i]))
               #print('Angle XU : '+str(geo[i].AngleXU))
               #print('Axis : '+str(geo[i].Axis))
               #print('XAxis : '+str(geo[i].XAxis))
               #print('YAxis : '+str(geo[i].YAxis))
               #print('Location : '+str(geo[i].Location))
               #print('Rotation : '+str(geo[i].Rotation))
               #print(geo[i].Rotation.Q)
               #print('Minor: '+str(geo[i].MinorRadius))
               #print('Major: '+str(geo[i].MajorRadius))
               fp.write('ellipse = Part.Ellipse(')
               self.wrtVector(fp, geo[i].Center, True)
               fp.write(str(geo[i].MajorRadius)+','+str(geo[i].MinorRadius)+')\n')
               fp.write('ellipse.rotate(FreeCAD.Placement(')
               self.wrtVector(fp,geo[i].Location,True)
               self.wrtRotation(fp,geo[i].Rotation.Q)
               fp.write(')))\n')
               fp.write('sketch.addGeometry(ellipse,False)\n')
            
            elif geo[i].TypeId == 'Part::GeomArcOfEllipse' :
               print('Arc of Ellipse')
               print(dir(geo[i])) 
               print(dir(geo[i].Ellipse)) 
               print(geo[i].Ellipse.Rotation) 
               fp.write('ellipse = Part.Ellipse(')
               self.wrtVector(fp, geo[i].Center, True)
               fp.write(str(geo[i].MajorRadius)+','+str(geo[i].MinorRadius)+')\n')
               fp.write('print(dir(ellipse))\n')
               fp.write('print(dir(ellipse.Rotation))\n')
               fp.write('print(ellipse.Rotation)\n')
               fp.write('print(ellipse.Rotation.Q)\n')
               fp.write('print(ellipse.AngleXU)\n')
               fp.write('ellipse.rotate(FreeCAD.Placement(')
               self.wrtVector(fp,geo[i].Location,True)
               print(fp,geo[i].Rotation)
               self.wrtRotation(fp,geo[i].Ellipse.Rotation.Q)
               #fp.write('FreeCAD.Rotation(0,0,0,1)')
               fp.write(')))\n')
               print(geo[i].Ellipse.Rotation.Angle)
               #rotRa   = geo[i].Ellipse.Rotation.Angle * math.pi / 180
               rotRa   = geo[i].Ellipse.Rotation.Angle
               startRa = self.getRadians(geo[i].StartPoint, geo[i].Center)-rotRa
               #startRa = self.getRadians(geo[i].StartPoint, geo[i].Center)
               endRa   = self.getRadians(geo[i].EndPoint, geo[i].Center)-rotRa
               #endRa   = self.getRadians(geo[i].EndPoint, geo[i].Center)
               fp.write('sketch.addGeometry(Part.ArcOfEllipse(ellipse,'+str(startRa)+','+str(endRa)+'),False)\n')
             
            elif geo[i].TypeId == 'Part::GeomBSplineCurve' :
               print('GeomBSpline')
               #print(dir(geo[i]))
               #print(geo[i].StartPoint)
               #print(geo[i].EndPoint)
               #print(geo[i].Degree)
               #print(geo[i].KnotSequence)
               #print(geo[i].NbKnots)
               #print(geo[i].NbPoles)
               #print(geo[i].getPoles())
               fp.write('sketch.addGeometry(Part.BSplineCurve(')
               self.wrtVectorList(fp, geo[i].getPoles())
               fp.write(',None,None,False,'+str(geo[i].NbPoles)+',None,False),False)\n')
        fp.write("print('Geometry added to Sketch : '+sketch.Label)\n")
        for i in sketch.Constraints :
           #print(dir(i))
           #print(i.Type)
           #print(i.Content)
           if i.Type == 'Coincident' :
             fp.write('sketch.addConstraint(Sketcher.Constraint("Coincident",')
             fp.write(str(i.First)+','+str(i.FirstPos)+',')
             fp.write(str(i.Second)+','+str(i.SecondPos)+'))\n')
           elif i.Type == 'Horizontal' :
             fp.write('sketch.addConstraint(Sketcher.Constraint("Horizontal",')
             fp.write(str(i.First)+'))\n')
           elif i.Type == 'Vertical' :
             fp.write('sketch.addConstraint(Sketcher.Constraint("Vertical",')
             fp.write(str(i.First)+'))\n')
           elif i.Type == 'Equal' : 
             fp.write('sketch.addConstraint(Sketcher.Constraint("Equal",')
             fp.write(str(i.First)+','+str(i.Second)+'))\n')
           elif i.Type == 'Angle' :
             if hasattr(i,'Second') :
                fp.write('sketch.addConstraint(Sketcher.Constraint("Angle",')
                fp.write(str(i.First)+','+str(i.FirstPos)+','+str(i.Second))
                fp.write(','+str(i.SecondPos)+','+str(i.Value)+'))\n')
        fp.write("print('Constraints added to Sketch : '+sketch.Label)\n")
        fp.close()
        print('Macro : '+sketch.Label+' Written')


class toPlane2PartFeature :    

    def Activated(self) :
        from .toSObjects import toSPlane, ViewProvider
        #   for obj in FreeCADGui.Selection.getSelection():
        selectEx = FreeCADGui.Selection.getSelectionEx()
        for sel in selectEx :
            print(f"Selected-Ex {sel.ObjectName} {sel.TypeId}")
            obj = sel.Object
            if obj.TypeId == 'Part::FeaturePython':
                if obj.Label[:7] == 'toPlane' or obj.Label[:5] == 'Plane':
                    print(f"Add Part Plane")
                    partPlane = FreeCAD.ActiveDocument.addObject("Part::Plane","PartPlane")
                    #print(partPlane.Placement)
                    #print(partPlane.Placement.Rotation)
                    #print(dir(partPlane.Placement))
                    partPlane.Placement.Rotation.Axis = [0.00, 1.00, 0.00]
                    partPlane.Placement.Rotation.Angle = 1.5708 # 90.0 degrees
                    partPlane.Placement.Base = [-50, 0, -50]
                    partPlane.Length = 100
                    partPlane.Width = 100

                    #print(dir(partPlane))



    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'Plane2Part', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'toPlane to PartPlane'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'toPlane to PartPlane')}


class toSPlaneFeature :    

    def Activated(self) :
        from .toSObjects import toSPlane, ViewProvider

        obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython', \
                   'toPlane')
        toSPlane(obj)
        ViewProvider(obj.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        # need Shape but do not want Placement
        #obj.setEditorMode('Placement',2)
        #print(dir(obj))
        #print(dir(obj.ViewObject))
        obj.ViewObject.Transparency = 20

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toPlane', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'create toPlane'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'create toPlane')}


class bSpline2ArcFeature :    

    def Activated(self) :
        from .toSObjects import toSPlane, ViewProvider

        #   for obj in FreeCADGui.Selection.getSelection():
        selectEx = FreeCADGui.Selection.getSelectionEx()
        for sel in selectEx :
            print(f"Selected-Ex {sel.ObjectName} {sel.TypeId}")
            obj = sel.Object
            if obj.TypeId == 'Sketcher::SketchObject':
                print(f'Check sketch Splines for possible arcs')

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'BSpline2Arc', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'BSpline to Arc'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'BSpline to Arc')}

    def is_bspline_close_to_circle(bspline, tolerance=1e-3):
        """
        Checks if the given B-spline is close to an arc of a circle.

        Args:
            bspline (Part.BSplineCurve): The B-spline to test.
            tolerance (float): Maximum allowed deviation from the circle.

        Returns:
            bool: True if close to a circle, False otherwise.
            dict: Details about the fitted circle if applicable.
        """
        # Sample points along the B-spline
        num_samples = 100
        points = [bspline.value(bspline.ParameterRange[0] + 
                            i * (bspline.ParameterRange[1] -
                            bspline.ParameterRange[0]) / (num_samples - 1)) 
                for i in range(num_samples)]
    
        # Fit a circle to the points
        try:
            circle = Part.Circle()
            circle.fitThroughPoints(points)
     
            # Calculate deviations
            deviations = [abs(circle.Center.distanceToPoint(p) -
            circle.Radius) for p in points]
            max_deviation = max(deviations)

            if max_deviation <= tolerance:
                return True, {"center": circle.Center, "radius": circle.Radius, "deviation": max_deviation}
            else:
                return False, {"max_deviation": max_deviation}
        except Exception as e:
                return False, {"error": str(e)}


    def subdivide_bspline(bspline, num_segments=5, arc_tolerance=1e-3):
        """
        Subdivides a B-spline into smaller B-splines and circular arcs if possible.

        Args:
            bspline (Part.BSplineCurve): The B-spline to subdivide.
            num_segments (int): Number of segments to split into.
            arc_tolerance (float): Tolerance for arc fitting.

        Returns:
            list: List of sub-elements (B-splines or arcs).
        """
        parameter_range = bspline.ParameterRange
        step = (parameter_range[1] - parameter_range[0]) / num_segments

        segments = []

        for i in range(num_segments):
            # Subdivide the B-spline
            start_param = parameter_range[0] + i * step
            end_param = start_param + step
            segment = bspline.trim(start_param, end_param)

            # Check if the segment is close to an arc
            is_arc, details = is_bspline_close_to_circle(segment, tolerance=arc_tolerance)
            if is_arc:
                circle = Part.Circle()
                circle.Center = details["center"]
                circle.Radius = details["radius"]
                arc = circle.toShape(segment.startPoint(), segment.endPoint())
                segments.append(arc)
            else:
                segments.append(segment)

        return segments


class toScaleFeature :

    def Activated(self):
      from .toSObjects import toScale, ViewProvider

      for sel in FreeCADGui.Selection.getSelection() :
          print('Selected')
          if len(sel.InList) > 0 :
             parent = sel.InList[0]
             obj = parent.newObject('Part::FeaturePython',sel.Label+'_Scale')
             toScale(obj, sel.Shape, sel.Shape.BoundBox)
             ViewProvider(obj.ViewObject)
          else :
             obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Scale')
             toScale(obj, sel.Shape, sel.Shape.BoundBox)
             ViewProvider(obj.ViewObject)
          for i in sel.OutList :
              obj.addObject(i) 
          FreeCAD.ActiveDocument.removeObject(sel.Name)
          FreeCAD.ActiveDocument.recompute()

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toScale', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toScaleFeature',\
                'To Scale'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toScalesFeature',\
                'To Scale')}


class toResetOriginFeature :

    def Activated(self):
      from .toSObjects import toResetOrigin, ViewProvider

      for sel in FreeCADGui.Selection.getSelection() :
        print(f'to ResetOrigin Feature Selected {sel.TypeId}')
        Ignore = ['App::Part']
        if hasattr(sel,'Shape') and sel.TypeId not in Ignore :
           if len(sel.InList) > 0 :
              parent = sel.InList[0]
              obj = parent.newObject('Part::FeaturePython', \
                    sel.Label+'_Reset_Origin')
              toResetOrigin(obj, sel.Shape, sel.Shape.BoundBox)
              ViewProvider(obj.ViewObject)
           else :
              obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython', \
                   sel.Label+'_Reset_Origin')
              toResetOrigin(obj, sel.Shape, sel.Shape.BoundBox)
              ViewProvider(obj.ViewObject)
              for i in sel.OutList :
                 obj.addObject(i) 
           FreeCAD.ActiveDocument.removeObject(sel.Name)
           FreeCAD.ActiveDocument.recompute()

        elif sel.TypeId == "Mesh::Feature":
           print(f"COG {sel.Mesh.CenterOfGravity}")
           placement = FreeCAD.Placement()
           placement.Base = FreeCAD.Vector( \
                - sel.Mesh.CenterOfGravity.x, \
                - sel.Mesh.CenterOfGravity.y, \
                - sel.Mesh.CenterOfGravity.z)
           # Adjust for Bounding Box  
           #placement.Base = FreeCAD.Vector( \
           #     -sel.Mesh.BoundBox.XMin,
           #     -sel.Mesh.BoundBox.YMin,
           #     -sel.Mesh.BoundBox.ZMin)

           mshCpy = sel.Mesh.copy()
           print(f"placement {placement}")
           mshCpy.transform(placement.toMatrix())
           sel.Mesh = mshCpy

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toResetOrigin', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toResetOriginFeature',\
                'To Reset Origin'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toResetOriginFeature',\
                'To Reset Orgin')}


class toShapeInfoFeature :

    def Activated(self):
      #from .toSObjects import toTransform, ViewProvider

      for sel in FreeCADGui.Selection.getSelection() :
          print('Selected')
          print(sel.Label)
          print(sel.TypeId)
          print(sel.Content)
          print('Number of Faces    : '+str(len(sel.Shape.Faces)))
          print('Number of Edges    : '+str(len(sel.Shape.Edges)))
          print('Number of Vertexes : '+str(len(sel.Shape.Vertexes)))
          print('Number of Wires    : '+str(len(sel.Shape.Wires)))
          print('InList  : '+str(sel.InList))
          print('OutList : '+str(sel.OutList))
          #print(dir(sel))
          print(dir(sel.Shape))
          print(dir(sel.Shape.Faces[0]))

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toShapeInfo', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toShapeInfo',\
                'Shape Info'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toShapeInfo',\
                'Shape Info')}


FreeCADGui.addCommand('toSketchCommand',toSketchFeature())
FreeCADGui.addCommand('section2SketchCommand',section2SketchFeature())
FreeCADGui.addCommand('Plane2PartPlaneCommand',toPlane2PartFeature())
FreeCADGui.addCommand('removeOuterBoxCommand',removeOuterBoxFeature())
FreeCADGui.addCommand('addBboxCommand',addBboxFeature())
FreeCADGui.addCommand('toLineCurveFitCommand',toLineCurveFitFeature())
FreeCADGui.addCommand('toCurveFitCommand',toCurveFitFeature())
FreeCADGui.addCommand('bSpline2ArcCommand',bSpline2ArcFeature())
FreeCADGui.addCommand('toMacroCommand',toMacroFeature())
FreeCADGui.addCommand('toSPlaneCommand',toSPlaneFeature())
FreeCADGui.addCommand('toScaleCommand',toScaleFeature())
FreeCADGui.addCommand('toResetOriginCommand',toResetOriginFeature())
FreeCADGui.addCommand('toShapeInfoCommand',toShapeInfoFeature())
