import CeleryPy
import cv2
import os

CeleryPy.log(str(cv2.ocl.haveOpenCL()))
dir_path = os.path.dirname(os.path.realpath(__file__))
getpip=dir_path+'/get-pip.py'
cmd='python3 {}'.format(getpip)
os.system(cmd)

