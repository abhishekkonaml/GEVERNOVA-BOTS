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
           down_alert=0
           bot_not_touched_tickets=[]
           query1="assignment_group=306e23c52b1cee903439fb5dce91bf1f^descriptionLIKEstatus^descriptionNOT LIKEstatusflap^descriptionLIKEinterfaces^opened_atONYesterday@javascript:gs.beginningOfYesterday()@javascript:gs.endOfYesterday()^ORopened_atONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()"
           query2="descriptionLIKEis down^assignment_group=306e23c52b1cee903439fb5dce91bf1f^sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()^ORsys_created_onONYesterday@javascript:gs.beginningOfYesterday()@javascript:gs.endOfYesterday()"
           fetch_status_tickets=incobj.get_incident_details_by_query(query1)
           fetch_down_tickets=incobj.get_incident_details_by_query(query2)
           if "Failed" in fetch_status_tickets:
              return {'status':'failed','response': 'Failed to fetch the Status Alert tickets'}
           if "Failed" in fetch_down_tickets:
              return {'status':'failed','response': 'Failed to fetch the Idle interval tickets'}
           statusalert={'StatusAlert':{'status_count':'','tickets':[]}}
           downalert={'DownAlert':{'status_count':'','tickets':[]}}

           for down_ticket in fetch_down_tickets:
               
               
               summary2=''
               status2=''
               if "Intelligeni Bot" in down_ticket['comments_and_work_notes']:
                   bot_touched_count+=1
                   down_alert+=1
                   if "504018887" in down_ticket['assigned_to']:
                      closed+=1
                   for comments in down_ticket['comments_and_work_notes'].split("\n\n"):
                       if "Summary" in comments:
                           summary2=comments
                       if "hence reassigned" in comments and "Summary" not in comments:
                           status2=comments
                       elif "Closing the incident" in comments:
                           status2=comments
                       
                   downalert['DownAlert']['tickets'].append({'Number': down_ticket['number'], 'Summary': summary2, 'Status': status2,'OpenedAt': down_ticket['sys_created_on']})
               if "Intelligeni Bot" not in down_ticket['comments_and_work_notes']:
                  bot_not_touched_count+=1
                  bot_not_touched_tickets.append({'Number': down_ticket['number'],'OpenedAt': down_ticket['sys_created_on'],'ShortDescription':down_ticket['short_description']})





           for status_ticket in fetch_status_tickets:
               
               
               summary=''
               status1=''
               if "Intelligeni Bot" in status_ticket['comments_and_work_notes']:
                   bot_touched_count+=1
                   status_alert+=1
                   if "closing the incident" in status_ticket['comments_and_work_notes']:
                      closed+=1
                   for comments in status_ticket['comments_and_work_notes'].split("\n\n"):
                       if "Summary" in comments:
                           summary=comments
                       if "hence reassigned" in comments and "Summary" not in comments:
                           status1=comments
                       elif "closing the incident" in comments:
                           status1=comments
                       
                   statusalert['StatusAlert']['tickets'].append({'Number': status_ticket['number'], 'Summary': summary, 'Status': status1,'OpenedAt': status_ticket['sys_created_on']})
               if "Intelligeni Bot" not in status_ticket['comments_and_work_notes']:
                  bot_not_touched_count+=1
                  bot_not_touched_tickets.append({'Number': status_ticket['number'],'OpenedAt': status_ticket['sys_created_on'],'ShortDescription':status_ticket['short_description']})
           statusalert['StatusAlert']['status_count']=status_alert 
           return {'status':'success','response': {'Bot touched data': bot_touched_count, 'Closed': closed, 'Bot not touched data': {'count': bot_not_touched_count,'tickets':bot_not_touched_tickets},'StatusAlert':statusalert['StatusAlert'],'IdleIntervalAlert': downalert['DownAlert']}   }
                  







        except Exception as e:
            return {'status': 'failed','response':str(e)}
