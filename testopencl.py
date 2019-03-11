import CeleryPy
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
cmd='ls {}'.format(dir_path)
url='https://raw.githubusercontent.com/Vegnics/files_probe/master/get-pip.py'
try:
    from urllib.request import urlretrieve
    try:
        urlretrieve(url, '{}/get-pip.py'.format(dir_path))
        f = os.popen(cmd)
        out = f.read()
        CeleryPy.send_message(message=str(out), message_type='success', channel='toast')
    except:
        CeleryPy.send_message(message='File not found', message_type='error', channel='toast')
except ImportError:
    CeleryPy.send_message(message='Module error', message_type='error', channel='toast')





