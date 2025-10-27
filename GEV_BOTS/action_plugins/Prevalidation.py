from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from BtoBtransaction import GrabIncidents
from GEV_Stage_Servicenow import CMDB
from awx_trigger import AWX_Trigger
warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            Change_number=self._task.args["Change"]
        except Exception as e:
            print("Change number is missing")

        chobj=CMDB()
        result=chobj.get_ci_affected_details_change(Change_number)
        return(result[0]['affected_ci_list'])
   

