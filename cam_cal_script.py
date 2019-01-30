import os
import sys
from CeleryPy import log
from DB import DB
import Capture 
import Image

X=DB().getcoordinates()
log(X, message_type='error', title='FUNCO')

