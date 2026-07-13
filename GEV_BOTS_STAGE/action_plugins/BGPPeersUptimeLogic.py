from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import warnings
import re
import paramiko
import decoding1
import sys
import time
from multiprocessing import Pool
import csv
import os
from GEV_DEV_Servicenow import Incidents
import math


incobj=Incidents()

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            hostname1=self._task.args["hostname"]
            command=self._task.args["command"]
            incidentno=self._task.args['incidentno']
            notesupdate=self._task.args['notesupdate']
            cisco_username=decoding1.decoding1('NTAxNTI5NTI4')
            cisco_password=decoding1.decoding1('V2hpejIwMTJDMTBzZQ==')
            if "gdn" not in hostname1:
               hostname=hostname1+".gdn.ge.com"
            else:
                hostname=hostname1
            ChartserverConnection = paramiko.SSHClient()
            ChartserverConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ChartserverConnection.connect(hostname=hostname, username=cisco_username,password=cisco_password,look_for_keys=False,allow_agent=False)
            channel = ChartserverConnection.invoke_shell()
            channel.send('term len 0'+'\n')
            while not channel.recv_ready():
                  time.sleep(1)
            
            out= channel.recv(math.inf) 
            channel.send(command+ '\n')
            while not channel.recv_ready():
                  time.sleep(1)
            
            out= channel.recv(math.inf)
            if('not known' in str(out.decode())):
                result = 'Hostname not known'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            elif('Authentication failed.' in str(out.decode())):
                result = 'Hostname not known'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            
            elif('Connection timedout' in str(out.decode())):
                result = 'Hostname not known'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            elif(('Invalid input detected' in str(out.decode())) and command == 'show logging'):
                result = 'Unable to execute show log command'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result

           
            if(command == 'Sh ip bgp vpnv4 vrf INSIDE Summary'):
                result=result.lower().replace('\r\n',"")
                result=result.replace('\r\n',"")
            result=result.replace('>',"")
            lines = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3}).*?\s+(\S+)\s+\d+$', result, re.MULTILINE)


            
            
            ChartserverConnection.close()
            if 'no' not in notesupdate:
               result1='''[code]<h3>{}:</h3>[/code]
                         {}'''.format(command,result)
               incobj.update_notes(incidentno,result1)
            result={'Hostname': hostname, 'status': 'success','Output':lines}
            return result
            
        except Exception as e:
           result={'Hostname': hostname, 'status': 'failed','Output': str(e)}
           return  result 





# def parse_uptime_to_minutes(time_str):
#     """Converts various BGP uptime formats (1d15h, 12:16:00, 00:35:18) into minutes."""
#     total_minutes = 0
    
#     # Handle XdYh format
#     if 'd' in time_str or 'h' in time_str:
#         days = re.search(r'(\d+)d', time_str)
#         hours = re.search(r'(\d+)h', time_str)
#         if days: total_minutes += int(days.group(1)) * 24 * 60
#         if hours: total_minutes += int(hours.group(1)) * 60
        
#     # Handle HH:MM:SS format
#     elif ':' in time_str:
#         parts = [int(p) for p in time_str.split(':')]
#         if len(parts) == 3: # HH:MM:SS
#             total_minutes += (parts[0] * 60) + parts[1] + (parts[2] / 60)
#         elif len(parts) == 2: # MM:SS
#             total_minutes += parts[0] + (parts[1] / 60)
            
#     return total_minutes