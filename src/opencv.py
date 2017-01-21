import _opencv
from numpy import array, zeros, shape, ndarray

__all__ = []

def unarize( func, *args ):
    #print args[1:len(args)]
    result = array( args[0] )
    print shape( result )
    new_args = ( args[0], result, args[1:len(args)] )
    func( *args )
    return result

CvUnaryFunctions = ['cvSobel', 
'cvLaplace', 
'cvCanny', 
'cvPreCornerDetect', 
'cvCornerEigenValsAndVecs',
'cvCornerMinEigenVal',
'cvCornerHarris',
'cvGoodFeaturesToTrack',
'cvGetRectSubPix',
'cvGetQuadrangleSubPix',
'cvResize',
'cvEqualizeHist' ]

for f in CvUnaryFunctions:
    exec("%s=lambda *args, **kw: unarize(_opencv.%s, *args, **kw)" %  (f.lstrip('cv').lower(), f))

class CvImageViewer:
    """
    Wrapper class for some matlab/octave/scilab syntax image viewing functions
    """
    currentWindowName = ""
    currentWindow = -1
    maxWindow = -1

    def __init__(self):
        _opencv.cvStartWindowThread()

    def imagesc(self,im, clims=None):
        """
        Display a normalized version of the image
        """
        if(self.currentWindow==-1):
            self.display()

        # don't normalize multichannel image
        #if(im.nChannels>1):
        #    if(im.depth!=cv.IPL_DEPTH_8U):
        #        im2 = cvCreateImage( cvSize(im.width, im.height), cv.IPL_DEPTH_8U, im.nChannels)
        #        cvScale(im, im2)
        #        im = im2
        #    cvShowImage(self.currentWindowName, im)
        #    return self.currentWindow
        
        # normalize image
        if clims:
            [minv, maxv] = clims
        else:
            #[minv,maxv] = _opencv.cvMinMaxLoc(im)
            minv = ndarray.min(im)
            maxv = ndarray.max(im)
        if maxv != minv:
            s = 255.0/(maxv-minv)
            shift =  255*(-minv)/(maxv-minv)
        else:
            s = 1.0
            shift = -maxv

        im2 = ndarray( shape(im), 'uint8' )
        _opencv.cvConvertScale(im, im2, s, shift)
        _opencv.cvShowImage(self.currentWindowName, im2)

    def image(self, im):
        """
        Display image as is -- probably not what you'd expect for FP or integer images
        """
        if(self.currentWindow==-1):
            self.display()

        _opencv.cvShowImage(self.currentWindowName,im)
        return self.currentWindow
        
    
    def display(self, index=-1):
        """
        open a new window
        """
        if(index==-1):
            self.maxWindow = self.maxWindow+1;
            index= self.maxWindow;

        if(index > self.maxWindow):
            self.maxWindow = index;

        self.currentWindow = index;
        self.currentWindowName = "opencv-python window %d" % self.currentWindow
        _opencv.cvNamedWindow(self.currentWindowName,0)
        return self.currentWindow

    def close(self, index=-1):
        """
        close window(s)
        """
        pass
        
def drawnow():
    _opencv.cvWaitKey(10)

def pause(delay=-1):
    if delay<0:
        _opencv.cvWaitKey(-1)
    else:
        _opencv.cvWaitKey(delay*1000)

c = CvImageViewer()
imagesc = c.imagesc
display = c.display
figure = c.display
image = c.image
imshow = c.image
close = c.close

def imread(fname):
    return _opencv.cvLoadImage(fname, -1)   

loadimage = imread
imload = imread

def imsave(im, fname, format):
    return _opencv.cvSaveImage(fname, im)

saveimage = imsave
imwrite = imsave

def gradient(F):
    F = im2float(F)
    Fx = array(size(F))
    Fy = array(size(F))
    
    # new images
    _opencv.cvSobel(F, Fx, 1, 0, CV_SCHARR)
    _opencv.cvSobel(F, Fy, 0, 1, CV_SCHARR)
    return (Fx, Fy)

histeq=equalizehist
def imhist(im):
    pass
