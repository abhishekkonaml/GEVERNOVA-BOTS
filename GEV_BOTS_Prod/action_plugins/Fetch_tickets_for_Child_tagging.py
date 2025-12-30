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
            
            Query=self._task.args["query1"]
            incobj=Incidents()
            fetch_all_tickets_with_parent=incobj.get_incident_details_by_query(Query)
            
            Incident_list=[]
            for incident_ticket in fetch_all_tickets_with_parent:
                Number=incident_ticket['number']
                Incident_list.append(Number)
            if(len(Incident_list) <= 8):
                result='Trigger email'
            
    
            return {'status': 'success', 'response': result}
        except Exception as e:
            return {'status': 'failed','response':str(e)}