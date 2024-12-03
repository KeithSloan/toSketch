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

__title__="FreeCAD toSketch Workbench - Objects"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

import FreeCAD, Part, Draft

class toSPlane :

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
        obj.addProperty("App::PropertyFloat","Length","Plane", \
             "Length").Length = 500.0 
        obj.addProperty("App::PropertyFloat","Width","Plane", \
             "Width").Width = 500.0 
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

        if 'Placement' in prop :
           print(fp.Placement)

        if 'Offset' in prop :
           self.updateGeometry(fp)

        if 'Length' in prop or 'Width' in prop :
           fp.Shape = Part.makePlane(fp.Length,fp.Width, \
                      FreeCAD.Vector(-fp.Length/2,-fp.Width/2),\
                      FreeCAD.Vector(0,0,1))
           self.updateGeometry(fp)

    def getPlaneParms(self, fp) :
        # Note self values not saved acros file save and open
        # so getPlaneParms need to be called before any use of them
        print('getplaneParms')
        print(fp.Axis)
        if fp.Axis == 'Custom' : 
           self.dir  = FreeCAD.Vector(fp.XDir, fp.YDir, fp.ZDir)
           self.point = FreeCAD.Vector(0.0, 0.0, 0.0)
        elif fp.Axis == 'XY Plane' :
           self.dir  = FreeCAD.Vector(0.0, 0.0, 1.0)
           self.point = FreeCAD.Vector(0.0,0.0,fp.Offset)
        elif fp.Axis == 'XZ Plane' :
           self.dir  = FreeCAD.Vector(0.0, 1.0, 0.0)
           self.point = FreeCAD.Vector(0.0,fp.Offset,0.0)
        elif fp.Axis == 'YZ Plane' :
           self.dir  = FreeCAD.Vector(1.0, 0.0, 0.0)
           self.point = FreeCAD.Vector(fp.Offset,0.0,0.0)
        else :
           print('Invalid Axis')
           exit(3)
        return self.dir, self.point   

    def getPartPlane(self, fp) :
        # Note self values not saved acros file save and open
        # so getPlaneParms need to be called before any use of them
        print('getPartPlane')
        #print(dir(fp))
        print(fp.Axis)
        if fp.Axis == 'Custom' : 
           normal  = FreeCAD.Vector(fp.XDir, fp.YDir, fp.ZDir)
           self.point = FreeCAD.Vector(0.0, 0.0, 0.0)
        elif fp.Axis == 'XY Plane' :
           normal = FreeCAD.Vector(0.0, 0.0, 1.0)
           point = FreeCAD.Vector(0.0,0.0,fp.Offset)
        elif fp.Axis == 'XZ Plane' :
           normal  = FreeCAD.Vector(0.0, 1.0, 0.0)
           point = FreeCAD.Vector(0.0,fp.Offset,0.0)
        elif fp.Axis == 'YZ Plane' :
           normal  = FreeCAD.Vector(1.0, 0.0, 0.0)
           point = FreeCAD.Vector(fp.Offset,0.0,0.0)
        else :
           print('Invalid Axis')
           exit(3)
        distance = fp.Offset
        position = normal * distance
        plane = Part.Plane()
        plane.Position = position
        plane.Axis = normal
        #plane = Part.makePlane(fp.Length, fp.Width, position, normal)
        return plane.toShape(), point

    def getMeshPlane(self, fp) :
        import Mesh
        # Note self values not saved acros file save and open
        # so getPlaneParms need to be called before any use of them
        print('getMeshPlane')
        #print(dir(fp))
        print(fp.Axis)
        if fp.Axis == 'Custom' : 
           normal  = FreeCAD.Vector(fp.XDir, fp.YDir, fp.ZDir)
           self.point = FreeCAD.Vector(0.0, 0.0, 0.0)
        elif fp.Axis == 'XY Plane' :
           normal = FreeCAD.Vector(0.0, 0.0, 1.0)
           point = FreeCAD.Vector(0.0,0.0,fp.Offset)
        elif fp.Axis == 'XZ Plane' :
           normal  = FreeCAD.Vector(0.0, 1.0, 0.0)
           point = FreeCAD.Vector(0.0,fp.Offset,0.0)
        elif fp.Axis == 'YZ Plane' :
           normal  = FreeCAD.Vector(1.0, 0.0, 0.0)
           point = FreeCAD.Vector(fp.Offset,0.0,0.0)
        else :
           print('Invalid Axis')
           exit(3)
        distance = fp.Offset
        position = normal * distance
        plane = Part.Plane()
        plane.Position = position
        plane.Axis = normal
        #plane = Part.makePlane(fp.Length, fp.Width, position, normal)
        #return plane.toShape(), point
        return Mesh.Mesh(plane)

    def createGeometry(self, fp) :
        print('create Geometry')
        print(fp.Placement.Base)
        print(fp.Placement.Rotation)
        if hasattr(self, 'Plane') == False :
           print('Create Plane')
           #self.getPlaneParms(fp)
           self.Plane = Part.makePlane(fp.Length, fp.Width, \
               FreeCAD.Vector(-250,-250,0),FreeCAD.Vector(0,0,1))
           fp.Shape = self.Plane
        
    def updateGeometry(self, fp) :
        print('update Geometry')
        print(fp.Placement)
        self.getPlaneParms(fp)
        print('Current plane parms')
        print('Point : '+str(self.point))
        print('Dir   : '+str(self.dir))
        #self.Plane.Placement.Base = self.point
        fp.Placement.Base = self.point
        #self.Plane.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1),\
        fp.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1),\
              self.dir)
        #print(self.Plane.Placement.Base)
        #print(self.Plane.Placement.Rotation)
        # Following line would update Shape and drive onChanged Shape
        #fp.Shape = self.Plane
        
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

