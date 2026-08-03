from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
from GEV_Prod_Servicenow import Incidents
import math

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           incident=self._task.args["incident"]
           follow_up=self._task.args["follow_up"]

           incobj=Incidents()
           return {'status': 'success', 'result': incobj.Change_to_OnHold_state(incident,follow_up)}
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}

