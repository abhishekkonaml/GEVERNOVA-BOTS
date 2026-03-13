from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#from GEV_DEV_Servicenow import Incidents
from GEV_Prod_Servicenow import CMDB

warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           ch_number=self._task.args['change_no']
           work_notes=self._task.args['work_note']
           #SSOid=self.task.args['ssoid']
           chobj=CMDB()
           res=chobj.change_assigned_to(ch_number,work_notes)
           
           return {'status': 'success','result': res}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}