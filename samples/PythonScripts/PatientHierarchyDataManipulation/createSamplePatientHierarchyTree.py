import os
import glob
import math
from __main__ import vtk
from __main__ import slicer

import vtkSlicerContoursModuleMRML

def createSamplePatientHierarchyTree(patientName, studyName, generateStructureSets, volumeNodeID):
  
  #------------------------Generate Higher level parent and study hierarchy nodes---------------#
  patientID = 'PatientID01'
  studyInstanceUid = 'StudyID01'
  
  #------------------------Create CT Series---------------#
  volumeNode = slicer.mrmlScene.GetNodeByID(volumeNodeID)
  volumeSeriesInstanceUid = 'volumeSeriesHierarchyID'
  #Create CT series from volume node
  seriesNode = slicer.vtkMRMLHierarchyNode()
  seriesNode.HideFromEditorsOff()
  seriesNode.SetAssociatedNodeID(volumeNodeID)
  seriesNode.SetAttribute('HierarchyType', 'PatientHierarchy')
  seriesNode.SetAttribute('DicomLevel', 'Series')
  seriesDescription = volumeNode.GetName()
  #seriesDescription = volumeNodeID
  seriesDesciption = seriesDescription + '_Hierarchy'
  seriesNode.SetName(seriesDescription)
  seriesNode.SetAttribute('DicomUid', volumeSeriesInstanceUid)
  slicer.mrmlScene.AddNode(seriesNode)

  #Insert CT series in hierarchy
  slicer.modules.patienthierarchy.logic().InsertDicomSeriesInHierarchy(slicer.mrmlScene, patientID, studyInstanceUid, volumeSeriesInstanceUid)
  
   
  #Get higher level parent and study nodes by their IDs (set above). Assume that attributes
  #exist and therefore don't need to be set. 
  patientNode = slicer.modules.patienthierarchy.logic().GetPatientHierarchyNodeByUID(slicer.mrmlScene, patientID)
  patientNode.SetName(patientName)
  studyNode = slicer.modules.patienthierarchy.logic().GetPatientHierarchyNodeByUID(slicer.mrmlScene, studyInstanceUid)
  studyNode.SetName(studyName)
  
  #------------------------Create Colour Table---------------#
  seriesName = 'StructureSet'
  #Create colorTable node
  structureSetColorTableNode = slicer.vtkMRMLColorTableNode()
  structureSetColorTableNodeName = seriesName + "_ColorTable"
  structureSetColorTableNodeName = slicer.mrmlScene.GenerateUniqueName(structureSetColorTableNodeName)
  structureSetColorTableNode.SetName(structureSetColorTableNodeName)
  structureSetColorTableNode.HideFromEditorsOff()
  structureSetColorTableNode.SetTypeToUser()
  slicer.mrmlScene.AddNode(structureSetColorTableNode)
  structureSetColorTableNode.SetNumberOfColors(4)
  structureSetColorTableNode.GetLookupTable().SetTableRange(0, 3)
  structureSetColorTableNode.AddColor('Background', 0.0, 0.0, 0.0, 0.0) #Black background
  structureSetColorTableNode.AddColor('Invalid', 0.5, 0.5, 0.5, 1.0) #Color for invalid index
  
  #------------------------Create root contour hierarchy for series-----------------#
  
  contourHierarchySeriesNodeName = seriesName + '_AllStructures' + '_PatientHierarchy'
  contourHierarchySeriesNodeName = slicer.mrmlScene.GenerateUniqueName(contourHierarchySeriesNodeName)
  contourHierarchySeriesNode = slicer.vtkMRMLDisplayableHierarchyNode()
  contourHierarchySeriesNode.SetName(contourHierarchySeriesNodeName)
  contourHierarchySeriesNode.SetParentNodeID(studyNode.GetID())
  contourHierarchySeriesNode.AllowMultipleChildrenOn()
  contourHierarchySeriesNode.HideFromEditorsOff()
  contourHierarchySeriesNode.SetAttribute('HierarchyType', 'PatientHierarchy');
  contourHierarchySeriesNode.SetAttribute('DicomLevel', 'Series');
  contourHierarchySeriesNode.SetAttribute('DicomUid', structureSetColorTableNode.GetID())
  contourHierarchySeriesNode.SetAttribute('DicomRtImport.' + "SeriesName", seriesName)
  contourHierarchySeriesNode.SetAttribute('ContourHierarchy','1')
  slicer.mrmlScene.AddNode(contourHierarchySeriesNode)
  
  #Display node needed for hierarchy node
  contourHierarchySeriesDisplayNode = slicer.vtkMRMLModelDisplayNode()
  contourHierarchySeriesDisplayNodeName = contourHierarchySeriesNodeName + 'Display'
  contourHierarchySeriesDisplayNode.SetName(contourHierarchySeriesDisplayNodeName)
  contourHierarchySeriesDisplayNode.SetVisibility(1)
  slicer.mrmlScene.AddNode(contourHierarchySeriesDisplayNode)
  contourHierarchySeriesNode.SetAndObserveDisplayNodeID(contourHierarchySeriesDisplayNode.GetID())
  
  
  if(generateStructureSets == 2):
    createStructures = True
  else:
    createStructures = False
  #------------------------Create contour Node from labelmap---------------#
  roiLabel_Labelmap = 'Sample_Labelmap' + '_PatientHierarchy'
  roiColor_Labelmap = [1.0, 0.0, 0.0]
  
  #Save color in color table
  structureSetColorTableNode.AddColor(roiLabel_Labelmap, roiColor_Labelmap[0], roiColor_Labelmap[1], roiColor_Labelmap[2]) 
    
  contourNodeName_Labelmap = roiLabel_Labelmap + '_Contour'
  contourNodeName_Labelmap = slicer.mrmlScene.GenerateUniqueName(contourNodeName_Labelmap)
  
  contourNode_Labelmap = vtkSlicerContoursModuleMRML.vtkMRMLContourNode()
  slicer.mrmlScene.AddNode(contourNode_Labelmap)
  contourNode_Labelmap.SetName(contourNodeName_Labelmap)
  
  if createStructures == True:
    roiPoly_Labelmap = createSampleLabelmapVolume(volumeNode)
    contourNode_Labelmap.SetAndObserveIndexedLabelmapVolumeNodeId(roiPoly_Labelmap.GetID())
    #TODO: Set reference?
    contourNode_Labelmap.HideFromEditorsOff()
    
  
  #Put contour node in hierarchy
  contourHierarchyNode_Labelmap = slicer.vtkMRMLDisplayableHierarchyNode()
  phContourNodeName_Labelmap = contourNodeName_Labelmap + '_PatientHierarchy'
  phContourNodeName_Labelmap = slicer.mrmlScene.GenerateUniqueName(phContourNodeName_Labelmap)
  contourHierarchyNode_Labelmap.SetName(phContourNodeName_Labelmap)
  contourHierarchyNode_Labelmap.SetParentNodeID(contourHierarchySeriesNode.GetID())
  contourHierarchyNode_Labelmap.SetAssociatedNodeID(contourNode_Labelmap.GetID())
  contourHierarchyNode_Labelmap.HideFromEditorsOff()
  contourHierarchyNode_Labelmap.SetAttribute('HierarchyType', 'PatientHierarchy')
  contourHierarchyNode_Labelmap.SetAttribute('DicomLevel', 'Series')
  slicer.mrmlScene.AddNode(contourHierarchyNode_Labelmap)
  
  #------------------------Create ROI Subseries from Model---------------#
  roiLabel_Model = 'Sample_Model' + '_PatientHierarchy'
  roiColor_Model = [0.0, 1.0, 0.0]
  
  #Save color in color table
  structureSetColorTableNode.AddColor(roiLabel_Model, roiColor_Model[0], roiColor_Model[1], roiColor_Model[2]) 
  
  contourNodeName_Model = roiLabel_Model + '_Contour'
  contourNodeName_Model = slicer.mrmlScene.GenerateUniqueName(contourNodeName_Model)
  
  contourNode_Model = vtkSlicerContoursModuleMRML.vtkMRMLContourNode()
  contourNode_Model = vtkSlicerContoursModuleMRML.vtkMRMLContourNode.SafeDownCast(slicer.mrmlScene.AddNode(contourNode_Model))
  contourNode_Model.SetName(contourNodeName_Model)
  
  if createStructures == True:
    roiPoly_Model = createSampleModelVolume(volumeNode, roiColor_Model)
    contourNode_Model.SetAndObserveIndexedLabelmapVolumeNodeId(roiPoly_Model.GetID())
    contourNode_Model.HideFromEditorsOff()
  
  #put contour node in hierarchy
  contourHierarchyNode_Model = slicer.vtkMRMLDisplayableHierarchyNode()
  phContourNodeName_Model = contourNodeName_Model + '_PatientHierarchy'
  phContourNodeName_Model = slicer.mrmlScene.GenerateUniqueName(phContourNodeName_Model)
  contourHierarchyNode_Model.SetName(phContourNodeName_Model)
  contourHierarchyNode_Model.SetParentNodeID(contourHierarchySeriesNode.GetID())
  contourHierarchyNode_Model.SetAssociatedNodeID(contourNode_Model.GetID())
  contourHierarchyNode_Model.HideFromEditorsOff()
  contourHierarchyNode_Model.SetAttribute('HierarchyType', 'PatientHierarchy')
  contourHierarchyNode_Model.SetAttribute('DicomLevel', 'Series')
  slicer.mrmlScene.AddNode(contourHierarchyNode_Model) 

  #--------------------Add color table to patient hierarchy (456)------------------#  
  patientHierarchyColorTableNode = slicer.vtkMRMLHierarchyNode()
  phColorTableNodeName = structureSetColorTableNodeName + '_PatientHierarchy'
  phColorTableNodeName = slicer.mrmlScene.GenerateUniqueName(phColorTableNodeName)
  patientHierarchyColorTableNode.SetName(phColorTableNodeName)
  patientHierarchyColorTableNode.HideFromEditorsOff()
  patientHierarchyColorTableNode.SetAssociatedNodeID(structureSetColorTableNode.GetID())
  patientHierarchyColorTableNode.SetAttribute('HierarchyType', 'PatientHierarchy')
  patientHierarchyColorTableNode.SetAttribute('DicomLevel', 'Series')
  patientHierarchyColorTableNode.SetParentNodeID(contourHierarchySeriesNode.GetID())
  slicer.mrmlScene.AddNode(patientHierarchyColorTableNode)
  
  slicer.modules.patienthierarchy.logic().InsertDicomSeriesInHierarchy(slicer.mrmlScene, patientID, studyInstanceUid, contourHierarchySeriesNode.GetID())

  return 0
  
