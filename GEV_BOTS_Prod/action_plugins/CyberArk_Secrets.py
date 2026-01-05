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
    def fetch_secrets_from_url(self,base_url,endpoint_path,params,certs,certs_key):
        url = f"https://{base_url}{endpoint_path}"
        try:
           headers = { "Content-Type": "application/json" }
           proxies={ "http": '', "https": '' }
           print(f"Trying: {url}")
           with open('sample.crt','w') as f:
                f.write(certs)
           with open('sample.key','w') as f:
                f.write(certs_key)
           response = requests.get(url, params=params, headers=headers, cert=('sample.cert','sample.key'), timeout=10,proxies=proxies)
           response.raise_for_status()
           os.remove('sample.cert')
           os.remove('sample.key')
           return response.json()
        except (RequestException, SSLError) as e:
           print(f"Failed to connect to {base_url}: {e}")
           return None
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
            
            # Target API path
            endpoint_path = "/AIMWebService/api/Accounts"
            params = { "AppID": app_id, "Safe": safe,"username": username }
            
            secrets = self.fetch_secrets_from_url(ccp1_url,endpoint_path,params,certs,certs_key)
            if not secrets:
                secrets = self.fetch_secrets_from_url(ccp2_url,endpoint_path,params,certs,certs_key)
            if secrets:
               user = secrets.get("UserName")
               pswd = secrets.get("Content")
               print("-----------------------------------------------------------------------------")
               print(f"Account Information from CyberArk:\nUsername = {user}\nPassword = {pswd}")
               print("-----------------------------------------------------------------------------")
            else:
                print("Failed to retrieve secrets from both endpoints.")

            












            
            return {'status': 'success', 'result': 'Parameters fetched successfully'}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}