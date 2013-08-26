import os
import glob
from __main__ import vtk
from __main__ import slicer

def getCenterOfMass(volumeNode):
  centerOfMass = [0,0,0]

  #logFile = open('d:/pyLog.txt', 'w')

  if volumeNode.GetLabelMap() == 0:
    print('Warning: input volume is not labelmap: \'' + volumeNode.GetName() + '\'')

  numberOfStructureVoxels = 0
  sumX = sumY = sumZ = 0

  volume = volumeNode.GetImageData()
  print('  Volume extent: (' + repr(volume.GetExtent()[0]) + '-' + repr(volume.GetExtent()[1]) + ', ' + repr(volume.GetExtent()[2]) + '-' + repr(volume.GetExtent()[3]) + ', ' + repr(volume.GetExtent()[4]) + '-' + repr(volume.GetExtent()[5]) + ')')
  for z in xrange(volume.GetExtent()[4], volume.GetExtent()[5]+1):
    #logFile.write(repr(z) + '\n')
    for y in xrange(volume.GetExtent()[2], volume.GetExtent()[3]+1):
      for x in xrange(volume.GetExtent()[0], volume.GetExtent()[1]+1):
        voxelValue = volume.GetScalarComponentAsDouble(x,y,z,0)
        if voxelValue>0:
          numberOfStructureVoxels = numberOfStructureVoxels+1
          sumX = sumX + x
          sumY = sumY + y
          sumZ = sumZ + z

  if numberOfStructureVoxels > 0:
    centerOfMass[0] = sumX / numberOfStructureVoxels
    centerOfMass[1] = sumY / numberOfStructureVoxels
    centerOfMass[2] = sumZ / numberOfStructureVoxels

  #logFile.close()
  print('Center of mass for \'' + volumeNode.GetName() + '\': ' + repr(centerOfMass))
  return centerOfMass

def getTranslationOfCentersOfMasses(volumeNode1, volumeNode2):
  center1 = getCenterOfMass(volumeNode1)
  center2 = getCenterOfMass(volumeNode2)

  translation = []
  for i in [0,1,2]:
    translation.append(center2[i] - center1[i])
  return translation