def createSampleLabelmapVolume(volumeNode):
  scalarVolumeNode_In = slicer.vtkMRMLScalarVolumeNode()
  scalarVolumeNode_In = slicer.mrmlScene.CopyNode(volumeNode)
  imageData = scalarVolumeNode_In.GetImageData()
  extent = imageData.GetExtent()
  minX = extent[0]
  maxX = extent[1]
  minY = extent[2]
  maxY = extent[3]
  minZ = extent[4]
  maxZ = extent[5]
  print(maxX)
  print((maxX/4))
  print((maxX/4)*3)
  
  for x in xrange(minX, maxX):
    for y in xrange(minY, maxY):
      for z in xrange(minZ, maxZ):
        if (x >= (maxX/4) and x <= (maxX/4) * 3) and (y >= (maxY/4) and y <= (maxY/4) * 3) and (z >= (maxZ/4) and z <= (maxZ/4) * 3):
          imageData.SetScalarComponentFromDouble(x,y,z,0,0)
        else:
          imageData.SetScalarComponentFromDouble(x,y,z,0,255)
 
  #Display labelmap
  scalarVolumeDisplayNode = slicer.vtkMRMLScalarVolumeDisplayNode()
  scalarVolumeDisplayNode = slicer.mrmlScene.AddNode(scalarVolumeDisplayNode)
  scalarVolumeDisplayNode.VisibilityOn()
  scalarVolumeNode_Out = slicer.vtkMRMLScalarVolumeNode()
  scalarVolumeNode_Out = slicer.mrmlScene.AddNode(scalarVolumeNode_Out)
  scalarVolumeNode_Out.SetName('regionFillingOfLabelMapTest')
  scalarVolumeNode_Out.SetAndObserveDisplayNodeID(scalarVolumeDisplayNode.GetID())
  scalarVolumeNode_Out.SetHideFromEditors(0)
  
  return scalarVolumeNode_Out
  

