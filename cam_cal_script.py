import os
import sys
from plant_detection.CeleryPy import log
from plant_detection.DB import DB
import plant_detection.Capture
import plant_detection.Image
import requests
x=DB()
y=x.api_get('peripherals/')
##log(y, message_type='error', title='FUNCO')
print(y)
