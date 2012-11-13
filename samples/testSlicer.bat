rem This script help in testing SlicerRT in course of development. Loads a scene and switches to a module, so saves a couple of clicks and attention

copy /Y c:\devel\_Scripts\SlicerIni\Debug\Slicer.ini c:\Users\pinter\AppData\Roaming\NA-MIC
c:\devel\Slicer_Trunk_D64-bin\Slicer-build\Slicer.exe --python-code "slicer.util.loadScene('c:/Slicer_Scenes/20121109_156_ProstateLoaded/2012-11-09-Scene.mrml'); slicer.util.selectModule('Contours')"