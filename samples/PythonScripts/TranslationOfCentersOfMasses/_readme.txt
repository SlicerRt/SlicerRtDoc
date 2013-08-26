Python script examples:

____________________________
TranslationOfCentersOfMasses
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
