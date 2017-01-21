%module cv 

// python module initialization 
%init %{
	// need to call this to use PyNum array functions
	import_array();
%}

%{
	#include "Numeric/arrayobject.h"
	#include "cv.h"
	#include "cxcore.h"
	#include "highgui.h"
%}

// typemaps between CvArray, CvMat, IplImage and PyNum
%include "cv_typemaps.i"

#if defined WIN32 || defined WIN64
#define CV_CDECL __cdecl
#define CV_STDCALL __stdcall
#else
#define CV_CDECL
#define CV_STDCALL
#endif

#ifndef CV_EXTERN_C
#ifdef __cplusplus
#define CV_EXTERN_C extern "C"
#define CV_DEFAULT(val) = val
#else
#define CV_EXTERN_C
#define CV_DEFAULT(val)
#endif
#endif

#ifndef CV_EXTERN_C_FUNCPTR
#ifdef __cplusplus
#define CV_EXTERN_C_FUNCPTR(x) extern "C" { typedef x; }
#else
#define CV_EXTERN_C_FUNCPTR(x) typedef x
#endif
#endif

#ifndef CV_INLINE
#if defined __cplusplus
#define CV_INLINE inline
#elif defined WIN32 || defined WIN64 || defined __GNUC__
#define CV_INLINE __inline
#else
#define CV_INLINE static
#endif
#endif /* CV_INLINE */

#if (defined WIN32 || defined WIN64) && defined CVAPI_EXPORTS
#define CV_EXPORTS __declspec(dllexport)
#else
#define CV_EXPORTS
#endif

#ifndef CVAPI
#define CVAPI(rettype) CV_EXTERN_C CV_EXPORTS rettype CV_CDECL
#endif

%include "cv.h"
%include "cxcore.h"
%include "highgui.h"
%include "cxtypes.h"

