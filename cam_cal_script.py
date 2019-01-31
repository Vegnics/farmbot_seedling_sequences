import os
import sys
from CeleryPy import log
from DB import DB
import Capture 
import Image
x=print(DB.getcoordinates())
log(x, message_type='error', title='FUNCO')

