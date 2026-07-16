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
            Bgppeeroutput=self._task.args["output"]
            neighbor_lines = re.findall(
        r'^\s*(\d+\.\d+\.\d+\.\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\S+)\s+\d+',
        Bgppeeroutput,
        flags=re.MULTILINE
    )

            if not neighbor_lines:
                result="No neighbor"

            uptimes = {}
            
            for neighbor_ip, updown in neighbor_lines:
                # Sometimes token could be '-' or 'never'; handle that if needed
                if updown in ('-', ''):
                    seconds_up = 0
                else:
                    seconds_up = uptime_to_seconds(updown)
                uptimes[neighbor_ip] = seconds_up

            # Print uptimes (optional)
            for ip, sec in uptimes.items():
                print(f"{ip} uptime_seconds={sec}")
            threshold_seconds = 2 * 3600  # 2 hours
            any_below_threshold = any(sec < threshold_seconds for sec in uptimes.values())

            if any_below_threshold:
                print("reassign")
                result="reassign"
            else:
                print("close")
                result="close"

         
            result={ 'status': 'success','Output':result, 'neighbor_lines': neighbor_lines}
            return result
            
        except Exception as e:
           result={'status': 'failed','Output': str(e)}
           return  result 



def uptime_to_seconds(uptime_str: str) -> int:
    """
    Converts uptime like '4d17h' or '2h' into seconds.
    Supports d/h/m/s combinations if present.
    """
    uptime_str = uptime_str.strip()

    # e.g. 4d17h, 1d19h, 90m, 120s, 2h30m, etc.
    pattern = r'(?:(\d+)\s*d)?\s*(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?'
    m = re.fullmatch(pattern, uptime_str)
    if not m:
        # Sometimes uptime can be like '00:10:23' depending on platform; handle minimally
        # You can extend this if needed.
        raise ValueError(f"Unrecognized uptime format: {uptime_str}")

    days = int(m.group(1) or 0)
    hours = int(m.group(2) or 0)
    minutes = int(m.group(3) or 0)
    seconds = int(m.group(4) or 0)
    return days * 86400 + hours * 3600 + minutes * 60 + seconds