from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from BtoBtransaction import GrabIncidents
from GEV_Prod_Servicenow import Incidents
from awx_trigger import AWX_Trigger
warnings.filterwarnings("ignore") 
from coreappapi import CoreApp

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try:
           incobj=Incidents() 
           coreobj=CoreApp()
           query1="assignment_group=306e23c52b1cee903439fb5dce91bf1f^descriptionLIKEstatus^descriptionNOT LIKEstatusflap^descriptionLIKEinterfaces^sys_created_onONLast 15 minutes@javascript:gs.beginningOfLast15Minutes()@javascript:gs.endOfLast15Minutes()^state=1^ORstate=2"
           #query1="assignment_group=306e23c52b1cee903439fb5dce91bf1f^descriptionLIKEstatus^descriptionNOT LIKEstatusflap^descriptionLIKEinterfaces^sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()^state=1^ORstate=2"
           
           fetch_status_tickets=incobj.get_incident_details_by_query(query1)
           if type(fetch_status_tickets)==list:
              for status_ticket in fetch_status_tickets:
                  if "Intelligeni Bot" not in status_ticket['comments_and_work_notes']:
                     incident_no=status_ticket['number']
                     desc=status_ticket['short_description']
                     org_assignment_group=status_ticket['assignment_group']
                     
                     response1=coreobj.coreapp_trigger(incident_no,desc,org_assignment_group)
                     print({'TicketNo' : incident_no, 'Problem': 'StatusAlert', 'Status': response1})
           #query2="state=1^ORstate=2^short_descriptionLIKEis down^assignment_group=306e23c52b1cee903439fb5dce91bf1f^sys_created_onONLast 45 minutes@javascript:gs.beginningOfLast45Minutes()@javascript:gs.endOfLast45Minutes()"
           query2="sys_created_onBETWEENjavascript:gs.dateGenerate('2025-12-30','00:00:00')@javascript:gs.dateGenerate('2025-12-30','23:59:59')^assignment_group=609fb9273b426690e2d5cbc964e45a7a^state=2"
           query3="assignment_group=306e23c52b1cee903439fb5dce91bf1f^short_descriptionLIKEstatusflap^state=1^ORstate=2^sys_created_onONLast 45 minutes@javascript:gs.beginningOfLast45Minutes()@javascript:gs.endOfLast45Minutes()"
           fetch_statusflap_tickets=incobj.get_incident_details_by_query(query3)
           if type(fetch_statusflap_tickets)==list:
              for statusflap_ticket in fetch_statusflap_tickets:
                  if "Intelligeni Bot" not in statusflap_ticket['comments_and_work_notes']:
                     incident_no=statusflap_ticket['number']
                     desc=statusflap_ticket['short_description']
                     org_assignment_group=statusflap_ticket['assignment_group']
                     
                     response1=coreobj.coreapp_trigger(incident_no,desc,org_assignment_group)
                     print({'TicketNo' : incident_no, 'Problem': 'StatusFlap', 'Status': response1})
           #query2="state=2^ORstate=1^descriptionLIKEis down^assignment_group=306e23c52b1cee903439fb5dce91bf1f^sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()"
           fetch_idleinterval_tickets=incobj.get_incident_details_by_query(query2)
           #print(fetch_idleinterval_tickets)
           #print("=-=-=---=-00-----------------")
           for idleinterval_ticket in fetch_idleinterval_tickets:
               if "Intelligeni Bot" not in idleinterval_ticket['comments_and_work_notes']: #and  "GEVINC0055402" == idleinterval_ticket['number']:
                  incident_no=idleinterval_ticket['number']
                  desc=idleinterval_ticket['short_description']
                  org_assignment_group=idleinterval_ticket['assignment_group']
                  #coreobj=CoreApp()
                  response1=coreobj.coreapp_trigger(incident_no,desc,org_assignment_group)
                  print({'TicketNo' : incident_no, 'Problem': 'IdleInterval','Status': response1})
                  #break
           
           return {'status': 'success','response': 'Successfully triggered Eligible tickets'}
        except Exception as e:
            return {'status': 'failed','response':str(e)}
