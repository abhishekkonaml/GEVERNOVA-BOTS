from __future__ import (absolute_import, division, print_function)
import json
import requests
import pandas as pd
import time
import pprint
import urllib.parse

__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        
        try:
            out_data= self._task.args["out_data"]
            base_url = task_vars["base_url"]
            auth_token = task_vars["generic_token1"]
            uri = base_url + '/apis/deviceslist'
            deviceDataFile = out_data['csv_path']        

            # importing data from csv as json
            try:
                
                # device onboard path
                df = pd.read_csv(deviceDataFile,encoding='utf-8', skipinitialspace=True)
                df = df.fillna('')
                df.rename(columns = {'CustomerID':'customer_id','Hostname':'key','IPAddress':'ip_address','OS':'os','HostGroup':'group','Status':'status','InventoryID':'value','Description':'description','Tags':'tags'}, inplace = True)
                csv_device_details = json.loads(df.to_json(orient='records'))
                csv_c_id= csv_device_details[0]['customer_id']
                
            except Exception as err:
                print("raising importing data from CSV exception")
                return dict(success=False, failed=True, error="Error occurred: " + str(err))

            # API response Validation 
            try:
                csv_c_id_encoded = urllib.parse.quote(str(csv_c_id))                
                query = '?q={\"customer_id\":\"' + csv_c_id_encoded + '\"}'
                url = uri + query
                                
                payload = {'customer_id': str(csv_c_id)}
                headers = {'AuthToken': auth_token,
                        'Content-Type': 'application/json'
                        }
                response = requests.get(str(url), json=payload, headers=headers)
                response.raise_for_status()
                if response.status_code != 200:
                    return dict(success=False, failed=True, error="Failed to fetch devices, status_code: {0}".format(str(response.status_code)))
            
            except requests.exceptions.RequestException as errreq:
                return dict(success=False, failed=True, error="Error occurred while fetching devices: " + str(errreq))
            except Exception as err:
                return dict(success=False, failed=True, error="Error occurred while fetching devices: " + str(err))
            
            # Getting Mapping data from Mongodb
            try:
                mongo_device_mapping={}
                api_json=response.json()
                mapping_data_mongodb=api_json["data"]
                for details in mapping_data_mongodb:
                    details.pop("_id")
                    device_name = details["key"].lower()
                    mongo_device_mapping[device_name]=details["key"]
                
            except Exception as err:
                return dict(success=False, failed=True, error="Error occurred: " + str(err))

            # Storing matching and non-matching fields in different arrays
            try:
                Devicemapping={}
                lst_matching_data=[]
                lst_non_matching_data=[]
                count_matching_data = 0
                count_non_matching_data = 0

                elems = set((d['customer_id'].lower(), d['os'].lower(), d['key'].lower()) for d in mapping_data_mongodb if (set(['customer_id','os','key'])).issubset(d.keys()))             
                for e in csv_device_details:
                    if ((e['customer_id'].lower(), e['os'].lower(), e['key'].lower()) in  elems):
                        count_matching_data=count_matching_data+1
                        lst_matching_data.append(e)
                    else:
                        lst_non_matching_data.append(e)
                        count_non_matching_data=count_non_matching_data+1
        
            except Exception as err:
                print("raising some exception")
                return dict(success=False, failed=True, error="Error occurred: "+ str(err))
             
            # Updating matching devices
            try:                
                updated_records_count=0
                matched_records_count=0
                update_fail_count=0
                total_records_to_update = len(lst_matching_data)
                failed_to_update_devices =[]
                updated_devices=[]
                

                if (len(lst_matching_data)==0):
                    print("No matching fields to update")
                else:
                    print("About to update")
                    for i in range(0,len(lst_matching_data)):
                        try:
                            csv_device_name = lst_matching_data[i]['key'].lower()
                            mongo_device_name = mongo_device_mapping[csv_device_name]
                            url = uri+"?q={\"customer_id\": \""+lst_matching_data[i]['customer_id']+"\", \"os\": \""+lst_matching_data[i]['os']+"\", \"key\": \""+mongo_device_name+"\"}"
                            payload = json.dumps(lst_matching_data[i])
                            headers = {
                                    'AuthToken': auth_token,
                                    'Content-Type': 'application/json'
                                }                            
                            
                            response = requests.request("PUT", url, headers=headers, data=payload)
                            response.raise_for_status()
                            json_resp = response.json()                                                        
                        
                            # Checking response status code
                            if (response.status_code == 200):
                                if (json_resp['update_count']!=0):
                                    updated_devices.append({"key":lst_matching_data[i]['key'],"value":lst_matching_data[i]['value'],"description":lst_matching_data[i]['description'],"os":lst_matching_data[i]['os'],"customer_id":lst_matching_data[i]['customer_id'],"ip_address":lst_matching_data[i]['ip_address'],"tags":lst_matching_data[i]['tags']})
                                updated_records_count = updated_records_count + json_resp['update_count']
                                matched_records_count = matched_records_count + json_resp['match_count']

                            else:
                                update_fail_response_code = response.status_code
                                update_fail_count = update_fail_count + 1
                                failed_to_update_devices.append({"key":lst_matching_data[i]['key'],"value":lst_matching_data[i]['value'],"description":lst_matching_data[i]['description'],"os":lst_matching_data[i]['os'],"customer_id":lst_matching_data[i]['customer_id'],"ip_address":lst_matching_data[i]['ip_address'],"tags":lst_matching_data[i]['tags']})
                                print("HTTP error {0} has occured on updating of devices".format(update_fail_response_code))

                        except requests.exceptions.RequestException as errreq:
                            print("Error occurred while updating matching devices: " + str(errreq))
                            update_fail_count = update_fail_count + 1
                            failed_to_update_devices.append({"key":lst_matching_data[i]['key'],"value":lst_matching_data[i]['value'],"description":lst_matching_data[i]['description'],"os":lst_matching_data[i]['os'],"customer_id":lst_matching_data[i]['customer_id'],"ip_address":lst_matching_data[i]['ip_address'],"tags":lst_matching_data[i]['tags']})
                        except Exception as err:
                            print("Error occurred while updating matching devices: " + str(err))
                            update_fail_count = update_fail_count + 1
                            failed_to_update_devices.append({"key":lst_matching_data[i]['key'],"value":lst_matching_data[i]['value'],"description":lst_matching_data[i]['description'],"os":lst_matching_data[i]['os'],"customer_id":lst_matching_data[i]['customer_id'],"ip_address":lst_matching_data[i]['ip_address'],"tags":lst_matching_data[i]['tags']})

                        if i%100==0:
                            time.sleep(5)
                    
            except Exception as err:
                print("Error: error while updating matching devices, " + str(err))
                update_fail_count = update_fail_count + 1

            # Inserting non-matching devices 
            try:
                inserted_record_count = 0
                insert_fail_count = 0
                lst_insert_fail_data=[]
                total_records_to_insert = len(lst_non_matching_data)
                
                if(len(lst_non_matching_data)==0):
                    print("No new device details present to insert")
                else:
                    
                    url = uri + query
                    headers = {'AuthToken': auth_token,
                            'Content-Type': 'application/json'
                            }
                    
                    i = 0
                    while i < len(lst_non_matching_data):
                        sub_lst_non_matching_data = []
                        j = 0
                        while i<len(lst_non_matching_data) and j < 100:
                            sub_lst_non_matching_data.append(lst_non_matching_data[i])
                            j = j+1
                            i = i+1
                     
                        payload = json.dumps(sub_lst_non_matching_data)
                
                        # Checking response status code
                        response = requests.request("POST", url, headers=headers, data=payload)
                        response.raise_for_status()
                        json_resp2 = response.json()

                        if (response.status_code == 201): #201
                            inserted_record_count = inserted_record_count + json_resp2['insert_count'] 
                        else:
                            insert_fail_count = insert_fail_count + len(sub_lst_non_matching_data)
                            for i in range(0,len(sub_lst_non_matching_data)):
                                lst_insert_fail_data.append(sub_lst_non_matching_data[i])                            
                            print('HTTP error code on inserting of new device details: {O}'.format(response.status_code))
                        
            except requests.exceptions.RequestException as errreq:
                print("Error occurred while inserting devices: " + str(errreq))
                insert_fail_count = insert_fail_count + 1
                lst_insert_fail_data=lst_insert_fail_data.append(lst_non_matching_data)
            except Exception as err:
                print("Error occurred while inserting devices: " + str(err))
                insert_fail_count = insert_fail_count + 1
                lst_insert_fail_data=lst_insert_fail_data.append(lst_non_matching_data)

            result = {
                'to_update_count': total_records_to_update,
                'to_insert_count': total_records_to_insert,
                'matched_count': matched_records_count,
                'update_count': updated_records_count,
                'insert_count': inserted_record_count,
                'failed_to_insert_count': insert_fail_count,
                'failed_to_update_count': update_fail_count,
                }

            result_list ={
                    'devices_inserted_list': lst_non_matching_data,
                    'devices_updated_list': updated_devices,
                    'failed_to_update_devices': failed_to_update_devices,
                    'lst_insert_fail_data': lst_insert_fail_data
                    }

            if(insert_fail_count==0 and update_fail_count==0):
                return dict(success=True, failed=False, msg="Successful",result=result, result_list=result_list)
            else:
                # if(len(failed_to_update_devices!=0)):
                #     print("Devices failed to update are: {0}".format(failed_to_update_devices))
                return dict(success=False, failed=True, error="Unsucessful", result=result, result_list=result_list)
        except Exception as err:
            return dict(success=False, failed=True, error="Error occurred: " +str(err))
