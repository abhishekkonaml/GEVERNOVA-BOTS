from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import warnings
#from GEV_Prod_Servicenow import Incidents
from GEV_Stage_Servicenow import Incidents
from datetime import datetime
import pytz
incobj=Incidents()
warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            
            short_description=self._task.args["sh_description"]
            description=self._task.args["description"]
            work_notes='It is a notification alert generated as part of the device silencing change'
            cmdb_ci=self._task.args["ci"]
            incobj=Incidents()
            CreateIncident=incobj.incident_creation(504018887,504018887,'Monitoring','Network Monitoring','HQ CTO Network Enterprise Site Support',short_description,description,'3',work_notes,cmdb_ci)
            
            result=CreateIncident
                
                
           
            return {'status': 'success', 'response': result}
        except Exception as e:
            return {'status': 'failed','response':str(e)}