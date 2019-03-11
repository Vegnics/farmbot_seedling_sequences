import CeleryPy
import cv2
import os

CeleryPy.log(str(cv2.ocl.haveOpenCL()))
CeleryPy.log(str(cv2.getNumberOfCPUs()))
cmd='pip install cython'
f=os.popen(cmd)
out=f.read()
CeleryPy.log(str(out))

