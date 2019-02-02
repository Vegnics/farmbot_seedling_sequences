import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import Capture
import Image
import requests
import subprocess
import json
x=DB()
y=x.get_image(50)
z=json.loads(y)
#y=x._get_bot_state()
#y=dict(y)['user_env']['camera']
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
z=str(z)
send_message(message=y, message_type='success', channel='toast')
