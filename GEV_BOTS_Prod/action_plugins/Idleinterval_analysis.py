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
           incobj=Incidents() 
           bot_touched_count=0
           bot_not_touched_count=0
           closed=0
           status_alert=0
           status_alert_not_touched=0
           down_alert=0
           down_alert_not_touched=0
           status_closed=0
           down_closed=0
           bot_not_touched_tickets=[]
           
           query1="state=2^short_descriptionLIKEis down^assignment_group=306e23c52b1cee903439fb5dce91bf1f"
           fetch_node_tickets=incobj.get_incident_details_by_query(query1)
           print(fetch_node_tickets)

           if "Failed" in fetch_node_tickets:
              return {'status':'failed','response': 'Failed to fetch the Node down tickets'}

           #return {'status':'success','response': {'Bot touched data': bot_touched_count, 'Closed': closed, 'Bot not touched data': {'count': bot_not_touched_count,'tickets':bot_not_touched_tickets},'StatusAlert':statusalert['StatusAlert'],'IdleIntervalAlert': downalert['DownAlert']}   }
                  

        except Exception as e:
            return {'status': 'failed','response':str(e)}
