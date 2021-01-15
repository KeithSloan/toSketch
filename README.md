# toSketch 

## ( FreeCAD workbench to add toSketch Facility )

## Installation

* Clone into FreeCAD's Mod directory

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
                           
### create Scale Object : to Scale

Aimed at scaling objects imported from a step file, provide the ability to scale a selected Object as follows

     * Select the object to be Scaled.
     * Click on the to Scale icon
     * A new object is created where the Shape from the selected Object is stored.
     * By changing the Objects Properties from the inital values of **one** the Shape of the object is reScale
     * The original selected object is deleted

