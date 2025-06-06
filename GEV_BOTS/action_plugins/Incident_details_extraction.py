from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print("Current Python sys.path:", sys.path)

from GEV_DEV_Servicenow import Incidents

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            incident_no=self._task.args["incident_no"]
            host_pattern='Host: (.*)'
            interface_pattern="Datasource: Network Interfaces-(.*) "
            query="number={}?sso={}".format(incident_no,"503437104")
            incobj=Incidents()
            incident_details=incobj.get_incident_details_by_query(query)
            if type(incident_details)==list:
               description=incident_details[0]['description']
               hostname=re.findall(host_pattern,description)
               interface=re.findall(interface_pattern,description)
               if len(hostname)>0:
                  hostname=re.findall(host_pattern,description)[0]
               else:
                  hostname=''
               if len(interface)>0:
                  interface=re.findall(interface_pattern,description)[0]
               else:
                  interface=''
               return {'status':'success','hostname':hostname,'interface':interface,'description':description}
            else:
               return {'status':'failed','hostname':'Incident not found','interface':'Incident not found','description':''}
        except Exception as e:
           return  {'status':'error','hostname':'Error in Incident Extraction','interface':'Error in Incident Extraction','description':str(e)}  
