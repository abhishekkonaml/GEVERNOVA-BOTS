from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import warnings
from GEV_Prod_Servicenow import Incidents
from datetime import datetime, timezone
incobj=Incidents()
warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            #query1="assignment_group=609fb9273b426690e2d5cbc964e45a7a^state!=6^state!=7"
            
            query1="assignment_group=306e23c52b1cee903439fb5dce91bf1f^short_descriptionLIKEstatusflap^state=1^ORstate=2"
            incobj=Incidents()
            fetch_stalled_tickets=incobj.get_incident_details_by_query(query1)
            for stalled_ticket in fetch_stalled_tickets:
                Number=stalled_ticket['number']
                group='HQ CTO Network Enterprise Site Support'
                openedAt=stalled_ticket['sys_created_on']
                print(Number,openedAt)
                current_utc_time = datetime.now(timezone.utc)
                tickettime=datetime.strptime(openedAt,"%m-%d-%Y %I:%M:%p")
                utctime=datetime.strptime(current_utc_time,"%m-%d-%Y %I:%M:%S %p")
                print(utctime,tickettime)
                print("=-"*35)
            return {'status': 'success', 'response': 'Stalled tickets reassigned successfully'}
        except Exception as e:
            return {'status': 'failed','response':str(e)}