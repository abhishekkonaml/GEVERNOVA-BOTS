from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64
import requests
from requests.exceptions import RequestException, SSLError


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GEV_Prod_Servicenow import Incidents
import os
warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            cyber_username=task_vars["cyber_username"]
            cyber_password=task_vars["cyber_password"]
            print(cyber_username)
            print(cyber_password)
            return { 'status': 'Success','response': 'Credentials Printed' }
        except Exception as e:
            return { 'status': 'Failed', 'error': str(e) }