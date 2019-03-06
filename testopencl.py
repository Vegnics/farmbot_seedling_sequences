import CeleryPy
import cv2

CeleryPy.log(str(cv2.ocl.setUseOpenCL(True)))
CeleryPy.log(str((cv2.ocl.haveOpenCL())))
