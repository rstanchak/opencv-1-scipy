#!/usr/bin/python
from opencv.cv import cvCreateMemStorage, cvCreateSeq, cvSeqPush, CvSeq_Point, sizeof_CvPoint, sizeof_CvSeq, cvPoint 

storage = cvCreateMemStorage(0)
seq = cvCreateSeq( 0, sizeof_CvSeq, sizeof_CvPoint, storage );
cvSeqPush(seq, cvPoint(0,1))
cvSeqPush(seq, cvPoint(1,0))
ptseq = CvSeq_Point.cast(seq)

print ptseq[0]
print ptseq[1]

for pt in ptseq:
    print pt
