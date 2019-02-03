import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import json
from Parameters import Parameters
import requests

x=DB()
y=x.get_image(52)
