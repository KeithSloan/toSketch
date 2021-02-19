# toSketch 

## ( FreeCAD workbench to add toSketch Facility )

The main emphasis of the facilities in this workbench are to help with remodelling of
existing models. When a STEP model is imported into FreeCAD you have a a viewable model
but no details about how it was created or Parametric properties that you can change.

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
                           
### Sketch to Macro ( Alpha - Under Development )

* Select a sketch
* Click on ToMacro

   Creates a macro name (sketch.FCMacro) in the user Macro directory
   
Currently supports ( More to follow )
    
      * Points
      * Lines
      * Circles
      * ArcOfCircle
      * BSpline ( Initial Attempt )
      * Ellipse
      
When executing the macro

     If there is a an ActiveSketch, the geometry is added, otherwise a new sketch is created.
     
Constraints

     The following types of constraints are exported if present in the selected sketch.
     
         * Coincident
         * Vertical
         * Horizontal
 
                              
### Section a Mesh Cross Section : to CurveFit ( Alpha - Under Development )

Requires NURBS-Python ( geomdl ) see https://nurbs-python.readthedocs.io/en/5.x/

* To Install
   
    * From FreeCAD python console
    * **import os**
    * **print(os.environ)**
    * Note one of the library paths [path]
    * **pip3 install geomdl -t [path]**

* To Use

    * Load/Create a Mesh
    * Use Mesh Design workbench to create a section 
       
        Toobar - **Meshes | Cutting | Cross-Sections**

        Creates a Mesh Cross-Section
        
    * Select Cross-Section in Tree View, click on 'To Sketch' icon

        Creates a Raw Sketch
      
    * Select Created Sketch, click on 'To CurveFit' icon

        Creates a Sketch with some line and Curve Fitting
        
## Constraints

Note: Ideally constraints should be set on a geometric basis, however there is always
      the option to fix all points with the installable Macro SketcherFixAllPoints.FCMacro
      see Addon Manager for installation. 
 
                           
## The following are intended to help with Objects created via import of STEP files                           
                           
### Create Scale Object : to Scale

Aimed at scaling objects imported from a STEP file, provides the ability to scale a
selected Object as follows

* Select the object to be Scaled.
* Click on the to Scale icon
* A new object is created where the Shape from the selected Object is stored.
* The original selected object is then deleted
* By changing the Objects Properties from the inital values of ONE the Shape of the object can be reScaled

     
### Reset Origin

When STEP files are imported into FreeCAD their Placements are all set to zero and the Shapes are all created accordingly.
This means if you try and Rotate an object that has been imported into FreeCAD it does not rotate correctly.

Selecting an Object and clicking on the Reset Origin icon results in the following

 * A new PartFeaturePython object is created and stores a copy of the selected objects Shape.
 * The Objects Placement is set based on the Shapes Bounding box and drawn at the same position.
 * The Selected Object is removed
 
 The display of the Object will not change, but the Placement will be updated and it can be correctly rotated.
     
 For the new object
      
 * The Origin can be changed via the Object Type Parameter using the Parameter window between
     
    * min x/y/z 
    * Center of Mass
    * Original ( as created by STEP import )
           
 * The parameter window shows readonly Bounding box info
 * The Origin type can be changed via the Objects Parameter Placement setting.
 * Apart from when the Origin Type is set to Original the Object should now rotate correctly
 
 ## Acknowledgments
 
 Thanks to the following FreeCAD forum members
 
     * suzanne.soy
     * wmayer
     
 Icons thanks to jmaustpc    
     
          

