// python module initialization 
%init %{
	   // change default OpenCV Memory Allocation functions to normal malloc/free
//	   cvSetMemoryManager( cvMallocWrap, cvFreeWrap, NULL );

       // need to call this to use PyNum array functions
	   import_array()
%}
			 
%{
	#define SWIG_FILE_WITH_INIT
	#include "cv_typemaps.h"
%}

%include "cv_defines.i"


%typemap( out ) IplImage * (){
	$result = (PyObject *) PyArrayFromCvArr( $1, true);
	if($result==NULL) SWIG_exception (SWIG_TypeError, "could not convert IplImage to PyArray");
}
%typemap( out ) CvMat * (){
	$result = (PyObject *) PyArrayFromCvArr( $1, true );
	if($result==NULL) SWIG_exception (SWIG_TypeError, "could not convert CvMat to PyArray");
}
%typemap( in ) IplImage * (IplImage temp) {
	$1 = IplImageFromPyArray( $input, &temp );
	if($1==NULL) SWIG_exception (SWIG_TypeError, "could not convert PyArray to IplImage");
}
%typemap( in ) CvMat * (CvMat temp) {
	$1 = CvMatFromPyArray( $input, &temp );
	if($1==NULL) SWIG_exception (SWIG_TypeError, "could not convert PyArray to CvMat");
}
%typemap( in ) CvArr * (CvMat temp) {
	$1 = CvMatFromPyArray( $input, &temp );
	if($1==NULL) SWIG_exception (SWIG_TypeError, "could not convert PyArray to CvArr");
}
