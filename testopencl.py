import CeleryPy
import os
import subprocess
proc = subprocess.Popen(['locate','LOGGING'])
try:
    outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()
CeleryPy.send_message(message=str(outs), message_type='success', channel='toast')







