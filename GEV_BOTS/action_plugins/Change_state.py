from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
from GEV_Stage_Servicenow import CMDB
import math

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           ch_number=self._task.args["change"]
           ch_state=self._task.args["state"]
           
           if(ch_state == 'implement'):
               chobj=CMDB()
               return {'status': 'success', 'result': chobj.state_change(ch_number,ch_state)}
           if(ch_state == 'review'):
               chobj=CMDB()
               tasks = chobj.get_tasks_by_change(ch_number)
               result = tasks['result'][0]['affected_ci_list']
               print(result)
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}

