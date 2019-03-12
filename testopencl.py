import CeleryPy
import os
def find_all(name, path):
    result = []
    for root, dirs, files in list(os.walk(path)):
        if name in files or name in dirs:
            result.append(os.path.join(root, name))
    return result

dir_path = os.path.dirname(os.path.realpath(__file__))
url='http://192.168.0.6:8000/Desktop/get-pip.py'
try:
    from urllib.request import urlretrieve
    try:
        urlretrieve(url, '/root/farmware/get-pip.py')
        CeleryPy.send_message(message='Downloading get-pip.py.....', message_type='warn', channel='toast')
    except:
        CeleryPy.send_message(message='File not found', message_type='error', channel='toast')
except ImportError:
    CeleryPy.send_message(message='Module error', message_type='error', channel='toast')
CeleryPy.wait(10000)
result=find_all('get-pip.py','/')
#a=os.popen('pip --version'.format(result[0]))
#result=a.read()
CeleryPy.send_message(message='YEAH'+'\n'+str(result), message_type='success', channel='toast')







