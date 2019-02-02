import os
import sys
from CeleryPy import log
from CeleryPy import send_message
from DB import DB
from subprocess import call

def upload_path(filename):
    try:
        images_dir = os.environ['IMAGES_DIR']
    except KeyError:
        images_dir = '/tmp/images'
    path = images_dir + os.sep + filename
return path

x=DB()
y=x.get_image(50)
filename_path = upload_path(y)
retcode = call(["raspistill", "-w", "640", "-h", "480", "-o", filename_path])
#y=x._get_bot_state()
#y=dict(y)['user_env']['camera']
#log(print(os.environ['API_TOKEN']), message_type='error', title='FUNCO')
#z=str(z)
send_message(message='bien', message_type='success', channel='toast')
