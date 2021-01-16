# toSketch 

## ( FreeCAD workbench to add toSketch Facility )

## Installation

* Using Addon Manager

  * Click on Configure
  * Enter https://github.com/KeithSloan/toSketch.git

## Alternative Installation

Clone into FreeCAD's Mod directory

   * Change to FreeCAD Mod directory
   * **git clone https://github.com/KeithSloan/toSketch.git**

* Start/Restart FreeCAD

## Use

### Face to Sketch : to Sketch

* Select a single planar Face
* Click on toSketch Icon - Should create a new sketch from the selected Face

### Create Plane : to Plane

* Select the toPlane Icon to create a Plane
* Edit properties to adjust Plane

### Section Plane to Sketch : to Sketch

* Select Plane in treeView
* Click on toSketch Icon - Should create a section of the Plane and other objects
                           that is then opened as a new sketch
                           
## The following are intended to help with Objects created via import of STEP files                           
                           
### Create Scale Object : to Scale

Aimed at scaling objects imported from a STEP file, provides the ability to scale a
selected Object as follows

     * Select the object to be Scaled.
     * Click on the to Scale icon
     * A new object is created where the Shape from the selected Object is stored.
     * By changing the Objects Properties from the inital values of ONE the Shape of the object is reScale
     * The original selected object is deleted
     
### Reset Origin

When STEP files are imported into FreeCAD their Placements are all set to zero and the Shapes are all created accordingly,
this means if you try and Rotate an object that has been imported into FreeCAD it does not rotate correctly.
Selecting an Object and clicking on the Reset Origin icon results in the following.

     * A new PartFeaturePython object is created and stores a copy of the objects Shape.
     * The Objects Placement is set based on the Shapes Bounding box and drawn at the same position.
     * The Selected Object is removed
     
     For the new object
      
        * The Origin can be changed via the Object Parameter using the Parameter window between
     
            * min x/y/z 
            * Center of Mass
            * Original ( as created by STEP import )
           
        * The parameter window shows readonly Bounding box info
        * The Origin type can be changed via the Objects Parameter Placement setting.
        * Apart from when the Origin Type is set to Original the Object should now rotate corretly
          

