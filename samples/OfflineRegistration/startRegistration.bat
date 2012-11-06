@echo off
set SLICER_BUILD=f:\devel\Slicer4-win64rel\Slicer-build

set SLICER_LAUNCH="%SLICER_BUILD%\Slicer.exe" --testing --no-splash --no-main-window --ignore-slicerrc
set ADDITIONAL_SLICER_OPTIONS=--additional-module-paths "."

set FIXED_IMAGE_FILE=MRgRT-registration-test/5 MRgRT_phantom_Guidance_MR_t1_tse_tra_320_1AVG_position_2.nrrd
set MOVING_IMAGE_FILE=MRgRT-registration-test/7 MRgRT_phantom_Planning_MR_t1_tse_tra_320_2AVG.nrrd
set OUTPUT_FILE=translation-MrGuidanceToMrPlanning.txt
%SLICER_LAUNCH% --python-code "import RegisterRtImages; logic=RegisterRtImagesLogic(); logic.computeMriToMriTranslation('%FIXED_IMAGE_FILE%','%MOVING_IMAGE_FILE%', '%OUTPUT_FILE%');" %ADDITIONAL_SLICER_OPTIONS%

set FIXED_IMAGE_FILE=MRgRT-registration-test/2 CT.nrrd
set MOVING_IMAGE_FILE=MRgRT-registration-test/CBCT-1.nrrd
set OUTPUT_FILE=translation-CtToCbct.txt
%SLICER_LAUNCH% --python-code "import RegisterRtImages; logic=RegisterRtImagesLogic(); logic.computeCtToCbctTranslation('%FIXED_IMAGE_FILE%','%MOVING_IMAGE_FILE%', '%OUTPUT_FILE%');" %ADDITIONAL_SLICER_OPTIONS%

set FIXED_IMAGE_FILE=MRgRT-registration-test/7 MRgRT_phantom_Planning_MR_t1_tse_tra_320_2AVG.nrrd
set MOVING_IMAGE_FILE=MRgRT-registration-test/2 CT.nrrd
set OUTPUT_FILE=translation-MriToCt.txt
%SLICER_LAUNCH% --python-code "import RegisterRtImages; logic=RegisterRtImagesLogic(); logic.computeMriToCtTranslation('%FIXED_IMAGE_FILE%','%MOVING_IMAGE_FILE%', '%OUTPUT_FILE%');" %ADDITIONAL_SLICER_OPTIONS%

set FIXED_IMAGE_FILE=MRgRT-registration-test/7 MRgRT_phantom_Planning_MR_t1_tse_tra_320_2AVG.nrrd
set MOVING_IMAGE_FILE=MRgRT-registration-test/CBCT-1.nrrd
set OUTPUT_FILE=translation-MriToCbct.txt
%SLICER_LAUNCH% --python-code "import RegisterRtImages; logic=RegisterRtImagesLogic(); logic.computeMriToCtTranslation('%FIXED_IMAGE_FILE%','%MOVING_IMAGE_FILE%', '%OUTPUT_FILE%');" %ADDITIONAL_SLICER_OPTIONS%
   
pause
