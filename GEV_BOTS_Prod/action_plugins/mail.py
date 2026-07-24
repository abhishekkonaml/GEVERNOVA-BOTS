from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64
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


warnings.filterwarnings("ignore") 




class ActionModule(ActionBase):
    def send_mail(self,incident_number,send_to,cc,configuration_item, short_dec):
        
        assert isinstance(send_to, list)
        server="smtprelay.gevernova.net"
        send_from="automatedassignmentnotification@gevernova.com"
        subject=" Ticket Assignment- {}".format(incident_number)
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Cc'] = COMMASPACE.join(cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        text='''
          <html>
          <body>

           <p>Hi,</p>
              <p>The ticket - {} has been assigned to you, as it could not be closed by the bot.

Please review and take the necessary action to resolve/close the ticket.</p>
<p>
<b>Ticket Details: </b>
description: {}
configuration_item: {}
</p>
           <p>Regards,<br>
           <b>Automation </b><br></p>
           
           
           </body>
           </html>'''.format(incident_number,short_dec, configuration_item)        
        
        msg.attach(MIMEText(text, 'html'))
        part = MIMEBase('application', "octet-stream")
        
                
        try: 
           smtp = smtplib.SMTP(server)
           #smtp.set_debuglevel(1)
           all_recipients= send_to + cc
           smtp.sendmail(send_from, all_recipients, msg.as_string())
           smtp.close()
           return "Mail sent successfully"
        except Exception as e:
           print(str(e))
           return "Unable to send mail"


    
    
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try:
           incident_number=self._task.args["incident"] 
           configuration_item=self._task.args["hostname"] 
           short_dec=self._task.args["short_description"]
           send_to=["Aishwarya.Shet@microland.com"]
           cc=["Aishwarya.Shet@microland.com"]
    
           mail_response=self.send_mail(incident_number,send_to,cc,configuration_item, short_dec)

           print(mail_response)
           return {'status': 'success','result': 'mail sent successfully'}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}