class toScale() :
   def __init__(self, obj, shape, bbox) :
       print('Scale Init')
       obj.Proxy = self
       obj.addProperty("App::PropertyFloat","ScaleX","Base", \
              "Scale").ScaleX = 1.0
       obj.addProperty("App::PropertyFloat","ScaleY","Base", \
              "Scale").ScaleY = 1.0
       obj.addProperty("App::PropertyFloat","ScaleZ","Base", \
              "Scale").ScaleZ = 1.0
       
       obj.addProperty("Part::PropertyPartShape","saveShape","Base", \
              "Saved Shape").saveShape = shape
       self.Shape = obj.saveShape

   def onChanged(self, fp, prop) :
       print(fp.Label+" State : "+str(fp.State)+" prop : "+prop)
       if 'ScaleX' in prop or 'ScaleY' in prop or 'ScaleZ' in prop :
           self.updateGeometry(fp)

   def updateGeometry(self, fp) :
       print('Update Geometry')
       if hasattr(fp,'saveShape') :
          s = fp.saveShape.copy()
          #print(s.BoundBox)
          #print(dir(s))
          m = FreeCAD.Matrix()
          cx = (s.BoundBox.XMin+s.BoundBox.XMax)*(1.0-fp.ScaleX)/(2.0*fp.ScaleX)
          #print('cx : '+str(cx))
          cy = (s.BoundBox.YMin+s.BoundBox.YMax)*(1.0-fp.ScaleY)/(2.0*fp.ScaleY)
          #print('cy : '+str(cy))
          cz = (s.BoundBox.ZMin+s.BoundBox.ZMax)*(1.0-fp.ScaleZ)/(2.0*fp.ScaleZ)
          #print('cz : '+str(cz))
          m.move(FreeCAD.Vector(cx,cy,cz))
          m.scale(fp.ScaleX,fp.ScaleY,fp.ScaleZ)
          s = s.transformGeometry(m)
          fp.Shape = s

   def execute(self,fp):
       print('execute')
       self.updateGeometry(fp)

   def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None

   def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None

