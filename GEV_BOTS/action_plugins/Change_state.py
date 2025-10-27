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
               results=chobj.state_change(ch_number,ch_state)
               return {'status': 'success', 'result': results}
           if(ch_state == 'review'):
               task_numbers=[]
               chobj=CMDB()
               sys_id = chobj.get_ci_affected_details_change(ch_number)
               sys = sys_id['result'][0]['sys_id']
               tasks_data = chobj.get_tasks_by_change_sys_id(sys)
               for task in tasks_data:
                   print(task)
                
            

               
               
               return {'status': 'success', 'result': sys}
                   
                
            
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}

