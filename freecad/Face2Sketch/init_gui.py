# Face2Sketch wrkbench gui init module
#
# Gathering all the information to start FreeCAD
# This is the second one of three init scripts, the third one
# runs when the gui is up

#***************************************************************************
#*   (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Juergen Riegel 2002                                                   *
#*                                                                         *
#* Also copyright Keith Sloan                                              * 
#***************************************************************************/

#import FreeCAD
#from FreeCAD import *
import FreeCAD
#import PartGui
import FreeCADGui
#from freecad.gdml import F2SCommands, F2SResources
from freecad.Face2Sketch import F2SCommands

def joinDir(path) :
    import os
    __dirname__ = os.path.dirname(__file__)
    return(os.path.join(__dirname__,path))

class Face2Sketch_Workbench ( FreeCADGui.Workbench ):

#    import FreeCAD

    "Face2Sketch workbench object"
    def __init__(self):
        self.__class__.Icon = joinDir("Resources/icons/F2SWorkbench.svg")
        self.__class__.MenuText = "Face2Sketch"
        self.__class__.ToolTip = "Face2Sketch workbench"

    def Initialize(self):
        def QT_TRANSLATE_NOOP(scope, text):
            return text
        
        #import GDMLCommands, GDMLResources
        #import F2SCommands
        commands=['Face2SketchCommand']

        toolbarcommands=['Face2SketchCommand']

        self.appendToolbar(QT_TRANSLATE_NOOP('Workbench','F2S_Tools'),toolbarcommands)
        self.appendMenu('Face2Sketch',commands)
        FreeCADGui.addIconPath(joinDir("Resources/icons"))
        FreeCADGui.addLanguagePath(joinDir("Resources/translations"))
        #FreeCADGui.addPreferencePage(joinDir("Resources/ui/Face2Sketch-base.ui"),"Face2Sketch")

    def Activated(self):
        "This function is executed when the workbench is activated"
        print ("Activated")
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return
    
    def GetClassName(self):
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(Face2Sketch_Workbench())

