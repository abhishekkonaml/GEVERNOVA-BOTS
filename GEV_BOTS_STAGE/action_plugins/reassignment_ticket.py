from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from GEV_DEV_Servicenow import Incidents
import math

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           incident=self._task.args["incident"]
           group=self._task.args["group"]
           
           incobj=Incidents()
           return {'status': 'success', 'result': incobj.reassignment(incident,group)}
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}

