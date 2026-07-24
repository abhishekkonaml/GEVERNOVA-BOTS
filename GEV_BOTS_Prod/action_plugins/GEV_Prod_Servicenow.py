import requests
import json
class Incidents:
    def __init__(self):
        url = "https://fssfed.ge.com/fss/as/token.oauth2?grant_type=client_credentials&scope=api"
        headers = {
          'Authorization': 'Basic c2x2TmZYYUFOV3JMUXhTbUhoUjN2ZWdKSkxUMnA1dFVNeXFXd2JBVWh6RVZCdTQ4OlJzNlpOZWo1eFFBV3hBMGJ2d2x5aGFPdERhSG9jbUVUc0kxU0hBZWtMWmx4T3FYYVlXYUJMekhaOGpsMXpRdEM=',
          
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
    def incident_creation(self,opened_by,caller_id,business_service,service_offering,assignment_group,short_description,description,urgency,work_notes,cmdb_ci):
        url1="https://api.gevernova.com/servicenow_incident/"
        
        token='Bearer {}'.format(self.access_token)
        payload = json.dumps({
                             "insert": {
                                 "partnerInfo": {
                                   "externalRecord": "",
                                   "name": "com.microland.intelligenie"
                                 },
                                 "opened_by": opened_by,
                                 "caller_id": caller_id,
                                 "business_service": business_service,
                                 "service_offering": service_offering,
                                 "assignment_group": assignment_group,
                                 "short_description": short_description,
                                 "description": description,
                                 "urgency": urgency,
                                 "work_notes": work_notes,
                                 "cmdb_ci":cmdb_ci
                             }
                            })
        headers = {
                   'Content-Type': 'application/json',
                   'Authorization': token,
                   'Cookie': 'BIGipServerpool_gevernovaqa=e50c24c05607137134b987b035fe487d; JSESSIONID=9E63CEC62D27553D912E725D31E66FBD; glide_node_id_for_js=089cab321ff39bfe74597e963c0c2334b85df218538922fe5f14561ed8de96d7; glide_session_store=0BEBC7B03BE922107BFECBC964E45A75; glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("POST", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def reassignment(self,incidentnumber,group):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "assignment_group": group
                                
                              }
                            })
        print(payload)
        print("-="*40)
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def assigned_to_bot(self,incidentnumber,jobid,update_desc):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "work_notes": "[code] <h3> The Ticket has been assigned to Intelligeni Bot - {} </h3> [/code]".format(jobid),
                                "assignment_group": "HQ CTO Network BOT",
                                "assigned_to": "504018887",
                                "state":2,
                                "short_description": update_desc
                              }
                            })
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def assigned_to_renewables_bot(self,incidentnumber,jobid,update_desc):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "work_notes": "[code] <h3> The Ticket has been assigned to Intelligeni Bot - {} </h3> [/code]".format(jobid),
                                "assigned_to": "504018887",
                                "state":2,
                                "short_description": update_desc
                              }
                            })
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def Change_to_OnHold_state(self,incidentnumber):
            token='Bearer {}'.format(self.access_token)
            url1="https://api.gevernova.com/servicenow_incident/" 
            payload = json.dumps({
                                  "update": {
                                    "partnerInfo": {
                                      "name": "com.microland.intelligenie",
                                      "externalRecord": ""
                                    },
                                    "number": incidentnumber,
                                    "state":3,
                                    "hold_reason": "Awaiting Information",
                                    "follow_up":  "2026-07-27 05:11:10"
                              
                                  }
                                })
            headers = {
                        'Content-Type': 'application/json',
                        'Authorization': token,
                        'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                      }
            try: 
                response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
                if response.status_code == 201:
                   return (response.json()['result'])
                else:
                   return ("Failed - {}".format(response.json()))
            except Exception as e:
                   return ("Failed - Something went wrong - {}".format(str(e)))
        
    def Reassign_to_renewables_Engineer(self,incidentnumber):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "work_notes": "Unable to trobleshoot, Reassigning ticket to engineer",
                                "assigned_to": "502742160",
                           
                              }
                            })
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def update_notes(self,incidentnumber,work_notes):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "work_notes": work_notes
                              }
                            })
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def update_short_desription(self,incidentnumber,updated_description):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "short_description": updated_description
                              }
                            })
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def close_ticket(self,incidentnumber,close_notes,close_code):
        token='Bearer {}'.format(self.access_token)
        url1="https://api.gevernova.com/servicenow_incident/" 
        payload = json.dumps({
                              "update": {
                                "partnerInfo": {
                                  "name": "com.microland.intelligenie",
                                  "externalRecord": ""
                                },
                                "number": incidentnumber,
                                "state" : "6",
                                
                                "close_notes" : close_notes,
                                "close_code" : close_code
                              }
                            })
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token,
                    'Cookie': 'glide_user_route=glide.ab96de1815d3b1b5951c142924425060'
                  }
        try: 
            response = requests.request("PUT", url1, headers=headers,verify=False,data=payload)
            if response.status_code == 201:
               return (response.json()['result'])
            else:
               return ("Failed - {}".format(response.json()['error']['message']))
        except Exception as e:
               return ("Failed - Something went wrong - {}".format(str(e)))
    def get_incident_details_by_incident_number(self,number):
          url1="https://api.gevernova.com/servicenow_task_cmdb/query/number={}?sso=503437104".format(number)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url1, headers=headers,verify=False)
               if response.status_code == 200:
                  return response.json()['result']
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))
    def get_parent_details_by_number(self,number):
          url1="https://api.gevernova.com/servicenow_incident/query/number={}?sso=503438685".format(number)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url1, headers=headers,verify=False)
               if response.status_code == 200:
                  return response.json()['result']
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))        
        
    def get_incident_details_by_query(self,query):
          url1="https://api.gevernova.com/servicenow_incident/query/{}?sso=503437104".format(query)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url1, headers=headers,verify=False)
               if response.status_code == 200:
                  return response.json()['result']
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))

