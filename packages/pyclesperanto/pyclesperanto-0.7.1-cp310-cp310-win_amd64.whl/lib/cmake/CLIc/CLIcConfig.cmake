
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was Config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../../../../../../Program Files/pyclesperanto" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

if(NOT TARGET ${PROJECT_NAME}::${PROJECT_NAME})
    include("${CMAKE_CURRENT_LIST_DIR}/CLIcTargets.cmake")
endif()

set(_LIBRARIES CLIc::CLIc)

# find GPU Framework (OpenCL, CUDA)
find_package(OpenCL)
find_package(CUDA)
find_package(CUDAToolkit)
if (NOT OpenCL_FOUND AND NOT CUDAToolkit_FOUND AND NOT CUDA_FOUND)
    message(FATAL_ERROR "No GPU framework found (OpenCL, CUDA). Please install one of them in order to compile the librairy.")
endif()

check_required_components("CLIc")
