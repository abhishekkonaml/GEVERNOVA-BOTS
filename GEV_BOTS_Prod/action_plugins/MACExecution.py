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
from GEV_Prod_Servicenow import Incidents
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
            #cisco_username=decoding1.decoding1('NTAxNTI5NTI4')
            #cisco_password=decoding1.decoding1('V2hpejIwMTJDMTBzZQ==')
            #cisco_username='504018887'
            #cisco_password=task_vars["cyber_password"]
            cisco_username=decoding1.decoding1('NTA0MDE4ODg3')
            cisco_password=decoding1.decoding1('QjB0czg4LVJP')
            if "gdn" not in hostname1:
               hostname=hostname1+".gdn.ge.com"
            else:
                hostname=hostname1
            ChartserverConnection = paramiko.SSHClient()
            ChartserverConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ChartserverConnection.connect(hostname=hostname, username=cisco_username,password=cisco_password,look_for_keys=False,allow_agent=False)
            stdin,stdout,stderr = ChartserverConnection.exec_command(command)
            
            output=stdout.readlines()
            out=[i for i in output if hostname not in i.lower() and 'river' not in i.lower() and 'road' not in i.lower()]
            result="".join(out)
            
            if('not known' in str(out)):
                result = 'Hostname not known'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            elif('Connection timedout' in str(out)):
                result = 'Connection timedout'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            elif(('Invalid input detected' in str(out)) and command == 'show logging'):
                result = 'Unable to execute show log command'
                result={'Hostname': hostname, 'status': 'failed','Output': result}
                return result
            

            
            #result=result.replace('\r\n',"")
            
            if result=='' or len(result)<3:
                   result1='Destination MAC not found'
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
