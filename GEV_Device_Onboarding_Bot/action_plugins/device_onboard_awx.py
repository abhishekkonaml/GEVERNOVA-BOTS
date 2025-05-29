import base64
import requests
import json
import pandas as pd
import time
import requests, pprint

__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        try:
            out_data=self._task.args["out_data"]
            awx_url = task_vars["awx_url"]
            awx_uname = task_vars["generic_username"]
            awx_pass = task_vars["generic_password"]
            deviceDataFile = out_data['csv_path']

            awx_creds = awx_uname + ":" + awx_pass
            awx_creds_enc = awx_creds.encode('utf-8')
            awx_auth_enc = base64.b64encode(awx_creds_enc).decode('utf-8')
            
            # Extra variables
            #  - Insert 
            inserted_AWX_data=[]
            failed_to_insert_AWX_data=[]
            AWX_total_records_to_insert = 0
            AWX_insert_success=0
            AWX_insert_failed=0
            
            # - Update
            updated_AWX_data=[]
            failed_to_update_AWX_data=[]
            AWX_total_records_to_update = 0
            AWX_update_success = 0
            AWX_update_failed = 0
 
            # Importing data from csv as json
            try:
                print("Inside importing data from csv as json")
                # device onboard path
                df = pd.read_csv(deviceDataFile,encoding='utf-8', skipinitialspace=True)
                df = df.fillna('')

                df.rename(columns = {'CustomerID':'customer_id','Hostname':'name','IPAddress':'ip_address','OS':'os','HostGroup':'group','Status':'status','InventoryID':'value','Description':'description','Tags':'tags'}, inplace = True)
                csv_device_details = json.loads(df.to_json(orient='records'))
                
                d={}
                for item in csv_device_details:
                    d.setdefault(item['value'],[]).append({"name":item["name"],"description":item["description"],"customer_id":item['customer_id'],"os":item['os'],"ip_address":item['ip_address'],"tags":item['tags']})
                
                for InventoryID,deviceData in d.items():
                        
                    # GET data from AWX
                    try:
                        url = awx_url+"inventories/"+str(InventoryID)+"/hosts/"+"?page_size=10000"
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': 'Basic ' + awx_auth_enc
                        }
                       
                        response = requests.request("GET", url, headers=headers)
                        response.raise_for_status()
                        response_json=response.json()
                        data_AWX_all=[] #list of all devices from AWX
                        
                        for i in range(0,len(response_json['results'])):
                            data_AWX_all.append({"name":response_json['results'][i]['name'],"description":response_json['results'][i]['description'],"status":response_json['results'][i]['enabled'],"id":response_json['results'][i]['id']})                                                
                        
                        elems = set((d["name"].lower()) for d in data_AWX_all)
                        
                        lst_matching_data=[]
                        lst_non_matching_data=[]
                        lst_matching_data_csv=[]
                        for e in deviceData:     
                            if((e["name"].lower()) not in elems):
                                lst_non_matching_data.append(e) #list_to_insert
                            else:
                                lst_matching_data_csv.append(e)
                        elems1 = set((d["name"].lower()) for d in deviceData)
                        
                        for e in data_AWX_all:
                            if ((e["name"].lower()) in elems1):
                                lst_matching_data.append(e)                        

                    except requests.exceptions.RequestException as errreq:
                        print("Error while fetching data from AWX")
                        return dict(success=False, failed=True, error="Error occurred while fetching data: " + str(errreq))
                    except Exception as err:
                        print("Error while fetching data from AWX")
                        return dict(success=False, failed=True, error="Error occurred while fetching data: " + str(err))

                    # Insert new devices
                    try:
                        AWX_total_records_to_insert = AWX_total_records_to_insert + len(lst_non_matching_data)

                        if len(lst_non_matching_data) == 0:
                            print("No new devices to insert")
                        else:
                            for i in range(0,len(lst_non_matching_data)):
                                try:
                                    payload = json.dumps({
                                        "name": lst_non_matching_data[i]['name'],
                                        "description": lst_non_matching_data[i]['description']
                                        })
                                    response = requests.request("POST", url, headers=headers, data=payload)
                                    response.raise_for_status()
                                    if (response.status_code == 201):
                                        AWX_insert_success= AWX_insert_success + 1
                                        inserted_AWX_data.append(lst_non_matching_data[i])
                                    else:
                                        insert_fail_response_code = response.status_code
                                        AWX_insert_failed = AWX_insert_failed + 1
                                        failed_to_insert_AWX_data.append(lst_non_matching_data[i])
                                        print("HTTP error {0} has occured on inserting devices".format(insert_fail_response_code))
                                except requests.exceptions.RequestException as errreq:
                                    print("Error occurred while inserting devices: " + str(errreq))
                                    AWX_insert_failed = AWX_insert_failed + 1
                                    failed_to_insert_AWX_data.append(lst_non_matching_data[i])
                                except Exception as err:
                                    print("Error occurred while inserting devices: " + str(err))
                                    AWX_insert_failed = AWX_insert_failed + 1
                                    failed_to_insert_AWX_data.append(lst_non_matching_data[i])

                                if i%20==0:
                                    time.sleep(5)
                                
                    except Exception as err:
                        print("Error: error occurred while inserting devices, " + str(err))

                    # Updating matching devices
                    try:
                        AWX_total_records_to_update = AWX_total_records_to_update +len(lst_matching_data_csv)
                        
                        if len(lst_matching_data_csv) == 0:
                            print("No matching devices to update")
                        else:
                            matching_data_awx_df=pd.DataFrame(lst_matching_data)
                            matching_data_awx_df['name']=matching_data_awx_df['name'].str.lower()                            
                            matching_data_awx_df.pop('description')
                            matching_data_csv_df=pd.DataFrame(lst_matching_data_csv)
                            matching_data_csv_df['OriginalName']=matching_data_csv_df['name']
                            matching_data_csv_df['name']=matching_data_csv_df['name'].str.lower()
                            matching_df=matching_data_csv_df.merge(matching_data_awx_df,on='name',how='outer')
                            matching_df.pop('name')
                            matching_df.rename(columns = {'OriginalName':'name'}, inplace = True)
                            lst_matching_data_json = json.loads(matching_df.to_json(orient='records'))                            
                            
                            for i in range(0,len(lst_matching_data_json)):
                                try:
                                    url = awx_url+"hosts/"+str(lst_matching_data_json[i]['id'])+"/"
                                    payload = json.dumps({
                                        "name": lst_matching_data_json[i]['name'],
                                        "description": lst_matching_data_json[i]['description'],
                                        "enabled": lst_matching_data_json[i]['status']
                                        })
                                    response = requests.request("PUT", url, headers=headers, data=payload)
                                    response.raise_for_status()
                                    if (response.status_code == 200):
                                        AWX_update_success = AWX_update_success + 1
                                        updated_AWX_data.append(lst_matching_data_json[i])
                                    else:
                                        update_fail_response_code = response.status_code
                                        AWX_update_failed = AWX_update_failed + 1
                                        failed_to_update_AWX_data.append(lst_matching_data_json[i])
                                        print("HTTP error {0} has occured on updating of devices".format(update_fail_response_code))
                                except requests.exceptions.RequestException as errreq:
                                    print("Error occurred while updating matching devices: " + str(errreq))
                                    AWX_update_failed = AWX_update_failed + 1
                                    failed_to_update_AWX_data.append(lst_matching_data_json[i])
                                except Exception as err:
                                    print("Error occurred while updating matching devices: " + str(err))
                                    AWX_update_failed = AWX_update_failed + 1
                                    failed_to_update_AWX_data.append(lst_matching_data_json[i])

                                if i%20==0:
                                    time.sleep(5)
                                
                    except Exception as err:
                        print("Error: error while updating matching devices, " + str(err))

                    result_awx={
                        'AWX_to_update_count': AWX_total_records_to_update,
                        'AWX_to_insert_count': AWX_total_records_to_insert,
                        'AWX_insert_success' : AWX_insert_success,
                        'AWX_insert_failed': AWX_insert_failed,
                        'AWX_update_success': AWX_update_success,
                        'AWX_update_failed': AWX_update_failed,
                        'updated_AWX_data_list': updated_AWX_data,
                        'inserted_AWX_data_list': inserted_AWX_data,
                        'failed_to_update_AWX_data': failed_to_update_AWX_data,
                        'failed_to_insert_AWX_data': failed_to_insert_AWX_data
                        }

            except Exception as err:
                print("raising error in AWX device insertion process")
                return dict(success=False, failed=True, error="Error occurred: " + str(err))

            return dict(success=True, failed=False, msg="Successful", result_awx = result_awx)

        except Exception as err:
            print("raising out side the 1st try some exception")
            return dict(success=False, failed=True, error="Error occurred: " + str(err))
