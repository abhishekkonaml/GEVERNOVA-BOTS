import requests
import json

class CoreApp:
    def coreapp_trigger(self,ticketNo,desc):
        url = "https://bots.intelligeni.gevernova.net/bots/apis/resolve"
        
        payload = json.dumps({
          "ticket": {
            "source": "servicenow-prod",
            "customer_id": "ge_vernova",
            "ticket_type": "incident",
            "ticketNo": ticketNo,
            "description": desc,
            "priorityName": "P3",
            "deviceName": "",
            "application_owner": "HQ CTO Network Enterprise Site Support"
          }
        })
        headers = {
          'Content-Type': 'application/json',
          'AuthToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2ODM5NzkyZTJkODIzOTVjYWFkZGRlNzkiLCJlbWFpbCI6ImlnYm90c2FwaXNhZG1pbkBnZXZlcm5vdmEuY29tIiwidGVuYW50IjoiZ2VfdmVybm92YSIsImlhdCI6MTc1NTUyMTI3OCwiZXhwIjoxNzg3MDU3Mjc4fQ.DGIGAMkcAYpxWBe9R-kmZPiZGgI2zH4vyn8iyN8aHAE'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code==201:
               return response.json()
            else:
                return response.json()
        except Exception as e:
                return str(e)
    