class toResetOrigin() :
   
   def __init__(self, obj, shape, bbox) :
       obj.Proxy = self
       self.TypeList = ['Min x/y/z','Center of Mass','Original']
       obj.addProperty("App::PropertyEnumeration","Type","Base", \
           "Reset Origin To").Type = self.TypeList
       obj.addProperty("App::PropertyFloat","MinX","Bounding Box", \
              "Bounding Box Min X")
       obj.setEditorMode('MinX',1)
       obj.addProperty("App::PropertyFloat","MaxX","Bounding Box", \
              "Bounding Box Max X")
       obj.setEditorMode('MaxX',1)
       obj.addProperty("App::PropertyFloat","LengthX","Bounding Box", \
              "Bounding Box X Length").LengthX = bbox.XLength
       obj.setEditorMode('LengthX',1)
       obj.addProperty("App::PropertyFloat","MinY","Bounding Box", \
              "Bounding Box Min Y")
       obj.setEditorMode('MinY',1)
       obj.addProperty("App::PropertyFloat","MaxY","Bounding Box", \
              "Bounding Box Max Y")
       obj.setEditorMode('MaxY',1)
       obj.addProperty("App::PropertyFloat","LengthY","Bounding Box", \
              "Bounding Box Y Length").LengthY = bbox.YLength
       obj.setEditorMode('LengthY',1)
       obj.addProperty("App::PropertyFloat","MinZ","Bounding Box", \
              "Bounding Box Min Z")
       obj.setEditorMode('MinZ',1)
       obj.addProperty("App::PropertyFloat","MaxZ","Bounding Box", \
              "Bounding Box Max Z")
       obj.setEditorMode('MaxZ',1)
       obj.addProperty("App::PropertyFloat","LengthZ","Bounding Box", \
              "Bounding Box Z Length").LengthZ = bbox.ZLength
       obj.setEditorMode('LengthZ',1)
       obj.addProperty("App::PropertyBool","SavedFlag","Base", \
           " Saved Flag ").SavedFlag = False
       obj.setEditorMode('SavedFlag',2)
       obj.addProperty("App::PropertyVector","SavedBase","Base", \
           " Saved Base ").SavedBase = FreeCAD.Vector(0,0,0)
       obj.setEditorMode('SavedBase',2)
       obj.addProperty("Part::PropertyPartShape","saveShape","Base", \
              "Saved Shape").saveShape = shape
       self.Shape = obj.saveShape

   def onChanged(self, fp, prop) :
       print(fp.Label+" State : "+str(fp.State)+" prop : "+prop)
       if 'Type' in prop :
          #fp.SavedBase = fp.Placement 
          #fp.SavedFlag = False
          self.updateGeometry(fp, True)

       if 'Placement' in prop :
          print(fp.Placement.Base)
          fp.SavedBase = fp.Placement.Base
          fp.SavedFlag = True
          
   def updateGeometry(self, fp, flag) :
       print('Update Geometry')
       if hasattr(fp,'saveShape') :
          s = fp.saveShape.copy()
          t = self.TypeList.index(fp.Type)
          if t == 0 :
             v = FreeCAD.Vector(s.BoundBox.XMin, \
                    s.BoundBox.YMin, s.BoundBox.ZMin)
          if t == 1 :
             v = s.CenterOfMass
          if t == 2 :
             v = FreeCAD.Vector(0,0,0)          
          vt = v.negative()
          m = FreeCAD.Matrix()
          m.move(vt)
          m.scale(1,1,1)
          s = s.transformGeometry(m)
          #s.translate(vt)
          fp.Shape = s
          if fp.SavedFlag  == False or flag == True :
             fp.Placement.Base = v
             fp.SavedFlag = True
          #else : 
          #   fp.Placement.Base = fp.SavedBase
          fp.MinX = s.BoundBox.XMin
          fp.MinY = s.BoundBox.YMin
          fp.MinZ = s.BoundBox.ZMin
          fp.MaxX = s.BoundBox.XMax
          fp.MaxY = s.BoundBox.YMax
          fp.MaxZ = s.BoundBox.ZMax

   def execute(self,fp):
        print('execute')
        self.updateGeometry(fp, False)

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
       if hasattr(obj, "Proxy"):
            obj.Proxy = self

   def attach(self,obj):
       return
 
   def updateData(self, fp, prop):
       '''If a property of the handled feature has changed we have the chance to handle this here'''
       #print('updateData ViewProvider')
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
       #print('onChanged Viewprovider')

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

