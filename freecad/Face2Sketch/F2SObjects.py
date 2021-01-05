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

import FreeCAD, Part

class F2SPlane :

    def __init__(self,obj) :
        AxisList = ['XY Plane','XZ Plane','YZ Plane','Custom']
        obj.addProperty("App::PropertyEnumeration","Axis","Base", \
            "Axis").Axis=AxisList
        obj.addProperty("App::PropertyFloat","Offset","Base", \
            "Offset").Offset=0.0
        obj.addProperty("App::PropertyFloat","XDir","Custom Axis", \
            "Custom XDir").XDir=0.0
        obj.addProperty("App::PropertyFloat","YDir","Custom Axis", \
            "Custom YDir").YDir=0.0
        obj.addProperty("App::PropertyFloat","ZDir","Custom Axis", \
             "Custom ZDir").ZDir=1.0
        obj.setEditorMode("Placement",2)
        self.disableAxisParms(obj)
        obj.Proxy = self

    def enableAxisParms(self, obj) :
        print('Enable Axis Parms')
        obj.setEditorMode("XDir",0)
        obj.setEditorMode("YDir",0)
        obj.setEditorMode("ZDir",0)

    def disableAxisParms(self, obj) :
        print('Disable Axis Parms')
        obj.setEditorMode("XDir",1)
        obj.setEditorMode("YDir",1)
        obj.setEditorMode("ZDir",1)

    def onChanged(self, fp, prop):
        print(fp.Label+" State : "+str(fp.State)+" prop : "+prop)
        if 'Axis' in prop :
           print('Axis set to : '+fp.Axis)
           if fp.Axis == 'Custom' :
              self.enableAxisParms(fp)
           else :
              self.disableAxisParms(fp)
        self.updateGeometry(fp)

    def getPlaneParms(self, fp) :
        if fp.Axis == 'Custom' : 
           self.dir = FreeCAD.Vector(fp.XDir, fp.YDir, fp.ZDir)
           self.point = FreeCAD.Vector(0.0, 0.0, 0.0)
        elif fp.Axis == 'XY Plane' :
           self.dir = FreeCAD.Vector(0.0, 0.0, 1.0)
           self.point = FreeCAD.Vector(fp.Offset, 0.0, 0.0)
        elif fp.Axis == 'XZPlane' :
           self.dir = FreeCAD.Vector(0.0, 1.0, 0.0)
           self.point = FreeCAD.Vector(0.0, fp.Offset, 0.0)
        elif fp.Axis == 'YZPlane' :
           self.dir = FreeCAD.Vector(1.0, 0.0, 0.0)
           self.point = FreeCAD.Vector(0.0, 0.0, fp.Offset)
        else :
           print('Invalid Axis')
           exit(3)

    def createGeometry(self, fp) :
        print('create Geometry')
        #print(fp.Shape)
        if hasattr(self, 'Plane') == False :
           self.getPlaneParms(fp)
           self.Plane = Part.makePlane(1000,1000,self.point, self.dir)
           fp.Shape = self.Plane
        
    def updateGeometry(self, fp) :
        print('update Geometry')
        #if self.Plane is None :
        #   self.getPlaneParms(fp)
        #   self.Plane = Part.makePlane(1000,1000,self.point, self.dir)
        #   fp.Shape = self.Plane
        print(dir(fp.Shape))
        
    def execute(self,fp):
        print('execute')
        self.createGeometry(fp)

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

   def attach(self,obj):
       return
 
   def updateData(self, fp, prop):
       '''If a property of the handled feature has changed we have the chance to handle this here'''
       print('updateData')
       #pass
       return

   def getDisplayModes(self,obj):
       return []

   def getDefaultDisplayMode(self):
        """
        Return the name of the default display mode. It must be defined in getDisplayModes.
        """
        return "Shaded"

   def setDisplayMode(self,mode):
        """
        Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        return mode

   def onChanged(self, vp, prop):
       '''Here we can do something when a single property got changed'''
       print('onChanged')

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

