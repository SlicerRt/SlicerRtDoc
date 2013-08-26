Python script examples:

________________________________
PatientHierarchyDataManipulation
  Simple module that creates basic Patient Hierarchy objects
  Usage:
    1. Copy files into a build tree that is included in Slicer (lib/Slicer-4.2/qt-scripted-modules)
    2. Add PatientHierarchyDataManipulation directory path to additional module directories in Slicer Application settings
    3. Configure and build module as a scripted module
- CreatePatientHierarchyTree.py
  - Contains: Scripted module related classes and UI setup
- CreatePatientHierarchyTreeLogicFunctions.py
  - Contains: Functions that create a valid Patient Hierarchy study containing
    - an anatomical volume (selected from scene),
    - a structure set containing
      - a color table,
      - a contour having a closed surface representation (green sphere),
      - and a contour having an indexed labelmap representation (red cube)
  - Demonstrates:
    - Creating valid Patient Hierarchy objects and relations

____________________________
TranslationOfCentersOfMasses
  Simple script that traverses a volume to extract information (center of mass) out of it
  Usage: see getTranslationOfCentersOfMasses_Load.py
- getTranslationOfCentersOfMasses.py
  - Contains: The actual algorithm for computing the center of mass for a labelmap volume and get the translation vector of two centers of masses of two labelmaps
  - Demonstrates:
    - Access voxel data in a volume MRML node
    - Simple algorithm that can be used for not performance-critical applications
- getTranslationOfCentersOfMasses_Load.py
  - Contains: Code that needs to be run from the Slicer Python Interactor window in order to run the algorithm
  - Demonstrates:
    - Access MRML node objects in the MRML tree
    - Invoke function from an external python file
    - Reload an external python file after changed (without restarting Slicer)
