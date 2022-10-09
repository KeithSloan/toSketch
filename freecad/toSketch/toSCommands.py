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

import FreeCAD,FreeCADGui, Part, Draft, Sketcher, Show
from PySide import QtGui, QtCore

class toSketchFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        #   for obj in FreeCADGui.Selection.getSelection():
        for sel in FreeCADGui.Selection.getSelectionEx() :
            print("Selected-Ex")
            print(sel.TypeId)
            #print(dir(sel))
            #print(sel.ObjectName)
            #print(sel.FullName)
            if sel.HasSubObjects == True :
               print('SubObjects')
               if hasattr(sel.SubObjects[0],'Surface') :
                  if str(sel.SubObjects[0].Surface) == '<Plane object>' :
                     print('Planar')
                     face = sel.SubObjects[0]
                     # move face to origin
                     face.translate(face.Placement.Base.negative())
                     sketch = self.shapes2Sketch(face,'Sketch')
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
  
        for sel in FreeCADGui.Selection.getSelection() :
            print("Selected")
            print(sel.TypeId)
            #print(dir(sel))
            if sel.TypeId == 'PartDesign::Plane' :
               #print(dir(sel))
               #print(dir(sel.Shape))
               sketch = self.actionSection(sel.Shape)
               nVector = sel.Shape.Faces[0].normalAt(1,1)
               pVector = sel.Placement.Base
               dVector = nVector.multiply(nVector.dot(pVector))
               sketch.Placement.move(dVector)
            elif sel.TypeId == 'Part::FeaturePython' and \
               sel.Label[:5] == 'Plane' :
               sketch = self.actionSection(sel.Shape)
            elif sel.TypeId == 'Part::Plane' :
               self.actionSection(sel)
            elif sel.TypeId == 'Part::Feature' :
               sketch = self.shapes2Sketch(sel.Shape,'Sketch')
            elif sel.TypeId == 'Part::Offset2D':
                print(f'Part::Offset2D')
                sketch = self.shapes2Sketch(sel.Shape,'Sketch')

            #print(sel.ViewObject.Visibility)
            #sel.ViewObject.Visibility = False

        try :
            FreeCADGui.ActiveDocument.setEdit(sketch,0)
        except :
            pass

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toSketch', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toSketchFeature',\
                'To Sketch'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSketchFeature',\
                'To Sketch')}

    def actionSection(self,plane):
        print('Action Section')
        edges = []
        for obj in FreeCAD.ActiveDocument.Objects :
            #print(obj.Label)
            print(obj.TypeId)
            if hasattr(obj,'Mesh') :
               print(dir(obj))
               print(dir(obj.Mesh))
               print(dir(obj.Mesh.Content))
            if hasattr(obj,'Shape') and \
                  obj.TypeId != 'Sketcher::SketchObject' and \
                  obj.TypeId != 'PartDesign::Body' : # Otherwise Body & Content
               if obj.Shape.Volume > 0 :
                  print(obj.Label+' : Has shape')
                  sect = obj.Shape.section(plane)
                  #print(sect)
                  print(sect.ShapeType)
                  if len(sect.SubShapes) > 0 :
                     print('Intersect : '+obj.Label)
                     print(len(sect.SubShapes))
                     for e in sect.SubShapes :
                         edges.append(e)
                  obj.ViewObject.Visibility = False
                  #print(dir(sect))
        sketch = self.shapes2Sketch(edges,'Sketch')
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

    def shapes2Sketch(self, shapes, name) :
        print('shapes2sketch')
        Draft.draftify(shapes, makeblock=False, delete=True)
        try :
            print('Auto Constraint')
            sketch = Draft.makeSketch(shapes, autoconstraints=True, \
                 addTo=None, delete=False, name=name,  \
                       radiusPrecision=-1)
            return sketch
        except :
            print('Non Auto Constraint')
            sketch = Draft.makeSketch(shapes, autoconstraints=False, \
                 addTo=None, delete=False, name=name,  \
                         radiusPrecision=-1)
            return sketch

