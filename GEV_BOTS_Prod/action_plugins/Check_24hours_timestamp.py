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
import math
from datetime import datetime, timedelta
import pytz



warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            created_date_time=self._task.args["created_timestamp"]
            ist=pytz.timezone("Asia/Kolkata")
            #convert created tme to utc
            given_dt = datetime.strptime(created_date_time.strip(), "%m-%d-%Y %I:%M:%S %p")
            given_dt=ist.localize(given_dt)
            given_dt_utc=given_dt.astimezone(pytz.UTC)
            now_dt = datetime.now(pytz.UTC)

            diff = abs(now_dt - given_dt_utc)

            if diff > timedelta(hours=23):
                decision='greater than 23'
            else:
                decision= "lesser than 23"
         
            result={ 'status': 'success', 'current_time': now_dt, 'created_time': given_dt_utc, 'difference': diff, 'output': decision}
            return result
            
        except Exception as e:
           result={'status': 'failed','Output': f'failed- {str(e)}' }
           return  result 
    def parse_dt(self, dt_str: str) -> datetime:
        # Input format: '07-11-2026 06:42:37 AM'
        return datetime.strptime(dt_str.strip(), "%d-%m-%Y %I:%M:%S %p")