"""
Analysis and Statistics
corr2   [octave-forge/main/image/corr2.m]
returns the correlation coefficient between I and J. 
fftconv2   [octave-forge/main/image/fftconv2.m]
Convolve 2 dimensional signals using the FFT. 
graycomatrix   [octave-forge/main/image/graycomatrix.cc]
Calculate the gray-level co-occurrence matrix P = f(i,j,d,theta) of a gray-level image. 
houghtf   [octave-forge/main/image/houghtf.cc]
Calculate the straight line Hough transform of an image. 
imhist   [octave-forge/main/image/imhist.m]
Shows the histogram of an image using hist See also: hist. 
mean2   [octave-forge/main/image/mean2.m]
returns the mean value for a 2d real type matrix. 
qtdecomp   [octave-forge/main/image/qtdecomp.m]
Performs quadtree decomposition 
qtgetblk   [octave-forge/main/image/qtgetblk.m]
Obtain block values from a quadtree decomposition 
qtsetblk   [octave-forge/main/image/qtsetblk.m]
Set block values in a quadtree decomposition 
std2   [octave-forge/main/image/std2.m]
returns the standard deviation for a 2d real type matrix. 
Black and white image functions
bwarea   [octave-forge/main/image/bwarea.m]
Estimates the area of the "on" pixels of BW. 
bwborder   [octave-forge/main/image/bwborder.m]
b is the borders in the 0-1 matrix im. 
bweuler   [octave-forge/main/image/bweuler.m]
Calculates the Euler number of a binary image 
bwfill   [octave-forge/main/image/bwfill.cc]
performs a flood-fill on BW1 
bwlabel   [octave-forge/main/image/bwlabel.cc]
label foreground components of boolean image 
bwmorph   [octave-forge/main/image/bwmorph.m]
Perform a morphological operation on a binary image 
bwperim 
not implemented 
bwselect   [octave-forge/main/image/bwselect.m]
select connected regions in a binary image 
conndef   [octave-forge/main/image/conndef.m]
Creates a connectivity array 
dilate   [octave-forge/main/image/dilate.m]
Perform a dilation morphological operation on a binary image. 
edge   [octave-forge/main/image/edge.m]
find image edges 
erode   [octave-forge/main/image/erode.m]
Perform an erosion morphological operation on a binary image. 
Colour controls
cmpermute   [octave-forge/main/image/cmpermute.m]
Reorders colors in a colormap 
cmunique   [octave-forge/main/image/cmunique.m]
Finds colormap with unique colors and corresponding image 
hsv2rgb   [octave/scripts/image/hsv2rgb.m]
Transform a colormap from the hsv space to the rgb space. 
imapprox 
not implemented 
ntsc2rgb   [octave/scripts/image/ntsc2rgb.m]
Image format conversion. 
rgb2hsv   [octave/scripts/image/rgb2hsv.m]
Transform a colormap from the rgb space to the hsv space. 
rgb2ntsc   [octave/scripts/image/rgb2ntsc.m]
Image format conversion. 
rgb2ycbcr 
not implemented 
ycbcr2rgb 
not implemented 
Colour maps
autumn   [octave-forge/main/image/autumn.m]
Create color colormap. 
bone   [octave-forge/main/image/bone.m]
Create color colormap. 
colorcube 
not implemented 
colorgradient   [octave-forge/main/image/colorgradient.m]
Define a colour map which smoothly traverses the given colors. 
contrast 
not implemented 
cool   [octave-forge/main/image/cool.m]
Create color colormap. 
copper   [octave-forge/main/image/copper.m]
Create color colormap. 
flag   [octave-forge/main/image/flag.m]
Create color colormap. 
gray   [octave/scripts/image/gray.m]
Return a gray colormap with N entries corresponding to values from 0 to N-1. 
hot   [octave-forge/main/image/hot.m]
Create color colormap. 
hsv   [octave-forge/main/image/hsv.m]
Create color colormap. 
jet   [octave-forge/main/image/jet.m]
Create color colormap. 
lines 
not implemented 
ocean   [octave/scripts/image/ocean.m]
Create color colormap. 
pink   [octave-forge/main/image/pink.m]
Create color colormap. 
prism   [octave-forge/main/image/prism.m]
Create color colormap. 
rainbow   [octave-forge/extra/tk_octave/rainbow.m]
Create color colormap. 
spring   [octave-forge/main/image/spring.m]
Create color colormap. 
summer   [octave-forge/main/image/summer.m]
Create color colormap. 
vga 
not implemented 
white   [octave-forge/main/image/white.m]
Create color colormap. 
winter   [octave-forge/main/image/winter.m]
Create color colormap. 
Display
image   [octave/scripts/image/image.m]
Display a matrix as a color image. 
imagesc   [octave/scripts/image/imagesc.m]
Display a scaled version of the matrix A as a color image. 
imshow   [octave/scripts/image/imshow.m]
Display an image. 
Filtering
applylut   [octave-forge/main/image/applylut.m]
Uses lookup tables to perform a neighbour operation on binary images. 
colfilt   [octave-forge/main/image/colfilt.m]
Apply filter to matrix blocks 
cordflt2   [octave-forge/main/image/cordflt2.cc]
Implementation of two-dimensional ordered filtering. 
histeq   [octave-forge/main/image/histeq.m]
histogram equalization 
imadjust   [octave-forge/main/image/imadjust.m]
Adjust image or colormap values to a specified range 
imnoise   [octave-forge/main/image/imnoise.m]
Adds noise to image in A. 
makelut   [octave-forge/main/image/makelut.m]
Create a lookup table which can be used by applylut. 
medfilt2   [octave-forge/main/image/medfilt2.m]
Two dimensional median filtering. 
ordfilt2   [octave-forge/main/image/ordfilt2.m]
Two dimensional ordered filtering. 
stretchlim   [octave-forge/main/image/stretchlim.m]
Finds limits to contrast stretch an image 
uintlut   [octave-forge/main/image/uintlut.m]
Computes matrix B by using A as an index to lookup table LUT. 
Read/write
bmpwrite   [octave-forge/main/image/bmpwrite.m]
Write the bitmap X into file (8-bit uncompressed format). 
imfinfo 
not implemented 
imginfo   [octave-forge/main/image/imginfo.m]
Get image size from file 
imread   [octave-forge/main/image/imread.m]
Read images from various file formats. 
imwrite   [octave-forge/main/image/imwrite.m]
write image from octave to various file formats 
jpgread   [octave-forge/main/image/jpgread.cc]
Read a JPEG file from disk. 
jpgwrite   [octave-forge/main/image/jpgwrite.cc]
Write a JPEG file to disk. 
loadimage   [octave/scripts/image/loadimage.m]
Load an image file and it's associated color map from the specified FILE. 
pngread   [octave-forge/main/image/pngread.cc]
Read a PNG file from disk. 
pngwrite   [octave-forge/main/image/pngwrite.cc]
pngwrite writes a png file to the disk. 
saveimage   [octave/scripts/image/saveimage.m]
Save the matrix X to FILE in image format FMT. 
Region-based and block processing
bestblk   [octave-forge/main/image/bestblk.m]
Calculates the best size of block for block processing. 
blkproc   [octave-forge/main/image/blkproc.m]
Processes image in blocks using user-supplied function 
col2im   [octave-forge/main/image/col2im.m]
Rearranges matrix columns into blocks 
im2col   [octave-forge/main/image/im2col.m]
Rearranges image blocks into columns 
nlfilter   [octave-forge/main/image/nlfilter.m]
Processes image in sliding blocks using user-supplied function 
poly2mask   [octave-forge/main/image/poly2mask.m]
Convert a polygon to a region mask 
roicolor   [octave-forge/main/image/roicolor.m]
Select a Region Of Interest of an image based on color. 
roifill 
not implemented 
roifilt2 
not implemented 
roipoly 
not implemented 
Representation
dither 
not implemented 
gray2ind   [octave/scripts/image/gray2ind.m]
Convert a gray scale intensity image to an Octave indexed image. 
grayslice   [octave-forge/main/image/grayslice.m]
creates an indexed image X from an intensitiy image I using multiple threshold levels. 
im2bw   [octave-forge/main/image/im2bw.m]
converts image data types to a black-white (binary) image. 
ind2gray   [octave/scripts/image/ind2gray.m]
Convert an Octave indexed image to a gray scale intensity image. 
ind2rgb   [octave/scripts/image/ind2rgb.m]
Convert an indexed image to red, green, and blue color components. 
isbw   [octave-forge/main/image/isbw.m]
returns true for a black-white (binary) image. 
isgray   [octave-forge/main/image/isgray.m]
returns true for an intensity image. 
isind   [octave-forge/main/image/isind.m]
returns true for an index image. 
isrgb   [octave-forge/main/image/isrgb.m]
Returns true if parameter is a RGB image 
mat2gray   [octave-forge/main/image/mat2gray.m]
converts a matrix to a intensity image 
rgb2gray   [octave-forge/main/image/rgb2gray.m]
converts a color map to a gray map. 
rgb2ind   [octave/scripts/image/rgb2ind.m]
Convert and RGB image to an Octave indexed image. 
Reshape
imcrop 
not implemented 
impad   [octave-forge/main/image/impad.m]
Pad (augment) a matrix for application of image processing algorithms. 
imresize   [octave-forge/main/image/imresize.m]
Scales the image A by a factor M using nearest neighbour interpolation. 
imrotate   [octave-forge/main/image/imrotate.m]
imrotate(IMGPRE, THETA, METHOD, BBOX) Rotation of a 2D matrix about its center. 
imshear   [octave-forge/main/image/imshear.m]
imshear (M, AXIS, ALPHA, BBOX) Applies a shear to M. 
imtranslate   [octave-forge/main/image/imtranslate.m]
imtranslate (M, X, Y [, BBOX]) Translate a 2D image by (x,y) using Fourier interpolation. 
MakeShears   [octave-forge/main/image/MakeShears.m]
no description 
padarray   [octave-forge/main/image/padarray.m]
Pads an array in a configurable way. 
rotate_scale   [octave-forge/main/image/rotate_scale.cc]
arbitrary rotation and scaling of an image
"""
