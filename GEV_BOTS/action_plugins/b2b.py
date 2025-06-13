import requests
import json
class GrabIncidents:
    def __init__(self):
        url = "https://fssfed.stage.ge.com/fss/as/token.oauth2?grant_type=client_credentials&scope=api"
        headers = {
          'Authorization': 'Basic aUZJZHlkNTNnWFhKVzNPZGF1ODJGWVVIbmFaVDYzSWo2WHR4MktCbEFxZ09lWkdMOnhHa25uVllCRG1LMmFRRk16YndVb1FmbGhreXR2UkVKT203QkZpUldBUFh2THlxS3g5N2F1N0IzUlhTSTZhaG0=',
          
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cookie': 'PF=g4icCfGqJDOJT2NT4Q6JA5'

        }
        
        try: 
           response = requests.request("POST", url, headers=headers, verify=False)
           if response.status_code == 200:
              self.access_token=response.json()["access_token"]
           else: 
              self.access_token="Failed to fetch the access token"
        except Exception as e:
              self.access_token="Failed to fetch the access token-{}".format(str(e))
    
    def getincidents(self):
        if "Failed" in self.access_token:
            return self.access_token
        url = "https://dev.api.gevernova.com/servicenow_task_cmdb/b2b/100?debug=1"
        token='Bearer {}'.format(self.access_token)
        headers = {
                    'tradingPartner': 'com.microland.intelligenie',
                    'Authorization': token,
                    'Cookie': 'BIGipServerpool_gevernovadev=322e8be49f365b847e52f223036da18e; BIGipServerpool_gevernovaqa=c7410877879604bb52a141b075310f46; JSESSIONID=79B4109889D4B3DEC13CCDEC7F39A9F3; glide_node_id_for_js=787fbcb29b8f37362baf4f4b36be092c7eded2081e38792a74de0e120ad98d38; glide_session_store=1604DAAAFB8A66D087F9FB1F5EEFDC88; glide_user_activity=U0N2M18xOlkxU0F3L0pRR3FpUHdjMlFSVWVKUHIzeTIxaWo4QTlkV0E2Y0ZHZmI2b1k9OnAwalhySmM0K2xaZEEzOVV1NFpIUHFKRVAzZ1BIYlZNZ3psRWIzc1c4UEU9; glide_user_route=glide.1294f0008eaa1e78ad2c4b80f68ce42c'
                  }
        try: 
            response = requests.request("GET", url, headers=headers,verify=False)
            if response.status_code == 200:
                return (response.json()['result'])
            else:
                return ("Failed - {}".format(response.json()['error']['message']))
        except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))
        



