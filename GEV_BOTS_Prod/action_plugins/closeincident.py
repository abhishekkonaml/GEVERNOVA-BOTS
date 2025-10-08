from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
from GEV_Prod_Servicenow import Incidents
import math

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           incident=self._task.args["incident"]
           close_notes="Ticket For Autoclosure, Closed by Bot(504018887)"
           close_code = "Duplicate"
           incobj=Incidents()
           return {'status': 'success', 'result': incobj.close_ticket(incident,close_notes,close_code)}
        except Exception as e:
           return {'status': 'failed', 'result': str(e)}

