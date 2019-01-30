import os
import sys
from CeleryPy import log
from DB import DB
import Capture 
import Image


log(DB.getcoordinates(), message_type='error', title='FUNCO')

