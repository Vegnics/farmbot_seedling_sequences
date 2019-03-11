import CeleryPy
import cv2
import os

CeleryPy.log(str(cv2.ocl.haveOpenCL()))
CeleryPy.log(str(cv2.getNumberOfCPUs()))
cmd='sudo apt-get install python3-pip'
f=os.popen(cmd)
out=f.read()
CeleryPy.log(str(out))

