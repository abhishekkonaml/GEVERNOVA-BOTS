from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from GEV_DEV_Servicenow import Incidents

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            incident_no=self._task.args["incident_no"]
            #host_pattern='Host: (.*)'
            #interface_pattern="Datasource: Network Interfaces-(.*) "
            
            
            incobj=Incidents()
            incident_details=incobj.get_incident_details_by_incident_number(incident_no)
            print(incident_details)
            print("----------"*25)
            if type(incident_details)==list:
               description=incident_details[0]['description']
               
               #Bot Classification Logic
               
               # Usecase-1: Connection Down Bot 
               if 'network interface' in description.lower() and "statusflap" in description.lower(): 
                  #host_pattern="host (.*) is experiencing"
                  host_pattern="- (.*)Network Interfaces"
                  #interface_pattern="packets on (.*) \["
                  interface_pattern="Network Interfaces-(.*) \["
                  hostname=re.findall(host_pattern,description)
                  interface=re.findall(interface_pattern,description)
                  if len(hostname)>0:
                     hostname=re.findall(host_pattern,description)[0].strip()
                  else:
                     hostname=''
                  if len(interface)>0:
                     interface=re.findall(interface_pattern,description)[0].strip()
                  else:
                     interface=''
                  if hostname == '' and interface=='':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'interface':interface,'description':description,'botname': 'StatusFlap'}
               elif 'down' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Node down'}

                  
               # When no bot found
               else:
                  return {'status': 'failed','reason':'Bot not exist!'}
            else:
               return {'status':'failed','reason': 'Incident not found'}
        except Exception as e:
           return  {'status':'error','reason': 'Incident Parsing Error'}