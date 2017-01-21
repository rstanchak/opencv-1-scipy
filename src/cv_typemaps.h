#ifndef CV_TYPEMAPS_H
#define CV_TYPEMAPS_H

#include <cxtypes.h>
#include <cxcore.h> 
#include <Python.h>

// must define this symbol before including arrayobject.h
#define PY_ARRAY_UNIQUE_SYMBOL Py_Array_API_CV
#ifndef SWIG_FILE_WITH_INIT
#define NO_IMPORT_ARRAY
#endif

#include <numpy/arrayobject.h>

CvMat * CvMatFromPyArray( PyObject * pyarray, CvMat * header );

IplImage * IplImageFromPyArray( PyObject * pyarray, IplImage * header );

PyObject * PyArrayFromCvMat( CvMat * mat, bool own );

PyObject * PyArrayFromCvArr( CvArr * arr, bool own );

void * cvMallocWrap( size_t size, void * userdata  );
int cvFreeWrap( void * ptr, void * userdata  );

typedef CvSeq * pCvSeq;
typedef CvSeq ** ppCvSeq;

#endif
