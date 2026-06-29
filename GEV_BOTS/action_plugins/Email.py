from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
from GEV_Prod_Servicenow import CMDB
#from GEV_Stage_Servicenow import CMDB
import math
import re
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib
#import smtplibNe

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            send_to=self._task.args["send_to"]
            ch_number=self._task.args["ch_number"]
            cc=self._task.args["cc"]
            assert isinstance(send_to, list)
            server="smtprelay.gevernova.net"
            send_from="automatedchangenotification@gevernova.com"
            subject="Manual Processing Required, Change Closure Failed - {}".format(ch_number)
            msg = MIMEMultipart()
            msg['From'] = send_from
            msg['To'] = COMMASPACE.join(send_to)
            msg['Cc'] = COMMASPACE.join(cc)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            text='''
            Hi,

This is an automated notification to inform you that the bot will be unable to complete the closure of the change - {} request due to a access issue.

Kindly review the change and proceed with manual closure at your earliest convenience.

We apologize for the inconvenience'''.format(ch_number)
            
            
            msg.attach(MIMEText(text))
            part = MIMEBase('application', "octet-stream")
            
            '''with open(htmlfile,'r') as file:
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename={}'.format(htmlfile))
            msg.attach(part)'''
                    
            try: 
                smtp = smtplib.SMTP(server)
                res=smtp.sendmail(send_from, send_to, msg.as_string())
                smtp.close()
                print(res)
                return "Mail sent successfully"
            except Exception as e:
                print(str(e))
                return "Unable to send mail"
            
        except Exception as e:
            print(str(e))
            return "Unable to fetch details to send mail"
