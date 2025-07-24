from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from BtoBtransaction import GrabIncidents
from GEV_DEV_Servicenow import Incidents
from awx_trigger import AWX_Trigger
warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           grabobj=GrabIncidents()
           incobj=Incidents()
           grabincidents=grabobj.getincidents()['Record']
           awx_uname = task_vars["generic_username"]
           awx_pass = task_vars["generic_password"]
           awx_url=task_vars['awx_url']
           incidents=[]
           url = awx_url+"job_templates/12/launch/"
           for incident in grabincidents:
               if "statusflap" in incident['Payload']['RequestInfo']['description'].lower():
                    state_inc=incobj.get_incident_details_by_incident_number(incident['Payload']['RequestInfo']['number'])
                    
                    if "New" in state_inc[0]['state']:
                       incidents.append(incident['Payload']['RequestInfo']['number'])
               elif "down" in incident['Payload']['RequestInfo']['description'].lower():
                       #incidents.append(incident['Payload']['RequestInfo']['number'])
                       pass
           print(incidents)            
           #incidents=[incident['Payload']['RequestInfo']['number'] for incident in grabincidents if "network interfaces" in incident['Payload']['RequestInfo']['description'].lower() and "statusflap" in incident['Payload']['RequestInfo']['description'].lower() and "new" in incident['Payload']['RequestInfo']['state'].lower()]
           #incidents=["GEVINC0029674","GEVINC0029678"]
           awxobj=AWX_Trigger()
           #print(incobj.assigned_to_bot(incidents[0]))
           #triggering_template=awxobj.trigger(url,awx_uname,awx_pass,incidents[0])
           #print(triggering_template)
           #print("="*50)
           return {'status': 'success','result': incidents}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}