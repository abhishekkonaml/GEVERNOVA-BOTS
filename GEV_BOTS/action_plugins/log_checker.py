from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re
from datetime import datetime 
import warnings
warnings.filterwarnings("ignore")
class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try:
           systemlogs=self._task.args["log_results"]
           sh_clock_timestamp=self._task.args['clock_results']
           timeextractpatternfromlogs="\w+  \d+ \d+:\d+:\d+|\w+ \d+ \d+:\d+:\d+"
           timepatternforclock="[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]"
           timepatternfordate="\w+ \d+"
           logs_timestamp=re.findall(timeextractpatternfromlogs,systemlogs)[0]
           sh_clock_timestamp2=re.findall(timepatternforclock,sh_clock_timestamp)[0]
           sh_clock_timestamp1=re.findall(timepatternfordate,sh_clock_timestamp)[0]
           sh_clock_timestamp=sh_clock_timestamp1+" "+sh_clock_timestamp2
   
           
           
           sh_time1=datetime.strptime(sh_clock_timestamp,"%b %d %H:%M:%S")
           log_time1=datetime.strptime(logs_timestamp,"%b %d %H:%M:%S")
           time_difference=(sh_time1-log_time1).total_seconds()
           
           if time_difference<1800:
               
               result="Critical - Time Difference {} - show clock: {} && logstime: {}".format(time_difference,sh_time1,log_time1)

               return {'status': 'failed','output':result}
           else:
               result="Success - Time Difference {} - show clock: {} && logstime: {}".format(time_difference,sh_time1,log_time1)
               return {'status': 'success','output':result}
        except Exception as e:
           result="Error - Logs Validation Failed - {}".format(str(e))
           return {'status': 'failed','output':result}