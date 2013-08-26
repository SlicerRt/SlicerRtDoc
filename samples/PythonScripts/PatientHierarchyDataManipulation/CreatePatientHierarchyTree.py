import os
import unittest

from __main__ import vtk, qt, ctk, slicer

#
# CreatePatientHierarchyTree
#

class CreatePatientHierarchyTree:
  def __init__(self, parent):
    parent.title = "CreatePatientHierarchyTree" # TODO make this more human readable by adding spaces
    parent.categories = ["Examples"]
    parent.dependencies = ["PatientHierarchy"]
    parent.contributors = ["Mattea Welch (Queen's)"]
    parent.helpText = """This is a module used to create a patient hierarchy."""
    parent.acknowledgementText = """This file was originally developed by Mattea Welch, Perklab, Queen's University and was supported through the SWEP program.""" 
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['CreatePatientHierarchyTree'] = self.runTest

  def runTest(self):
    tester = CreatePatientHierarchyTreeTest()
    tester.runTest()

#
# qCreatePatientHierarchyTreeWidget
#

class CreatePatientHierarchyTreeWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    
    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "CreatePatientHierarchyTree Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)
    
    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Patient and study name
    #
    self.patientName = qt.QLineEdit()
    parametersFormLayout.addRow("Patient Name: ", self.patientName)
    
    self.studyName = qt.QLineEdit()
    parametersFormLayout.addRow("Study Name: ", self.studyName)
    
    #
    # Create structure sets
    #
    self.structureSet = qt.QCheckBox()
    parametersFormLayout.addRow("Create Structure Sets: ", self.structureSet)
    
    #
    # input volume selector
    #
    self.volumeSelector = slicer.qMRMLNodeComboBox()
    self.volumeSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.volumeSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.volumeSelector.selectNodeUponCreation = True
    self.volumeSelector.addEnabled = False
    self.volumeSelector.removeEnabled = False
    self.volumeSelector.noneEnabled = False
    self.volumeSelector.showHidden = False
    self.volumeSelector.showChildNodeTypes = False
    self.volumeSelector.setMRMLScene( slicer.mrmlScene )
    self.volumeSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Structure Set Volume: ", self.volumeSelector)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    #self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.volumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    
    # Add vertical spacer
    self.layout.addStretch(1)

  def onSelect(self):
    self.applyButton.enabled = self.volumeSelector.currentNode()

  def onApplyButton(self):
    self.patientID = self.patientName.text
    self.studyID = self.studyName.text
    self.generateStructureSets = self.structureSet.checkState() # 0 is true, 2 is false
    self.volumeNodeID = self.volumeSelector.currentNodeID
    logic = CreatePatientHierarchyTreeLogic()
    print("Run the algorithm")
    logic.run(self.patientID, self.studyID, self.generateStructureSets, self.volumeNodeID)
    
  def onReload(self,moduleName="CreatePatientHierarchyTree"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)
    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()

#
# CreatePatientHierarchyTreeLogic
#

class CreatePatientHierarchyTreeLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def run(self,patientID,studyID,generateStructureSets,volumeNode):
    import createSamplePatientHierarchyTree
    createSamplePatientHierarchyTree = reload(createSamplePatientHierarchyTree)
    createSamplePatientHierarchyTree.createSamplePatientHierarchyTree(patientID, studyID, generateStructureSets, volumeNode)
    return True


