#include "cv_typemaps.h"
#include <cxmisc.h>

CvMat * CvMatFromPyArray( PyObject * obj, CvMat * header ){
	int typenum=-1;

	PyArrayObject * pyarray=(PyArrayObject *) obj;
	//printf("Type=%d\n", pyarray->descr->type_num);


	//if(!PyArray_Check(obj)){
	//	return NULL;
	//}
	pyarray = (PyArrayObject *) obj;

	// Check PyArray_ISCARRAY
    // now intialize CvMat struct from PyNum array
	int sign=PyArray_ISSIGNED(obj);
	int itemsize=PyArray_ITEMSIZE(obj);

	if(PyArray_ISINTEGER(obj)){
		switch(itemsize){
			case 4 :
				typenum = CV_32S;
				break;
			case 2:
				typenum = sign ? CV_16S : CV_16U;
				break;
			case 1:
				typenum = sign ? CV_8S : CV_8U;
				break;
		}
	}
	else if(PyArray_ISFLOAT(obj)){
			if(itemsize==4){
            	typenum=CV_32F;
			}
			else if(itemsize==8){
				typenum=CV_64F;
			}
	}
	if(typenum==-1){
			printf("Unconvertible type %d\n", pyarray->descr->type_num);
			return NULL;
    }
    // account for multichannel image
    if(pyarray->nd == 3 && pyarray->dimensions[2]<CV_CN_MAX ){
        typenum = CV_MAKETYPE(typenum, pyarray->dimensions[2]);
    }
    else if(pyarray->nd > 2){
		printf("Too many dimensions: %d\n", pyarray->dimensions[2]);
		return NULL;
    }

    cvInitMatHeader(header, pyarray->dimensions[0], (pyarray->nd > 1 ? pyarray->dimensions[1] : 1), 
            typenum, pyarray->data);
    return header;
}

IplImage * IplImageFromPyArray( PyObject * pyarray, IplImage * header ){
	CvMat matheader;
	if(CvMatFromPyArray( pyarray, &matheader )){
		return cvGetImage(&matheader, header);
	}
	return NULL;
}

PyObject * PyArrayFromCvMat( CvMat * mat, bool own){
    int nd;
    int dims[3];
    int typenum;
    PyArrayObject * arr = NULL;

	if(!mat || !mat->data.ptr) return NULL;

    nd = 2;
    switch(CV_MAT_DEPTH(mat->type)){
    case CV_8U:
    case CV_8S:
        typenum=PyArray_UBYTE;
        break;
    case CV_16S:
        typenum=PyArray_SHORT;
        break;
    case CV_32S:
        typenum=PyArray_INT;
        break;
    case CV_32F:
        typenum=PyArray_FLOAT;
        break;
    case CV_64F:
        typenum=PyArray_DOUBLE;
        break;
    default:
        typenum=0;
		return NULL;
    }

	dims[0] = mat->rows;
	dims[1] = mat->cols;
	if(CV_MAT_CN(mat->type) > 1){
		nd = 3;
		dims[2] = CV_MAT_CN(mat->type);
	}
	
	arr = (PyArrayObject *) PyArray_FromDimsAndData(nd, dims, typenum, (char *) mat->data.ptr);
	if(own){ // give ownership of memory to python
		arr->flags |= NPY_OWNDATA; 
		cvIncRefData( mat );  // force CvMat to not free memory 
        cvReleaseMat( &mat );
    }

	return (PyObject *) arr;
}

PyObject * PyArrayFromCvArr( CvArr * arr, bool own ){
	PyArrayObject * pyarr=NULL;
	IplImage * im = (IplImage *) arr;
	CvMat * mat = (CvMat *) arr;

	if(CV_IS_MAT(mat)){
		return PyArrayFromCvMat( mat, own );
	}
	else if(CV_IS_IMAGE(im)){
		CvMat header;
		cvGetMat( arr, &header );
		pyarr = (PyArrayObject *) PyArrayFromCvMat( &header, false );
		if(pyarr && own){
			pyarr->flags |= NPY_OWNDATA; 
			cvReleaseImageHeader( &im );
		}
	}
	else if(arr==NULL){
		return Py_None;
	}
	return (PyObject *)pyarr;
}

// by default, cvAlloc and cvFree align pointers, so trying to 
// free() a section of memory allocated by cvAlloc leads to errors.
//
// PyArray doesn't do any alignment, so in order to allow PyArray to 
// free data allocated by OpenCV, need to set the memory allocation 
// functions to the standard malloc/free
//
// not doing this results in glibc error messages like:
// *** glibc detected *** double free or corruption (out): 0x00000000005ed4a0 ***
//
// CORRECTION: doing this seems to cause these errors ???
//
void * cvMallocWrap( size_t size, void * /* userdata */ ){
	return malloc( size );
}

int cvFreeWrap( void * ptr, void * /* userdata */ ){
	if( ptr == 0 ) return CV_BADARG_ERR;
	free( ptr );
	return CV_OK;
}