class CMDB:
      def __init__(self):
        url = "https://fssfed.ge.com/fss/as/token.oauth2?grant_type=client_credentials&scope=api"
        headers = {
          'Authorization': 'Basic c2x2TmZYYUFOV3JMUXhTbUhoUjN2ZWdKSkxUMnA1dFVNeXFXd2JBVWh6RVZCdTQ4OlJzNlpOZWo1eFFBV3hBMGJ2d2x5aGFPdERhSG9jbUVUc0kxU0hBZWtMWmx4T3FYYVlXYUJMekhaOGpsMXpRdEM=',
          
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
      def get_ci_details(self,hostname):
          url="https://api.gevernova.com/servicenow_task_cmdb/name/{}".format(hostname)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url, headers=headers,verify=False)
               if response.status_code == 200:
                  return (response.json()['result'])
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))
      def get_ci_details_by_id(self,id):
          url="https://api.gevernova.com/servicenow_task_cmdb/id/{}".format(id)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url, headers=headers,verify=False)
               if response.status_code == 200:
                  return (response.json()['result'])
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))
      def get_ci_full_details(self,hostname):
          url="https://api.gevernova.com/servicenow_task_cmdb/full/{}".format(hostname)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url, headers=headers,verify=False)
               if response.status_code == 200:
                  return (response.json()['result'])
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))
      def get_ci_by_query(self,query):
          url="https://api.gevernova.com/servicenow_task_cmdb/custom_query?{}".format(query)
          token='Bearer {}'.format(self.access_token)
          headers = {
               'Authorization': token,
               'tradingPartner': 'com.microland.intelligenie',
               'Content-Type': 'application/json'
              }
          try: 
               response = requests.request("GET", url, headers=headers,verify=False)
               if response.status_code == 200:
                  return (response.json()['result'])
               else:
                  return ("Failed - {}".format(response.json()['error']['message']))
          except Exception as e:
                  return ("Failed - Something went wrong - {}".format(str(e)))


