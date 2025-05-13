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


incobj=Incidents()
print(incobj.access_token)

        