class toCurveFitFeature :

    def Activated(self) :
        for sel in FreeCADGui.Selection.getSelection() :
            print('toCurveFit')
            print(sel.TypeId)
            if sel.TypeId == 'Sketcher::SketchObject' :
               #print(dir(sel))
               gL = sel.Geometry
               newSketch = FreeCAD.ActiveDocument.addObject("Sketcher::SketchObject", \
                           "Fitted Sketch")
               dL = []
               start = 0
               print('Geometry Count : '+str(sel.GeometryCount))
               for i in range(sel.GeometryCount):
                   #print('TypeId : '+gL[i].TypeId) 
                   if gL[i].TypeId == 'Part::GeomLineSegment':
                      #print(str(i)+' ' +str(gL[i]))
                      #print(dir(gL[i]))
                      #print(gL[i].StartPoint)
                      #print(gL[i].EndPoint)
                      ab = gL[i].StartPoint.sub(gL[i].EndPoint)
                      dL.append(ab.Length)
                   else :
                      # Add non Line Geometry 
                      newSketch.addGeometry(gL[i], False)
                      print('Break - need to process Lines')
                      if len(dL) > 0 :
                         self.processLines(newSketch,start,i,gL,dL)
                         dL = []
                         start = i
                      # append to new geometry
               # Catch tail end
               if len(dL) > 0 :
                  self.processLines(newSketch,start,i,gL,dL)
               #print(dir(sel.Geometry))
               #print(newSketch.Geometry)
               newSketch.recompute()

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

    def curveFit(self, sketch, gL) :
        #print('Curve Fit : points : '+str(len(gL)))
        if len(gL) < 2 :
           for i in gL :
               sketch.addGeometry(i, False)
        else :
           print('Curve Fit : '+str(len(gL)))
           #print(dir(gL[0]))
           #print(gL[0].StartPoint)
           #print(gL[0].EndPoint)
           #sketch.addGeometry(Part.LineSegment(gL[0].StartPoint,gL[-1].EndPoint))
           #try :
           from geomdl import fitting
              
           points = []
           for i in gL :
               points.append([i.StartPoint.x, i.StartPoint.y])
           points.append([i.EndPoint.x, i.EndPoint.y])
           points = tuple(points)
           degree = 3
           #curveI = fitting.interpolate_curve(points, degree)
           curve = fitting.approximate_curve(points, degree, \
                   centripetal=True, ctrlpts_size = 4)
           #print(dir(curve))
           #print(curve._control_points)
           fcCp = []
           for cp in curve._control_points :
               fcCp.append(FreeCAD.Vector(cp[0],cp[1],0))
           print(curve.degree)
           print(curve._geometry_type)
           print('Number of Control points : '+str(len(curve._control_points)))
           #print('Number of Control points : '+str(len(curveI._control_points)))
           print('Knot Vector : '+str(curve.knotvector))
           sketch.addGeometry(Part.BSplineCurve(fcCp,None,None,False, \
                             curve.degree,None,False))

           #except :
           #   print('You need to install NURBS-Python : geomdl')

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

class toSPlaneFeature :    

    def Activated(self) :
        from .toSObjects import toSPlane, ViewProvider

        obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython', \
                   'Plane')
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
                'to Plane'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toSPlaneFeature',\
                'to Plane')}

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
             toScale(obj, sel.Shape, sle.Shape.BoundBox)
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
          print('Selected')
          print(sel.TypeId)
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
                     'Reset_Origin')
                toResetOrigin(obj, sel.Shape, sel.Shape.BoundBox)
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
FreeCADGui.addCommand('toCurveFitCommand',toCurveFitFeature())
FreeCADGui.addCommand('toMacroCommand',toMacroFeature())
FreeCADGui.addCommand('toSPlaneCommand',toSPlaneFeature())
FreeCADGui.addCommand('toScaleCommand',toScaleFeature())
FreeCADGui.addCommand('toResetOriginCommand',toResetOriginFeature())
FreeCADGui.addCommand('toShapeInfoCommand',toShapeInfoFeature())
