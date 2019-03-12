import CeleryPy
import os
def find_all(name, path):
    result = []
    for root, dirs, files in list(os.walk(path)):
        if name in files or name in dirs:
            result.append(os.path.join(root, name))
    return result
f=os.popen('ls /root/.cache/pip')
result=f.read()
CeleryPy.send_message(message='YEAH'+'\n'+str(result), message_type='success', channel='toast')







