from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
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
            cisco_username=decoding1.decoding1('NTAxNTI5NTI4')
            cisco_password=decoding1.decoding1('V2hpejIwMTJDMTBzZQ==')
            hostname=hostname1+".gdn.ge.com"
            ChartserverConnection = paramiko.SSHClient()
            ChartserverConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ChartserverConnection.connect(hostname=hostname, username=cisco_username,password=cisco_password,look_for_keys=False,allow_agent=False)
            channel = ChartserverConnection.invoke_shell()
            channel.send('term len 0'+'\n')
            time.sleep(2)
            out= channel.recv(math.inf) 
            channel.send(command+ '\n')
            time.sleep(5)
            out= channel.recv(math.inf)
            result=str(out.decode()).replace(command,"")
            result=result.replace(hostname1,"")
            result=result.replace('>',"")
            #result=result.replace('\r\n',"")
            ChartserverConnection.close()
            incobj.update_notes(incidentno,result)
            result={'Hostname': hostname, 'status': 'success','Output':result}
            return result
            
        except Exception as e:
           result={'Hostname': hostname, 'status': 'failed','Output': str(e)}
           return  result 
