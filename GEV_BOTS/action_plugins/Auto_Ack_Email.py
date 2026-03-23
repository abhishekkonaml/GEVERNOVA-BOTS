from GEV_Prod_Servicenow import Change
import warnings
import re
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
#import smtplibNetwork
import smtplib
import requests
warnings.filterwarnings('ignore')
import sys
chobj=Change()

sso_extract_pattern='\d{9}'

assignment_group={'HQ CTO NETWORK ENTERPRISE SITE SUPPORT': ['@GE Vernova DT CTO Network Enterprise Site Support','Aishwarya.Shet@microland.com'],'HQ CTO NETWORK INTERNET SITE SUPPORT':['@GE Vernova DT CTO Network Internet Site Support','Aishwarya.Shet@microland.com'],'HQ CTO NETWORK DATA CENTER LAN':['@GE Vernova DT CTO Network Data Center LAN','Aishwarya.Shet@microland.com'],'HQ CTO NETWORK INTERNET EGRESS': ['@GE Vernova DT CTO Network Internet Egress','Aishwarya.Shet@microland.com'],'HQ CTO Network Firewall Support':['@GE Vernova DT CTO Network Firewall Support','Aishwarya.Shet@microland.com'],'HQ CTO NETWORK EDGE SERVICES':['@GE Vernova DT CTO Network Edge Services Devops','Aishwarya.Shet@microland.com'],'HQ CTO Network Cloud Connectivity':['@GE Vernova DT CTO Network Cloud Connectivity Devops','Aishwarya.Shet@microland.com'], 'HQ DT CTO NETWORK INTERNET EGRESS':['@GE Vernova DT CTO Network Internet Egress','Aishwarya.Shet@microland.com']}


def send_mail(ch_number,send_to,cc, assigned_to):
        
        assert isinstance(send_to, list)
        server="smtprelay.gevernova.net"
        send_from="automatedchangenotification@gevernova.com"
        subject=" {}".format(ch_number)
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Cc'] = COMMASPACE.join(cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        text='''
           Hi,
              This is to inform that the {} has been assigned to {}. The Engineer will review the requirement and get back to you at the earliest with an update on your request.
           Regards,
           Network Operations
           GE Vernova
           
           Kindly use this link to raise incidents, RITM and change. https://gevernova.service-now.com/ge_vernova_support_chat.do
           1st Level of Escalation - Tom, Amitha (560036476)
           2nd Level of Escalation - Babu, Rajesh (560036733)'''.format(ch_number,assigned_to)
        
        
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








#Created last 30 minutes

#Test query
query="sys_created_onONLast hour@javascript:gs.beginningOfLastHour()@javascript:gs.endOfLastHour()^assignment_group=306e23c52b1cee903439fb5dce91bf1f^ORassignment_group=306e23c52b1cee903439fb5dce91bf1b^ORassignment_group=497afd07fbe5ae507768f8f94eefdc1a^ORassignment_group=365f383f3346e290df8f27382e5c7bde^ORassignment_group=682dd4c5338936108ccdbf173e5c7b7e^ORassignment_group=529f15f92b7f1e10432cf2f9b891bfbe^ORassignment_group=6ea5b102fbb9e2109993f89c5eefdc4e"
#query="sys_created_onONLast hour@javascript:gs.beginningOfLastHour()@javascript:gs.endOfLastHour()^assignment_group=306e23c52b1cee903439fb5dce91bf1f^ORassignment_group=306e23c52b1cee903439fb5dce91bf1b^ORassignment_group=497afd07fbe5ae507768f8f94eefdc1a^ORassignment_group=365f383f3346e290df8f27382e5c7bde^ORassignment_group=529f15f92b7f1e10432cf2f9b891bfbe^ORassignment_group=6ea5b102fbb9e2109993f89c5eefdc4e^ORassignment_group=420aed69fb266e107768f8f94eefdc39"
print("Fetching tickets...............")
change_tickets=chobj.get_change_details_by_query(query)
print(f'change_tickets are: {change_tickets}')
if 'Failed' in change_tickets:
    sys.exit()
if len(change_tickets)>0:
   for change in change_tickets:
       ch_number=change['number']
       #Is Assigned_to null?    
       if change['assigned_to'] !='':
          assigned_to=change['assigned_to']
          assigned_to_engineer=re.findall(sso_extract_pattern,assigned_to)[0]
          ass_to=int(assigned_to_engineer)
          requested_by=change['requested_by']
          requested_by_engineer=re.findall(sso_extract_pattern,requested_by)[0]
          ass_grp=change['assignment_group'].strip()
          cc_id=assignment_group[ass_grp]

          #cc_id=['503438685@gevernova.com']
          send_to_id=[requested_by_engineer +'@gevernova.com']
          #send_to_id=['503438685@gevernova.com']
          #print(f"requestor_sso: {send_to_id}")
          #print(f"cc_id:{cc_id}")
          #print(f"assigned_to:{type(ass_to)}")
          #print(f"change_no: {type(ch_number)}")
          print(send_mail(ch_number,send_to_id,cc_id, ass_to))
          
        
        

         
       
       else:
         continue
