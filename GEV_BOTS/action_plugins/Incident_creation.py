from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import warnings
from GEV_Prod_Servicenow import Incidents
#from GEV_Stage_Servicenow import Incidents
from datetime import datetime
import pytz
incobj=Incidents()
warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            cmdb=self._task.args["ci"]
            cmdb_ci= cmdb 
            ch_number=self._task.args["change_number"]
            short_description='{} is unreachable.Node down after device silencing.'.format(cmdb_ci)
            description='''{} is unreachable.Node down after device silencing.
                                 It's a notification alert generated as part of the device silencing change : {}'''.format(cmdb_ci,ch_number)

            work_notes='It is a notification alert generated as part of the device silencing change'
            
            incobj=Incidents()
            CreateIncident=incobj.incident_creation(504018887,504018887,'Monitoring','Network Monitoring','HQ CTO Network Enterprise Site Support',short_description,description,'3',work_notes,cmdb_ci)
            
            result=CreateIncident
            print(result)
            
            if(result['number'] != ''):
                Incident_number=result['number']
                notes= '{} is currently not reachable; following incident has been created - {}'.format(cmdb_ci,Incident_number)
                incobj.update_notes_change(ch_number,notes)
            
                
                
           
            return {'status': 'success', 'response': result}
        except Exception as e:
            return {'status': 'failed','response':str(e)}