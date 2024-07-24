# HEC-RAS-Rain-on-Grid-Automation
This Python script automates the process of setting up and running a Rain on Grid 2D Model in HEC-RAS using pyautogui. The script performs all necessary steps, from creating a new project to saving the model outputs, thus streamlining the workflow for hydrological modeling in HEC-RAS.

## Features
 - Create New HEC-RAS Project: Initializes a new HEC-RAS project and completes the project information.
 - Model Setup: Sets up the model by configuring geometry, land cover, and soils layers.
   - Geometry Setup:
     - Set Projection
     - Create New RAS Terrain
     - Create Land Cover and Soils Layers
     - Add New Geometry
     - Define 2D Flow Areas Perimeters and Breaklines
     - Add Boundary Conditions
 - 2D Flow Area Setup:
   - Force Mesh Recomputation
   - Edit Breakline Properties
   - Regenerate Grid
   - Fix All Meshes (15 Loops)
 - Rain on Grid 2D Model Plan Setup:
   - Rainfall Input Setup
   - Simulation Settings Setup
 - Run the Model:
   - Execute the model run
   - Display user inputs and model outputs
   - Save depth, velocity, and WSE layer outputs
 - Close HEC-RAS: Save all projects and outputs and close the application.

Tank You for using the HEC-RAS-Rain-on-Grid-Automation Program!
