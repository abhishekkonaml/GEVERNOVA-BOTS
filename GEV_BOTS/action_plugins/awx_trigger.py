import base64
import requests
import json
class AWX_Trigger:

      def trigger(self,awx_url,awx_uname,awx_pass,incident):
           
            awx_creds = awx_uname + ":" + awx_pass
            awx_creds_enc = awx_creds.encode('utf-8')
           
            awx_auth_enc = base64.b64encode(awx_creds_enc).decode('utf-8')
            headers = {
                            'Content-Type': 'application/json',
                            'Authorization': 'Basic ' + awx_auth_enc
                        }
            awx_body={
                      "extra_vars": {
                               "incident_no": incident
                             }
                      }

            try:           
               response = requests.request("GET", awx_url, headers=headers,json=json.dumps(awx_body))
               return response.json()
            except Exception as e:
                 return str(e)