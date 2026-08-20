import base64
import requests
import json 
import decoding1
class AWX_Trigger:

      def trigger(self,incident):
            awx_url="https://bots.intelligeni.gevernova.net/api/v2/job_templates/22/launch/"
            proxies = {
                        "http": None,
                        "https": None,
                        }
            awx_uname=decoding1.decoding1("YWRtaW4=")
            awx_pass=decoding1.decoding1("YWRtaW4xMjM=")
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
               response = requests.request("POST", awx_url, proxies=proxies, headers=headers,json=awx_body,verify=False)
               return response.json()
            except Exception as e:
                 return str(e)