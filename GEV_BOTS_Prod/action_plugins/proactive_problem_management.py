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
            query1="assignment_group=306e23c52b1cee903439fb5dce91bf1f"
            incobj=Incidents() 
            fetch_enterprise_tickets=incobj.get_incident_details_by_query(query1)
            return {'status':'success','response': ''}
        except Exception as e:
            return {'status':'failed','response': str(e)}