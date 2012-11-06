set SLICER_LAUNCHER="c:\Program Files\Slicer 4.2.0-2012-11-05\Slicer.exe" 

rem --testing --no-splash --no-main-window --ignore-slicerrc
%SLICER_LAUNCHER% --python-code "import RegisterRtImages; logic=RegisterRtImagesLogic(); logic.computeMriToMriTranslation('MRgRT-registration-test/5 MRgRT_phantom_Guidance_MR_t1_tse_tra_320_1AVG_position_2.nrrd','MRgRT-registration-test/7 MRgRT_phantom_Planning_MR_t1_tse_tra_320_2AVG.nrrd', 'translation-MrGuidanceToMrPlanning.txt'); logic.computeCtToCbctTranslation('MRgRT-registration-test/2 CT.nrrd','MRgRT-registration-test/CBCT-1.nrrd', 'translation-CtToCbct.txt'); logic.computeMriToCtTranslation('MRgRT-registration-test/7 MRgRT_phantom_Planning_MR_t1_tse_tra_320_2AVG.nrrd','MRgRT-registration-test/2 CT.nrrd', 'translation-MriToCt.txt'); logic.computeMriToCtTranslation('MRgRT-registration-test/7 MRgRT_phantom_Planning_MR_t1_tse_tra_320_2AVG.nrrd','MRgRT-registration-test/CBCT-1.nrrd', 'translation-MriToCbct.txt');" --additional-module-paths "."

pause
