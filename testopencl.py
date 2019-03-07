import CeleryPy
import cv2

CeleryPy.log(str(cv2.ocl.haveOpenCL()))
CeleryPy.log(str(cv2.getNumberOfCPUs()))
