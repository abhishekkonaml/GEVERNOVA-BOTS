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
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from GEV_DEV_Servicenow import Incidents
import math

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           ch_number=self._task.args["change_number"]
           work_notes=self._task.args["work_notes"]
           incobj=Incidents()
           return {'status': 'success', 'result': incobj.update_notes_change(ch_number,work_notes)}
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}

