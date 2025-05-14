import requests

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
print(incobj.get_incident_details_by_query(query2))


        
