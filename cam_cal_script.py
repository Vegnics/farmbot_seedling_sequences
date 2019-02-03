import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
from Image import Image
import json
from Parameters import Parameters
import requests

x=DB()
y=x.get_image(52)
parms=Parameters()
z=Image(parms,x)
z.load(y)
#z.show()
