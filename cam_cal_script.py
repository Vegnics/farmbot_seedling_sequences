import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
import json
#from subprocess import call

x=DB()
response = x.api_get('images/' + str(52))
#filename_path = upload_path(y)
#retcode = call(["raspistill", "-w", "640", "-h", "480", "-o", filename_path])
#y=x._get_bot_state()
#y=dict(y)['user_env']['camera']
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
#z=str(z)
send_message(message=str(response.json()), message_type='success', channel='toast')
y=x.get_image(52)

