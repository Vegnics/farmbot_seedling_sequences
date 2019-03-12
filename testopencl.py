import CeleryPy
import os
import subprocess
proc = subprocess.Popen(['locate','LOGGING'],shell=True)
outs, errs = proc.communicate()
CeleryPy.send_message(message='TUDO BEM', message_type='success', channel='toast')







