from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GEV_Prod_Servicenow import Incidents

warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try:
           incobj=Incidents() 
           
           
           return {'status': 'success','response': 'Successfully triggered Eligible tickets'}
        except Exception as e:
            return {'status': 'failed','response':str(e)}
