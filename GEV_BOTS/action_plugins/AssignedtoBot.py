from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GEV_DEV_Servicenow import Incidents

warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           incident=task_vars['incident']
           incobj=Incidents()
           result=incobj.assigned_to_bot(incident)
           
           return {'status': 'success','result': result}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}