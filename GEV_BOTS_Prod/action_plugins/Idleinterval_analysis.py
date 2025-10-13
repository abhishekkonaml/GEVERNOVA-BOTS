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
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders


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
           print(len(fetch_node_tickets))
           if(len(fetch_node_tickets) >=1 ):
               print("send mail")
               op=self.send_mail(datetime.now())
               print(op)
           else:
               print("dont send mail")
           #print(type(fetch_node_tickets))

           if "Failed" in fetch_node_tickets:
              return {'status':'failed','response': 'Failed to fetch the Node down tickets'}

       
        except Exception as e:
            return {'status': 'failed','response':str(e)}
    def send_mail(self,today_date,server="smtprelay.gevernova.net"):
        send_from="automatedbotdailyanalysis@gevernova.com"
        send_to="Aishwarya.shet@microland.com"
        subject="ALERT".format(today_date)
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        text='''
           Hi Aishwarya, 
    
           There are tickets in bot queue.
    
           Regards, 
           Automation Team.
          
        '''

                
        try: 
           smtp = smtplib.SMTP(server)
           smtp.sendmail(send_from, send_to, msg.as_string())
           smtp.close()
           return "Mail sent successfully"
        except:
           return "Unable to send mail"
