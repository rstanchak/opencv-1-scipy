#!/usr/bin/python
import opencv
from numpy import *

print "OpenCV Scipy test"
#im = opencv.loadimage('/home/roman/pics/goofy.jpg')
#opencv.figure()
im = array([[0,0,0],[128,128,128],[255,255,255]])
print im
print shape(im)
opencv.imagesc(im)
opencv.pause()

