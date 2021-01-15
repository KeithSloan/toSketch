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
            print("Selected")
            if sel.HasSubObjects == True :
               if str(sel.SubObjects[0].Surface) == '<Plane object>' :
                  print('Planar')
                  shape = sel.SubObjects[0]
                  #shape.exportStep('/tmp/exported.step')
                  #shape.exportBrep('/tmp/exported.brep')
                  self.shapes2Sketch(shape,'Sketch')
        
        for sel in FreeCADGui.Selection.getSelection() :
            if sel.TypeId == 'Part::FeaturePython' and \
               sel.Label[:5] == 'Plane' : 
               self.actionSection(sel.Shape)
            if sel.TypeId == 'Part::Plane' :
               self.actionSection(sel)
            print(sel.ViewObject.Visibility)
            sel.ViewObject.Visibility = False

        try :
            FreeCADGui.ActiveDocument.setEdit('Sketch',0)
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
            if hasattr(obj,'Shape') :
               print(obj.Label)
               sect = obj.Shape.section(plane)
               #print(sect)
               #print(sect.ShapeType)
               #print(sect.Wires)
               print(sect.SubShapes)
               if len(sect.SubShapes) > 0 :
                  print('Intesect : '+obj.Label)
                  for e in sect.SubShapes :
                      edges.append(e)
               obj.ViewObject.Visibility = False
               #print(dir(sect))
        self.shapes2Sketch(edges,'Sketch')
        #Draft.makeSketch(edges,autoconstraints=False, addTo= None, \
        #       delete=False, name='Sketch', radiusPrecision=-1)

    def shapes2Sketch(self, shapes, name) :
        Draft.draftify(shapes, makeblock=False, delete=True)
        try :
            Draft.makeSketch(shapes, autoconstraints=True, \
                 addTo=None, delete=False, name=name,  \
                       radiusPrecision=-1)
        except :
            Draft.makeSketch(shapes, autoconstraints=False, \
                 addTo=None, delete=False, name=name,  \
                         radiusPrecision=-1)
        
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
          print(sel.Label)
          print(sel.TypeId)
          print(dir(sel))
          print(dir(sel.Shape))
          print(sel.InList)
          print(sel.OutList)
          #obj.OutList = sel.OutList
          if len(sel.InList) > 0 :
             parent = sel.InList[0]
             print('parent : '+parent.Label)
             print(parent.OutList)
             obj = parent.newObject('Part::FeaturePython',sel.Label+'_Scale')
             toScale(obj, sel.Shape)
             ViewProvider(obj.ViewObject)
 
             #for i in range(len(parent.OutList)) :
             #    if parent.OutList[i] == sel :
             #       parent.OutList[i] = obj
             #       obj.Label = sel.Label + '_Scale'
          else :
             obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Scale')
             toScale(obj, sel.Shape)
             ViewProvider(obj.ViewObject)
          for i in sel.OutList :
              obj.addObject(i) 
          FreeCAD.ActiveDocument.removeObject(sel.Name)
          #FreeCADGui.updateGui()            
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

class toTransformFeature :

    def Activated(self):
      from .toSObjects import toTransform, ViewProvider

      for sel in FreeCADGui.Selection.getSelection() :
          print('Selected')
          print(sel.Label)
          print(sel.TypeId)
          print(dir(sel.Shape))
          s = sel.Shape
          t = sel.Shape.copy()
          m = FreeCAD.Matrix()
          print(s.BoundBox.XMin)
          print(s.BoundBox.XMax)
          print(s.CenterOfMass)
          print(s.CenterOfMass.x)
          print(s.CenterOfMass.y)
          print(s.CenterOfMass.z)
          print(dir(s.CenterOfMass))
          print(dir(sel))
          print(dir(sel.Placement))
          sel.Placement.Base = s.CenterOfMass
          print(sel.Placement)
          v = s.CenterOfMass
          vt = v.negative()
          print(vt)
          #com = s.CenterOfMass
          #m.move(com.x,com.y,com.z)
          m.move(-s.CenterOfMass.x+5, -s.CenterOfMass.y+5, -s.CenterOfMass.z)
          #m.move(com[0],com[1],com[2])
          m.scale(1,1,1)
          #s = s.transformGeometry(m)
          #t.transformShape(m)
          #t.translate(s.CenterOfMass.negative)
          t.translate(vt)
          sel.Shape = t
          FreeCADGui.updateGui()

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'toTransform', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('toTransformFeature',\
                'To Transform'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('toTransformFeature',\
                'To Transform')}

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
FreeCADGui.addCommand('toSPlaneCommand',toSPlaneFeature())
FreeCADGui.addCommand('toScaleCommand',toScaleFeature())
FreeCADGui.addCommand('toTransformCommand',toTransformFeature())
FreeCADGui.addCommand('toShapeInfoCommand',toShapeInfoFeature())