def createSampleModelVolume(volumeNode, roiColor_Model):
#----------------------------Create sphere at the centre of the volume------------------------------------#
  modelNode = slicer.vtkMRMLModelNode()
  modelNode = slicer.mrmlScene.CopyNode(volumeNode)
  minX = maxX = minY = maxY = minZ = maxZ = 0.0
  min_max_values = [minX, maxX, minY, maxY, minZ, maxZ]
  modelNode.GetRASBounds(min_max_values)
  x = (min_max_values[0] + min_max_values[1])/2
  y = (min_max_values[2] + min_max_values[3])/2
  z = (min_max_values[4] + min_max_values[5])/2
  
  #---------------------------Taken from: http://www.na-mic.org/Bug/view.php?id=1536-------------------#
  sphere = vtk.vtkSphereSource()
  sphere.SetCenter(x, y, z)
  sphere.SetRadius(20)
  sphere.GetOutput().Update()
  displayNode = slicer.vtkMRMLModelDisplayNode()
  displayNode = slicer.vtkMRMLModelDisplayNode.SafeDownCast(slicer.mrmlScene.AddNode(displayNode))
  displayNode.SliceIntersectionVisibilityOn()
  displayNode.VisibilityOn()
  displayNode.SetColor(roiColor_Model[0], roiColor_Model[1], roiColor_Model[2])
  modelNode = slicer.vtkMRMLModelNode()
  modelNode = slicer.mrmlScene.AddNode(modelNode)
  modelNode.SetName('modelIntersectionTest')
  modelNode.SetAndObservePolyData(sphere.GetOutput())
  modelNode.SetAndObserveDisplayNodeID(displayNode.GetID())
  modelNode.SetHideFromEditors(0)
  modelNode.SetSelectable(1)
  
  return modelNode