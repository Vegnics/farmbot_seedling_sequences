import CeleryPy
import os
cmd='locate pip'
f=os.popen(cmd)
out=f.read()
CeleryPy.send_message(message=str(out), message_type='success', channel='toast')







