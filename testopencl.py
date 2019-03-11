import CeleryPy
import cv2
import os
import subprocess

CeleryPy.log(str(cv2.ocl.haveOpenCL()))
CeleryPy.log(str(cv2.getNumberOfCPUs()))
out = subprocess.Popen(['sudo','apt-get','install','python3-pip'], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
CeleryPy.log(str(stdout))
CeleryPy.log(str(stderr))
