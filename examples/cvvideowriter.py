#!/usr/bin/python
from opencv.highgui import cvCreateVideoWriter, CV_FOURCC

vw = cvCreateVideoWriter(cvSize(640,480), 30, CV_FOURCC('X','V','I','D'))
