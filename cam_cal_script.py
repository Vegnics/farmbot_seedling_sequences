import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import Capture
from Image import Image
from Parameters import Parameters
import requests
import subprocess
import json
database=DB()
params=Parameters()
imag=Image(params,database)
#y=x.get_image(50)
#y=x._get_bot_state()
#y=dict(y)['user_env']['camera']
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
#z=str(z)
imag.show()
send_message(message='bien'), message_type='success', channel='toast')
