# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the ToSketch addon.

################################################################################
#                                                                              #
#   Copyright (c) 2002 Juergen Riegel ( juergen.riegel@web.de )                #
#   Copyright (c) 2021 Keith Sloan ( keith@sloan-home.co.uk )                  #
#                                                                              #
#   This library is free software; you can redistribute it and/or modify it    #
#   under the terms of the GNU Lesser General Public License as published      #
#   by the Free Software Foundation; either version 2.1 of the License, or     #
#   (at your option) any later version.                                        #
#                                                                              #
#   This library is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                       #
#                                                                              #
#   See the GNU Lesser General Public License for more details.                #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public License   #
#   along with this library; if not, write to the Free Software Foundation,    # 
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA           #
#                                                                              #
################################################################################

# toSketch workbench gui init module
#
# Gathering all the information to start FreeCAD
# This is the second one of three init scripts, the third one
# runs when the gui is up

#import FreeCAD
#from FreeCAD import *
import FreeCAD
#import PartGui
import FreeCADGui
from freecad.toSketch import toSCommands

def joinDir(path) :
    import os
    __dirname__ = os.path.dirname(__file__)
    return(os.path.join(__dirname__,path))

class toSketch_Workbench ( FreeCADGui.Workbench ):

#    import FreeCAD

    "to workbench object"
    def __init__(self):
        self.__class__.Icon = joinDir("Resources/icons/toSWorkbench.svg")
        self.__class__.MenuText = "toSketch"
        self.__class__.ToolTip = "toSketch workbench"

    def Initialize(self):
        def QT_TRANSLATE_NOOP(scope, text):
            return text
        
        #import 2SCommands
        commands=['toSPlaneCommand', \
                    'Plane2PartPlaneCommand', \
                    'toSketchCommand', \
                    'section2SketchCommand', \
                    'removeOuterBoxCommand', \
                    #'addBboxCommand', \
                    'toMacroCommand', \
                    'ConstraintsGroupCmd', \
                    'toLineCurveFitCommand', \
                    'bSpline2ArcCommand', \
                    'toCurveFitCommand', \
                    'toScaleCommand','toResetOriginCommand']

        toolbarcommands=['toSPlaneCommand', \
                    'Plane2PartPlaneCommand', \
                    'toSketchCommand', \
                    'section2SketchCommand', \
                    'removeOuterBoxCommand', \
                    #'addBboxCommand', \
                    'toMacroCommand', \
                    'ConstraintsGroupCmd', \
                    'toLineCurveFitCommand', \
                    'toCurveFitCommand', \
                    'bSpline2ArcCommand', \
                    'toScaleCommand','toResetOriginCommand']

        import PartGui
        parttoolbarcommands =['Part_Loft']
        self.appendToolbar(QT_TRANSLATE_NOOP('Workbench', \
                           'toSketch_Tools'),toolbarcommands)
        self.appendToolbar(QT_TRANSLATE_NOOP('Workbench', \
                           'toSketch_Tools Part Tools'),parttoolbarcommands)
        self.appendMenu('toSketch',commands)
        FreeCADGui.addIconPath(joinDir("Resources/icons"))
        FreeCADGui.addLanguagePath(joinDir("Resources/translations"))
        #FreeCADGui.addPreferencePage(joinDir("Resources/ui/toSketch-base.ui"),"Face2Sketch")

    def Activated(self):
        "This function is executed when the workbench is activated"
        print ("Activated")
        #actDoc = FreeCAD.ActiveDocument
        #if actDoc is not None :
        #   objs = actDoc.Objects
        #   if objs is not None :
        #      for obj in objs :
        #          obj.ViewObject.Visibility = True
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return
    
    def GetClassName(self):
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(toSketch_Workbench())

