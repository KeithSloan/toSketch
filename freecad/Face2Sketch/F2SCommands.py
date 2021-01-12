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
This Script includes the GUI Commands of the F2S module
'''

import FreeCAD,FreeCADGui, Part, Draft, Sketcher, Show
from PySide import QtGui, QtCore

class Face2SketchFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        #   for obj in FreeCADGui.Selection.getSelection():
        for sel in FreeCADGui.Selection.getSelectionEx() :
            #if len(obj.InList) == 0: # allowed only for for top level objects
            #cycle(obj)
            print("Selected")
            if sel.HasSubObjects == True :
               if str(sel.SubObjects[0].Surface) == '<Plane object>' :
                  print('Planar')
                  shape = sel.SubObjects[0]
                  #shape.exportStep('/tmp/exported.step')
                  #shape.exportBrep('/tmp/exported.brep')
                  Draft.draftify(shape, makeblock=False, delete=True)
                  try :
                      Draft.makeSketch(shape, autoconstraints=True, \
                         addTo=None, delete=False, name="Sketch",  \
                         radiusPrecision=-1)
                  except :
                      Draft.makeSketch(shape, autoconstraints=False, \
                         addTo=None, delete=False, name="Sketch",  \
                         radiusPrecision=-1)
                  FreeCADGui.ActiveDocument.setEdit('Sketch',0)

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'Face2Sketch', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('Face2SketchFeature',\
                'Face 2 Sketch'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('Face2SketchFeature',\
                'Face 2 Sketch')}

class F2SPlaneFeature :    

    def Activated(self) :
        from .F2SObjects import F2SPlane, ViewProvider

        obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython', \
                   'Plane')
        F2SPlane(obj)
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
        return {'Pixmap'  : 'F2SPlane', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('F2SPlaneFeature',\
                'F2SPlane'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('Face2SketchFeature',\
                'F2SPlane')}

FreeCADGui.addCommand('Face2SketchCommand',Face2SketchFeature())
FreeCADGui.addCommand('F2SPlaneCommand',F2SPlaneFeature())
