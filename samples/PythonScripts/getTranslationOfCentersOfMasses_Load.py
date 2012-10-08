# Copy here (or to any directory included in PYTHONPATH):
#   c:\devel\Slicer_Trunk_R64-bin\Slicer-build\lib\Slicer-4.1\qt-loadable-modules\Python

v1 = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')

import getTranslationOfCentersOfMasses

#getTranslationOfCentersOfMasses.getCenterOfMass(v1)
getTranslationOfCentersOfMasses.getTranslationOfCentersOfMasses(v1, v2)

#getTranslationOfCentersOfMasses = reload(getTranslationOfCentersOfMasses)
