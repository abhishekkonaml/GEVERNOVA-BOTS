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
            neighbor_pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3})\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\S+)"
    )
            neighbours = []
            for match in neighbor_pattern.finditer(Bgppeeroutput):
                ip, uptime_str = match.groups()
                neighbours.append({
                    "neighbor": ip,
                    "uptime_str": uptime_str,
                    "uptime_to_secs": uptime_to_seconds(uptime_str)
                })
            


         
            result={ 'status': 'success', 'neighbor_lines': neighbours}
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