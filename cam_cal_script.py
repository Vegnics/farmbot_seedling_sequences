import os
import sys
from CeleryPy import log
from DB import DB
import Capture 
import Image
[x,y,z]=DB().getcoordinates(test_coordinates=True)
log('funcaaaaa', message_type='error', title='FUNCO')

