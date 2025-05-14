import requests
import json
class Incidents:
    def __init__(self):
        url = "https://fssfed.stage.ge.com/fss/as/token.oauth2?grant_type=client_credentials&scope=api"
        headers = {
          'Authorization': 'Basic ckdnMVd4V280Rko2SnpZZ2lUY3VnU1pqVzEzdmk1UVBjYnZjTnUxTUF0ZkZRM0xBOjA5enR1UUk4NlZMcVV5TEFOYW5taERuNGRaQXc1UTlYeENkSE5Pb0FpcTAxd0lOTU5JMTdDZFVibXMwRzRNMXQ=',
          
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cookie': 'PF=AvKeI0z1JjyimQVUejoyav'

        }
        
        try: 
           response = requests.request("POST", url, headers=headers, verify=False)
           if response.status_code == 200:
              self.access_token=response.json()["access_token"]
           else: 
              self.access_token="Failed to fetch the access token"
        except Exception as e:
              self.access_token="Failed to fetch the access token-{}".format(str(e))
    def incident_creation(self,opened_by,caller_id,business_service,service_offering,assignment_group,short_description,description,urgency,work_notes):
        url1="https://stage.api.gevernova.com/servicenow_incident/"
        payload = json.dumps({
                             "insert": {
                                 "partnerInfo": {
                                   "externalRecord": "",
                                   "name": "com.gevn.servicenow"
                                 },
                                 "opened_by": opened_by,
                                 "caller_id": caller_id,
                                 "business_service": business_service,
                                 "service_offering": service_offering,
                                 "assignment_group": assignment_group,
                                 "short_description": short_description,
                                 "description": description,
                                 "urgency": urgency,
                                 "work_notes": work_notes
                             }
                            })
    def get_incident_details_by_query(self,query):
          url1="https://stage.api.gevernova.com/servicenow_incident/query/{}".format(query)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.microwhiz',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url1, headers=headers,verify=False)
               if response.status_code == 200:
                  return (response.json()['result'])
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))



incobj=Incidents()
query1="number={}?sso={}".format("GEVINC0016024","503437104")
query2="active=true^assignment_groupGE Vernova DT CTO Network?sso={}".format("503437104")

opened_by="503437104"
caller_id="503437104"
business_service="Monitoring"
service_offering="Network monitoring"
assignment_group="GE Vernova DT CTO Network"
short_description="This is a test Please Ignore"
description="This is only a test"
urgency="3"
work_notes="This is a test. This is only a test."
print(incobj.get_incident_details_by_query(query2))


        
