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
from datetime import datetime, timedelta


incobj=Incidents()

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            created_date_time=self._task.args["created_timestamp"]
            given_dt = self.parse_dt(created_date_time)
            now_dt = datetime.now()

            diff = abs(now_dt - given_dt)

            if diff > timedelta(hours=23):
                decision='greater than 23'
            else:
                decision= "lesser than 23"
         
            result={ 'status': 'success', 'current_time': now_dt, 'created_time': created_date_time, 'difference': diff, 'output': decision}
            return result
            
        except Exception as e:
           result={'status': 'failed','Output': f'failed- {str(e)}' }
           return  result 
