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
This Script includes the GUI Commands of the GDML module
'''

import FreeCAD,FreeCADGui, Part, Draft, Sketcher
from PySide import QtGui, QtCore

class Face2SketchFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        #from .GDMLObjects import GDMLBox, ViewProvider
#        for obj in FreeCADGui.Selection.getSelection():
        for sel in FreeCADGui.Selection.getSelectionEx() :
            #if len(obj.InList) == 0: # allowed only for for top level objects
            #cycle(obj)
            print("Selected")
            print(sel.HasSubObjects)
            print(sel.Object)
            print(sel.Object.Label)
            print(sel.SubObjects)
            print(sel.SubObjects[0])
            print(sel.SubObjects[0].ShapeType)
            print(sel.SubObjects[0].Surface)
            if str(sel.SubObjects[0].Surface) == '<Plane object>' :
               print('Planar')
               #print(dir(sel.SubObjects[0].Wires))
               #print(dir(sel.SubObjects[0].SubShapes))
               print('Print Dir Surface')
               print(dir(sel.SubObjects[0].Surface))
               #shape = sel.SubObjects[0].Surface.toShape()
               shape = sel.SubObjects[0]
               print('Selected Shape')
               print(shape)
               print(shape.TypeId)
               print(shape.ShapeType)
               print('Sub Shapes')
               print(shape.SubShapes)
               print('Shape Vertexes')
               print(shape.Vertexes)
               print('Shape Wires')
               print(len(shape.Wires))
               print(shape.Wires)
               #newWire = Draft.makeWire(shape.Wires[0])
               #print(newWire)
               #Draft.makeSketch(newWire, autoconstraints=False, addTo=None, delete=False, name="Sketch", radiusPrecision=-1)
               Draft.draftify(shape)
               Draft.makeSketch(shape, autoconstraints=False, addTo=None, delete=False, name="Sketch2", radiusPrecision=-1)
               #print(ret)
               # Wire is depreciated replaced by OuterWire
               #print(shape.Wire)
               print('Outer Wire')
               print(shape.OuterWire)
               print('Wire Type')
               print(shape.OuterWire.TypeId)
               print('Wire ShapeType')
               #print(shape.OuterWire.ShapeType)
               print('Wire Edges')
               print(shape.OuterWire.Edges)
               #print(shape.OuterWire.Length)
               print('Wire Vertexes')
               print(shape.OuterWire.Vertexes)
               print(shape.OuterWire.Wires)

               print(dir(shape.OuterWire))
               print(shape.Shells)
               #print(shape.childShapes)
               #print(shape.defeaturing)
               print('Print Dir Shape')
               print(dir(shape))
               shape.exportStep('/tmp/exported.step')
               shape.exportBrep('/tmp/exported.brep')

            #obj1 = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject','one')
            #obj1.Shape = shape
            #print('Part2DObject')
            #print(obj1)
            #print(dir(obj1))
            #obj2 = FreeCAD.ActiveDocument.addObject('Sketcher::SketcherObjectPython','two')
            #print(dir(obj2))

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'Face2SketchFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('Face2SketchFeature',\
                'Face 2 Sketch'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('Face2SketchFeature',\
                'Face 2 Sketch')}

FreeCADGui.addCommand('Face2SketchCommand',Face2SketchFeature())
