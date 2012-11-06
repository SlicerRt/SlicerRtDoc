rem set SLICER_LAUNCHER="f:\devel\Slicer4-win64rel\Slicer-build\Slicer.exe" 
set SLICER_LAUNCHER="c:\Program Files\Slicer 4.2.0-2012-11-02\Slicer.exe" 

%SLICER_LAUNCHER% --python-code "import SlicerRtSliceletTest; slicelet=SlicerRtSliceletTestSlicelet();" --no-splash --no-main-window --additional-module-paths "."
