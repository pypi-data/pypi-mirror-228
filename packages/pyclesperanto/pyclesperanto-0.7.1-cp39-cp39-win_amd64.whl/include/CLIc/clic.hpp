#ifndef __CLIC_HPP
#define __CLIC_HPP

#define USE_OPENCL true
#define USE_CUDA false


#if USE_OPENCL
#  ifndef CL_TARGET_OPENCL_VERSION
#    define CL_TARGET_OPENCL_VERSION 120
#  endif
#  ifdef __APPLE__
#    include <OpenCL/opencl.h>
#  else
#    include <CL/cl.h>
#  endif
#endif

#if USE_CUDA
#  include <cuda.h>
#  include <cuda_runtime.h>
#  include <cuda_runtime_api.h>
#  include <nvrtc.h>
#endif

#endif // __CLIC_HPP
