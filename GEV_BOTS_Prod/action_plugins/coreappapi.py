import requests
import json

class CoreApp:
    def coreapp_trigger(self,ticketNo,desc,org_assignment_group):
        url = "https://bots.intelligeni.gevernova.net/bots/apis/resolve"
        proxies={
          'http_proxy' : None,
          'https_proxy' : None
        }
        payload = json.dumps({
          "ticket": {
            "source": "servicenow-prod",
            "customer_id": "ge_vernova",
            "ticket_type": "incident",
            "ticketNo": ticketNo,
            "description": desc,
            "priorityName": "P3",
            "deviceName": "",
            "application_owner": org_assignment_group.split("\n\n")[0]
          }
        })
        print("===="*10)
        print(payload)
        print("===="*10)
        headers = {
          'Content-Type': 'application/json',
          'AuthToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODM5NzkyZTJkODIzOTVjYWFkZGRlNzkiLCJlbWFpbCI6ImlnYm90c2FwaXNhZG1pbkBnZXZlcm5vdmEuY29tIiwidGVuYW50IjoiZ2VfdmVybm92YSIsImlhdCI6MTc1NTUyMTI3OCwiZXhwIjoxNzg3MDU3Mjc4fQ.DGIGAMkcAYpxWBe9R-kmZPiZGgI2zH4vyn8iyN8aHAE'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload,verify=False,proxies=proxies)
            print("----------------------------",response.status_code,"-----------------------------")
            if response.status_code==201:
               return response.json()
            else:
                print(response.json())
        except Exception as e:
                print("=-=-=-=-=-=-=-=-=-=-=")
                print(str(e))
                return str(e)
    
