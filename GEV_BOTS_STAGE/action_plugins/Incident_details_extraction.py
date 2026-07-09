from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from GEV_Stage_Servicenow import Incidents

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            incident_no=self._task.args["incident_no"]
            #host_pattern='Host: (.*)'
            #interface_pattern="Datasource: Network Interfaces-(.*) "
            
            
            incobj=Incidents()
            #print(incobj.assigned_to_bot(incident_no))
            incident_details=incobj.get_incident_details_by_incident_number(incident_no)
            print(incident_details)
            print("----------"*25)
            if type(incident_details)==list:
               description=incident_details[0]['description']
               assignment_group=incident_details[0]['assignment_group']
               #Bot Classification Logic
               #Renewables node down bot
               if assignment_group == 'HQ DT CTO Network Core 3PR' and 'down' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  updated_desc=description
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Renewables Idleinterval','updated_desc': updated_desc}
               
               # Usecase-1: Connection Down Bot 
               elif 'network interface' in description.lower() and "statusflap" in description.lower(): 
                  #host_pattern="host (.*) is experiencing"
                  host_pattern="- (.*)Network Interfaces"
                  #interface_pattern="packets on (.*) \["
                  interface_pattern="Network Interfaces-(.*) \["
                  hostname=re.findall(host_pattern,description)
                  interface=re.findall(interface_pattern,description)
                  
                  #Fetching WLC
                  ap_pattern="Int_Mon (.*) on"
                  aps=re.findall(ap_pattern,description)
                  if len(aps)>0:
                     ap_name=[i for i in aps if "wd" in i][0]
                  else:
                     ap_name=''

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
                 
                  return {'status':'success','hostname':hostname,'interface':interface,'description':description,'botname': 'StatusFlap','ap_name':ap_name}
               
               #Usecase2 - StatusAlert
               elif 'network interface' in description.lower() and "statusflap" not in description.lower() and "status": 
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
                 
                  return {'status':'success','hostname':hostname,'interface':interface,'description':description,'botname': 'StatusAlert'}


               elif 'down' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Node down'}
               
               elif 'temperature sensors' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Temperature Sensor'}
               
               elif 'power supply' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Power Supply Firewall'}

                  
               # When no bot found
               else:
                  return {'status': 'failed','reason':'Bot not exist!'}
            else:
               return {'status':'failed','reason': 'Incident not found'}
        except Exception as e:
           return  {'status':'error','reason': 'Incident Parsing Error'}