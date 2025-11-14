from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
from GEV_Prod_Servicenow import CMDB
import math

warnings.filterwarnings("ignore")


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           print('inside script')
           ch_number=self._task.args["change"]
           
           
           
           chobj=CMDB()
           sys_id = chobj.get_ci_affected_details_change(ch_number)
           sys = sys_id['result'][0]['sys_id']
           tasks_data = chobj.get_tasks_by_change_sys_id(sys)
           return {'status': 'success', 'result': tasks_data} 
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}