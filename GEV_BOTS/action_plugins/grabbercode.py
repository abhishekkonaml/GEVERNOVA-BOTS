from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
#from BtoBtransaction import GrabIncidents
warnings.filterwarnings("ignore")
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print("Current Python sys.path:", sys.path)

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           grabobj=GrabIncidents()
           grabincidents=grabobj.getincidents()['Record']
           incidents=[incident['Payload']['RequestInfo']['number'] for incident in grabincidents if "network interfaces" in incident['Payload']['RequestInfo']['description'].lower()]
           return {'status': 'success','result': incidents}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}