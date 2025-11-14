from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
from GEV_Prod_Servicenow import CMDB
from GEV_Prod_Servicenow import Incidents
import math

warnings.filterwarnings("ignore")


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           Query=self._task.args["query1"]
           incobj=Incidents()
           chobj=CMDB()
           fetch_changed_tickets=incobj.get_change_details_by_query(Query)
            
           ch_list=[]
           tasks_data_list=[]
           for change_ticket in fetch_changed_tickets:
               Number=change_ticket['number']
               ch_list.append(Number)
           if(len(ch_list) == 0):
               result='No device silencing tickets'
           else:
               result=ch_list
           for i in result:
               sys_id = chobj.get_ci_affected_details_change(i)
               sys = sys_id['result'][0]['sys_id']
               tasks_data = chobj.get_tasks_by_change_sys_id(sys)
               data = tasks_data['result']
               tasks_data_list.append(data)
            
               
   
           return {'status': 'success', 'result': tasks_data_list} 
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}