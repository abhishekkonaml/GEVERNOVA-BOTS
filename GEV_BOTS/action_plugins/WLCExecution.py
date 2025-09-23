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
            cisco_username=decoding1.decoding1('NTAyODI4MTkw')
            cisco_password=decoding1.decoding1('Q0JiekBIN1gxdlBCbXo=')
            if "gdn" not in hostname1:
               hostname=hostname1+".gdn.ge.com"
            else:
                hostname=hostname1
            ChartserverConnection = paramiko.SSHClient()
            ChartserverConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ChartserverConnection.connect(hostname=hostname, username=cisco_username,password=cisco_password,look_for_keys=False,allow_agent=False)
            channel = ChartserverConnection.invoke_shell()
            channel.send(cisco_username+"\n")
            time.sleep(3)
            channel.send(cisco_password+"\n")
            time.sleep(3)
            
            out= channel.recv(math.inf) 
            time.sleep(3)
            channel.send(command+ '\n')
            
            while not channel.recv_ready():
                  time.sleep(1)
            channel.send("\n")
            time.sleep(3)
            channel.send("\n")
            time.sleep(3)
            channel.send("\n")
            time.sleep(3)
            out= channel.recv(math.inf)
            
            if('not known' in str(out.decode())):
                result = 'Hostname not known'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            elif('Connection timedout' in str(out.decode())):
                result = 'Connection timedout'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            elif(('Invalid input detected' in str(out.decode())) and command == 'show logging'):
                result = 'Unable to execute show log command'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            

            result=str(out.decode()).replace(command,"")
            result=result.lower().replace(hostname1.lower(),"")
            result=result.replace('>',"")
            #result=result.replace('\r\n',"")
            ChartserverConnection.close()
            if result=='' or len(result)<3:
                   result1='No Logs found'
            else:
                   result1=result
            if 'no' not in notesupdate:
               
               result2='''[code]<h3>{}:</h3>[/code]
                         {}'''.format(command,result1)
               
               incobj.update_notes(incidentno,result2)
            result={'Hostname': hostname, 'status': 'success','Output':result1}
            return result
            
        except Exception as e:
           result={'Hostname': hostname, 'status': 'failed','Output': str(e)}
           return  result 
