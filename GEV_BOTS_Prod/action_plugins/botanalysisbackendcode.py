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
           
           query1="assignment_group=306e23c52b1cee903439fb5dce91bf1f^descriptionLIKEstatus^descriptionNOT LIKEstatusflap^descriptionLIKEinterfaces^opened_atONYesterday@javascript:gs.beginningOfYesterday()@javascript:gs.endOfYesterday()^ORopened_atONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()"
           fetch_status_tickets=incobj.get_incident_details_by_query(query1)
           
           if "Failed" in fetch_status_tickets:
              return {'status':'failed','response': 'Failed to fetch the Status Alert tickets'}

           statusalert={'StatusAlert':[]}
           for status_ticket in fetch_status_tickets:
               
               
               summary=''
               status1=''
               if "Intelligeni Bot" in status_ticket['comments_and_work_notes']:
                   bot_touched_count+=1
                   
                   if "closing the incident" in status_ticket['comments_and_work_notes']:
                      closed+=1
                   for comments in status_ticket['comments_and_work_notes'].split("\n\n"):
                       if "Summary" in comments:
                           summary=comments
                       if "hence reassigned" in comments and "Summary" not in comments:
                           status1=comments
                       elif "closing the incident" in comments:
                           status1=comments
                       
                   statusalert['StatusAlert'].append({'Number': status_ticket['number'], 'Summary': summary, 'Status': status1})
               if "Intelligeni Bot" not in status_ticket['comments_and_work_notes']:
                  bot_not_touched_count+=1
               
           return {'status':'success','response': {'Bot touched data': bot_touched_count, 'Bot not touched data': bot_not_touched_count,'Closed': closed,'StatusAlert':statusalert['StatusAlert']}   }
                  







        except Exception as e:
            return {'status': 'failed','response':str(e)}
