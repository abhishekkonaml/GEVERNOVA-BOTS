from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import warnings
from GEV_Prod_Servicenow import Incidents
from datetime import datetime
import pytz
incobj=Incidents()
warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            
            Number=self._task.args["INC_Number"]
            incobj=Incidents()
            fetch_parent_details=incobj.get_parent_details_by_number(Number)
            
            result=fetch_parent_details['result'][0]["parent_incident"]
            return {'status': 'success', 'response': result}
        except Exception as e:
            return {'status': 'failed','response':str(e)}