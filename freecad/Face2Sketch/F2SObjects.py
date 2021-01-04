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

__title__="FreeCAD Face2Sketch Workbench - Objects"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

class F2SPlane :

    def __init__(self,obj) :
        obj.addProperty("App::PropertyBool","xAxis","Plane", \
              "X Axis enabled?").xAxis=False
        obj.addProperty("App::PropertyFloat","xOffset","Plane", \
              "X Offset").xOffset=0.0
        obj.addProperty("App::PropertyBool","yAxis","Plane", \
              "Y Axis enabled?").yAxis=False
        obj.addProperty("App::PropertyFloat","yOffset","Plane", \
              "Y Offset").yOffset=0.0
        obj.addProperty("App::PropertyBool","zAxis","Plane", \
              "Z Axis enabled?").zAxis=False
        obj.addProperty("App::PropertyFloat","zOffset","Plane", \
            "Z Offset").zOffset=0.0
        obj.addProperty("App::PropertyBool","Axis","Custom Axis", \
            "Custom enabled?").Axis=False
        obj.addProperty("App::PropertyFloat","Offset","Custom Axis", \
            "Custom Offset").Offset=0.0
        obj.addProperty("App::PropertyFloat","Xdir","Custom Axis", \
            "Custom XDir").Xdir=0.0
        obj.addProperty("App::PropertyFloat","Ydir","Custom Axis", \
            "Custom YDir").Ydir=0.0
        obj.addProperty("App::PropertyFloat","Zdir","Custom Axis", \
             "Custom ZDir").Zdir=0.0

    def onChange(self, fp, prop):
        print(fp.Label+" State : "+str(fp.State)+" prop : "+prop)
        if 'custAxis' in fp.State :
           fp.xAxis = fp.yAxis = fp.z,zAxis = False
        
        if 'xAxis' in fp.State :
           fp.custAxis = False

        if 'yAxis' in fp.State :
           fp.custAxis = False

        if 'zAxis' in fp.State :
           fp.custAxis = False

    def createGeometry(self, fp) :
        print('create Geometry')
        
    def execute(self,fp):
        print('execute')

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None
 
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None

class ViewProvider():
   def __init__(self, obj):
       '''Set this object to the proxy object of the actual view provider'''
       obj.Proxy = self
 
   def updateData(self, fp, prop):
       '''If a property of the handled feature has changed we have the chance to handle this here'''

   def setDisplayMode(self,mode):
       '''Map the display mode defined in attach with those defined in getDisplayModes.\
               Since they have the same names nothing needs to be done. This method is optional'''
       return mode
 
   def onChanged(self, vp, prop):
       '''Here we can do something when a single property got changed'''

   def getIcon(self):
       '''Return the icon in XPM format which will appear in the tree view. This method is\
               optional and if not defined a default icon is shown.'''
       return """
           /* XPM */
           static const char * ViewProviderBox_xpm[] = {
           "16 16 6 1",
           "   c None",
           ".  c #141010",
           "+  c #615BD2",
           "@  c #C39D55",
           "#  c #000000",
           "$  c #57C355",
           "        ........",
           "   ......++..+..",
           "   .@@@@.++..++.",
           "   .@@@@.++..++.",
           "   .@@  .++++++.",
           "  ..@@  .++..++.",
           "###@@@@ .++..++.",
           "##$.@@$#.++++++.",
           "#$#$.$$$........",
           "#$$#######      ",
           "#$$#$$$$$#      ",
           "#$$#$$$$$#      ",
           "#$$#$$$$$#      ",
           " #$#$$$$$#      ",
           "  ##$$$$$#      ",
           "   #######      "};
           """
   def __getstate__(self):
       '''When saving the document this object gets stored using Python's json module.\
               Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
               to return a tuple of all serializable objects or None.'''
       return None

   def __setstate__(self,state):
       '''When restoring the serialized object from document we have the chance to set some internals here.\
               Since no data were serialized nothing needs to be done here.'''
       return None

