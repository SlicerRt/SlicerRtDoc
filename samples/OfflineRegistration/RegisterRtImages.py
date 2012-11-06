from __main__ import slicer

#########################################################################
# RegisterRtImages

class RegisterRtImages:
  def __init__(self, parent):
    pass

#########################################################################
# RegisterRtImagesLogic

class RegisterRtImagesLogic:
  
  def __init__(self):  
    # Set default registration parameters
    self.registrationParameters = {}
    self.registrationParameters["useRigid"] = True      
    self.registrationParameters["translationScale"] = 100000.0
    self.registrationParameters["minimumStepLength"] = 0.05
    self.registrationParameters["maximumStepLength"] = 10.0   
    self.registrationParameters["relaxationFactor"] = 0.9
    self.registrationParameters["numberOfSamples"] = 10000
    self.registrationParameters["initializeTransformMode"] = "useMomentsAlign"          

  def computeMriToMriTranslation(self, fixedImageFilename, movingImageFilename, resultTxtFilename):                
    self.registrationParameters["numberOfSamples"] = 10000
    self.computeTranslation(fixedImageFilename, movingImageFilename, resultTxtFilename)      

  def computeCtToCbctTranslation(self, fixedImageFilename, movingImageFilename, resultTxtFilename):                
    self.registrationParameters["numberOfSamples"] = 100000
    self.computeTranslation(fixedImageFilename, movingImageFilename, resultTxtFilename)      

  def computeMriToCtTranslation(self, fixedImageFilename, movingImageFilename, resultTxtFilename):                
    self.registrationParameters["numberOfSamples"] = 100000
    self.computeTranslation(fixedImageFilename, movingImageFilename, resultTxtFilename)      
            
  def computeTranslation(self, fixedImageFilename, movingImageFilename, resultTxtFilename):
    try:                                
      # Read input volumes
      fixedImageLoadingResult=slicer.util.loadVolume(fixedImageFilename, returnNode=True)
      fixedImageNode=fixedImageLoadingResult[1]      
      self.registrationParameters["fixedVolume"] = fixedImageNode.GetID()
      movingImageLoadingResult=slicer.util.loadVolume(movingImageFilename, returnNode=True)
      movingImageNode=movingImageLoadingResult[1]     
      self.registrationParameters["movingVolume"] = movingImageNode.GetID()
      # Create output transform node
      outputTransform = slicer.vtkMRMLLinearTransformNode()
      outputTransform.SetName("PlanningToGuidanceTransform")
      slicer.mrmlScene.AddNode( outputTransform )
      self.registrationParameters["linearTransform"] = outputTransform.GetID()
      # Run registration
      brainsFit = slicer.modules.brainsfit
      self.cliBrainsFitRigidNode = None
      self.cliBrainsFitRigidNode = slicer.cli.run(brainsFit, None, self.registrationParameters, wait_for_completion = True)
      # Retrieve resulting transformation matrix
      outputTransformMatrix=outputTransform.GetMatrixTransformToParent()   
      # Write results to file
      fp = open(resultTxtFilename, "w")
      fp.write('Translation: '+str(outputTransformMatrix.GetElement(0,3))+' '+str(outputTransformMatrix.GetElement(1,3))+' '+str(outputTransformMatrix.GetElement(2,3)))
      fp.close() 
      # Apply transform
      movingImageNode.SetAndObserveTransformNodeID(outputTransform.GetID())
    except Exception, e:
      fp = open(resultTxtFilename, "w")
      fp.write('Registration failed!\n' + str(e))
      fp.close()           
