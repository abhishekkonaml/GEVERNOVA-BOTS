from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from GEV_Prod_Servicenow import Incidents

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
               description=incident_details[0]['short_description']
               assignment_group=incident_details[0]['assignment_group']

               #Bot Classification Logic
               #Renewables node down bot
               #Renewables node down bot
               if assignment_group == 'GE Renewables Network Connectivity Team' and 'down' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  created_on=incident_details[0]['sys_created_on']
                  updated_desc=description
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Renewables Idleinterval','updated_desc': updated_desc, 'created_on': created_on}
               
               
               
               # Usecase-1: Connection Down Bot 
               elif 'network interface' in description.lower() and "statusflap" in description.lower(): 
                  KB_Article='[GEVKB0017428]'
                  desc=description[:145]
                  updated_desc=KB_Article + desc
                  #host_pattern="host (.*) is experiencing"
                  host_pattern="- (.*)Network Interfaces"
                  #description=description.replace('\\n','')
                  #interface_pattern="packets on (.*) \["
                  #interface_pattern="StatusFlapNetwork interface (.*) \["
                  interface_pattern="interface (.*) \["
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
                 
                  return {'status':'success','hostname':hostname,'interface':interface,'description':description,'botname': 'StatusFlap','ap_name':ap_name, 'updated_desc': updated_desc}
               
               #Usecase2 - StatusAlert
               elif 'network interface' in description.lower() and "statusflap" not in description.lower() and "status": 
                  KB_Article='[GEVKB0015490]'
                  desc=description[:145]
                  updated_desc=KB_Article + desc
                  
                  #host_pattern="host (.*) is experiencing"
                  #description=description.replace('\\n','')
                  host_pattern="- (.*)Network Interfaces"
                  #interface_pattern="packets on (.*) \["
                  interface_pattern="Interface (.*) \["
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
                 
                  return {'status':'success','hostname':hostname,'interface':interface,'description':description,'botname': 'StatusAlert','updated_desc': updated_desc}


               elif 'down' in description.lower():
                  KB_Article='[GEVKB0015329]'
                  desc=description[:145]
                  updated_desc=KB_Article + desc
                  
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Node down','updated_desc': updated_desc}

               elif 'temperature sensors' in description.lower():
                  hostname=''
                  hostname=incident_details[0]['cmdb_ci']
                  if hostname == '':
                     return {'status': 'failed','reason': 'Bot failed to extract the details for execution'}
                  return {'status':'success','hostname':hostname,'description':description,'botname': 'Temperature Sensor'}
                  
               # When no bot found
               else:
                  return {'status': 'failed','reason':'Bot not exist!'}
            else:
               return {'status':'failed','reason': 'Incident not found'}
        except Exception as e:
           return  {'status':'error','reason': 'Incident Parsing Error - {}'.format(str(e))}