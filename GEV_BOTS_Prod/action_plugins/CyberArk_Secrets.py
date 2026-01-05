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

warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            app_id=task_vars["app_id"]
            safe=task_vars["safe"]
            username=task_vars["username"]
            ccp1_url=task_vars["ccp1_url"]
            ccp2_url=task_vars["ccp2_url"]
            certs=task_vars['certs']
            certs_key=task_vars['certs_key']
            print(app_id,safe,username,ccp1_url,ccp2_url,certs,certs_key)
            return {'status': 'success', 'result': 'Parameters fetched successfully'}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}