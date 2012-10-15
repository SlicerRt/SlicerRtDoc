set(CTEST_DASHBOARD_ROOT "$ENV{HOME}/Devel")
set(CTEST_SOURCE_DIRECTORY "${CTEST_DASHBOARD_ROOT}/SlicerRT")
set(CTEST_BINARY_DIRECTORY "${CTEST_DASHBOARD_ROOT}/SlicerRT_R64_Continuous-bin")
set(CTEST_SVN_COMMAND "/usr/bin/svn")

set(CTEST_SITE "perklab-virtualbox")
set(CTEST_CMAKE_GENERATOR "Unix Makefiles")
set(CTEST_BUILD_CONFIGURATION "Release") # Release or Debug 

set(MY_COMPILER "g++4.6")
set(MY_QT_VERSION "4.7.4") 
set(MY_BITNESS "64")

set(Slicer_DIR "${CTEST_DASHBOARD_ROOT}/Slicer4_R64-bin/Slicer-build")

# Empty binary directory
ctest_empty_binary_directory(${CTEST_BINARY_DIRECTORY})

# Checkout source if needed and update
if(NOT EXISTS "${CTEST_SOURCE_DIRECTORY}")
  set(CTEST_CHECKOUT_COMMAND "${CTEST_SVN_COMMAND} co https://subversion.assembla.com/svn/slicerrt/trunk/SlicerRt/src ${CTEST_SOURCE_DIRECTORY}")
endif()

set(CTEST_UPDATE_COMMAND ${CTEST_SVN_COMMAND})


# Set CMakeCache content
set(ADDITIONAL_CMAKECACHE_OPTION "
  ADDITIONAL_C_FLAGS:STRING=
  ADDITIONAL_CXX_FLAGS:STRING=
  CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/g++-4.6
")
file(WRITE "${CTEST_BINARY_DIRECTORY}/CMakeCache.txt" "
  Slicer_DIR:PATH=${Slicer_DIR}
  ${ADDITIONAL_CMAKECACHE_OPTION}
")


# Get Slicer SVN revision
set(_revision_regex "^#define[ \t]+Slicer_WC_REVISION[ \t]+[\"]*([0-9A-Za-z\\.]+)[\"][ \t]*$")
file(STRINGS "${Slicer_DIR}/vtkSlicerVersionConfigure.h" _revision_string
      LIMIT_COUNT 1 REGEX ${_revision_regex})
set(dollar "$")
string(REGEX REPLACE ${_revision_regex} "\\1" Slicer_WC_REVISION "${_revision_string}")


# Get SlicerRT SVN revision
include(FindSubversion)
Subversion_WC_INFO(${CTEST_SOURCE_DIRECTORY} SlicerRT)
set(CTEST_BUILD_NAME "${Slicer_WC_REVISION}-SlicerRT-svn${SlicerRT_WC_REVISION}-${MY_COMPILER}-${MY_BITNESS}bits-Qt${MY_QT_VERSION}-${CTEST_BUILD_CONFIGURATION}")

# Set SlicerRT inner directory as test directory
set(SLICERRT_TEST_DIRECTORY "${CTEST_DASHBOARD_ROOT}/SlicerRT_R64_Continuous-bin/inner-build")

# Perform update, build, and test
ctest_start("Continuous" TRACK Extensions-Continuous)
ctest_update(RETURN_VALUE count)

#set(count 1) #TODO: Remove
if(count GREATER 0)
  ctest_configure(BUILD "${CTEST_BINARY_DIRECTORY}")
  ctest_build(BUILD "${CTEST_BINARY_DIRECTORY}")
  ctest_test(BUILD "${SLICERRT_TEST_DIRECTORY}")
  ctest_submit()
endif()
