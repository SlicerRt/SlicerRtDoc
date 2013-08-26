# In order to run this directly from Slicer, copy here (or to any directory included in PYTHONPATH):
#   c:\devel\Slicer_Trunk_R64-bin\Slicer-build\lib\Slicer-4.1\qt-loadable-modules\Python

# Get two volumes from the MRML scene (the first two)
v1 = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')
v2 = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode2')

# Import the algorithm script
import getTranslationOfCentersOfMasses

# Call getCenterOfMass on the first volume
#getTranslationOfCentersOfMasses.getCenterOfMass(v1)

# Call getTranslationOfCentersOfMasses on the two volumes (displacement of the two centers)
getTranslationOfCentersOfMasses.getTranslationOfCentersOfMasses(v1, v2)

# Reload algorithm script (in case it has been changed)
#getTranslationOfCentersOfMasses = reload(getTranslationOfCentersOfMasses)
