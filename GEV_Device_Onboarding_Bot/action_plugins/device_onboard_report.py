from __future__ import (absolute_import, division, print_function)
import pandas as pd
import pprint

__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        try:
            result_list=self._task.args["result_list"]
            result_awx=self._task.args["result_awx"]

            out_csv_full_path_failed= task_vars["out_csv_full_path_failed"]
            out_csv_full_path_success = task_vars["out_csv_full_path_success"]
            
            updated_AWX_data = result_awx.get('updated_AWX_data_list') or [] #success
            inserted_AWX_data = result_awx.get('inserted_AWX_data_list') or [] #success
            failed_to_update_AWX_data = result_awx.get('failed_to_update_AWX_data') or []
            failed_to_insert_AWX_data = result_awx.get('failed_to_insert_AWX_data') or []
            lst_non_matching_data = result_list.get('devices_inserted_list') or [] # success
            updated_devices =result_list.get('devices_updated_list') or [] #sucess
            failed_to_update_devices = result_list.get('failed_to_update_devices') or []
            lst_insert_fail_data = result_list.get('lst_insert_fail_data') or []
        
            # importing data from csv as json
            sucessful_onboarded_list=[]
            successful_onboard_list_db=[]
            successful_onboard_list_awx=[]
            # failed_onboard_list=[]
            failed_onboard_list_db=[]
            failed_onboard_list_awx=[]
             
            # Checking condition for successful Onboarding or update
            try:
                if(len(lst_non_matching_data) !=0 or len(updated_devices) !=0 or len(updated_AWX_data) != 0 or len(inserted_AWX_data) != 0 ):
                    if (len(lst_non_matching_data) !=0):
                        for i in range(0,len(lst_non_matching_data)):
                            successful_onboard_list_db.append({'CustomerID': lst_non_matching_data[i]['customer_id'] ,'Hostname': lst_non_matching_data[i]['key'] ,'OS':lst_non_matching_data[i]['os'] ,'IPAddress':lst_non_matching_data[i]['ip_address'],'Tags':lst_non_matching_data[i]['tags']})
                    

                    if (len(updated_devices) !=0):
                        for i in range(0,len(updated_devices)):
                            successful_onboard_list_db.append({'CustomerID': updated_devices[i]['customer_id'] ,'Hostname': updated_devices[i]['key'] ,'OS':updated_devices[i]['os'] ,'IPAddress':updated_devices[i]['ip_address'],'Tags':updated_devices[i]['tags']})
                    

                    # if (len(updated_AWX_data) != 0 ):
                    #     for i in range(0,len(updated_AWX_data)):
                    #         successful_onboard_list_awx.append({'CustomerID': updated_AWX_data[i]['customer_id'] ,'Hostname': updated_AWX_data[i]['name'] ,'OS':updated_AWX_data[i]['os'] ,'IPAddress':updated_AWX_data[i]['ip_address'],'Tags':updated_AWX_data[i]['tags']})
                    

                    if (len(inserted_AWX_data) != 0 ):
                        for i in range(0,len(inserted_AWX_data)):
                            successful_onboard_list_awx.append({'CustomerID':inserted_AWX_data[i]['customer_id'] ,"Hostname": inserted_AWX_data[i]['name'] ,"OS":inserted_AWX_data[i]['os'] ,"IPAddress":inserted_AWX_data[i]['ip_address'],'Tags':inserted_AWX_data[i]['tags']})
                    
                    # Generating CSV report for successful onboarding
                    try:
                        if(len(successful_onboard_list_awx)!=0 and len(successful_onboard_list_db)!=0):
                            successful_onboard_list_awx_df= pd.DataFrame(successful_onboard_list_awx)
                            successful_onboard_list_db_df= pd.DataFrame(successful_onboard_list_db)
                            successful_onboard_list_awx_df['IPAddress']=successful_onboard_list_awx_df['IPAddress'].fillna('None')
                            successful_onboard_list_db_df['IPAddress']=successful_onboard_list_db_df['IPAddress'].fillna('None')
                            sucessful_onboarded_list = successful_onboard_list_awx_df.merge(successful_onboard_list_db_df, on=['CustomerID','Hostname','OS','IPAddress','Tags'], how='outer')
                        elif(len(successful_onboard_list_awx)==0 and len(successful_onboard_list_db)!=0):
                            sucessful_onboarded_list = pd.DataFrame(successful_onboard_list_db)
                        else:
                            if(len(successful_onboard_list_awx)!=0 and len(successful_onboard_list_db)==0):
                                sucessful_onboarded_list = pd.DataFrame(successful_onboard_list_awx)
                        
                        sucessful_onboarded_list=sucessful_onboarded_list[['CustomerID','Hostname','OS','IPAddress','Tags']]
                        sucessful_onboarded_list.to_csv(out_csv_full_path_success,index=False)
                    
                    # Exception for generation of csv report for successful onboarding
                    except Exception as err:
                        print("Error occured in generation of csv report for successful onboarding")
                        return dict(success=False, failed=True, error="Error occurred: " + str(err))
                
                # No Successful Onboarding or update occured
                else:
                    print("No report to be generated for successful onboarding")
                 
            except Exception as err:
                print("raising error in CSV success report generation")
                return dict(success=False, failed=True, error="Error occurred: " + str(err))
            
            # Checking condition for Failed Onboarding or update
            try:
                if(len(failed_to_update_AWX_data)!=0 or len(failed_to_insert_AWX_data)!=0 or len(failed_to_update_devices)!=0 or len(lst_insert_fail_data)!=0 ):
                    
                    # if(len(failed_to_update_AWX_data)!=0):
                    #     for i in range(0,len(failed_to_update_AWX_data)):
                    #         failed_onboard_list_awx.append({'CustomerID': failed_to_update_AWX_data[i]['customer_id'] ,'Hostname': failed_to_update_AWX_data[i]['name'] ,'OS':failed_to_update_AWX_data[i]['os'] ,'IPAddress':failed_to_update_AWX_data[i]['ip_address'],'Tags':failed_to_update_AWX_data[i]['tags'],'AWX_Onboard_Status': 'Failed'})
                    
                    if(len(failed_to_insert_AWX_data)!=0):
                        for i in range(0,len(failed_to_insert_AWX_data)):
                            failed_onboard_list_awx.append({'CustomerID': failed_to_insert_AWX_data[i]['customer_id'] ,'Hostname': failed_to_insert_AWX_data[i]['name'] ,'OS':failed_to_insert_AWX_data[i]['os'] ,'IPAddress':failed_to_insert_AWX_data[i]['ip_address'],'Tags':failed_to_insert_AWX_data[i]['tags'],'AWX_Onboard_Status': 'Failed'})
                        
                    
                    if(len(failed_to_update_devices)!=0):
                        for i in range(0,len(failed_to_update_devices)):
                            failed_onboard_list_db.append({'CustomerID': failed_to_update_devices[i]['customer_id'] ,'Hostname': failed_to_update_devices[i]['name'] ,'OS':failed_to_update_devices[i]['os'] ,'IPAddress': failed_to_update_devices[i]['ip_address'],'Tags':failed_to_update_devices[i]['tags'],'DataBase_Onboard_Status': 'Failed'})
                        
                    if(len(lst_insert_fail_data)!=0):
                        for i in range(0,len(lst_insert_fail_data)):
                            failed_onboard_list_db.append_db({'CustomerID': lst_insert_fail_data[i]['customer_id'] ,'Hostname': lst_insert_fail_data[i]['name'] ,'OS':lst_insert_fail_data[i]['os'] ,'IPAddress': lst_insert_fail_data[i]['ip_address'],'Tags':lst_insert_fail_data[i]['tags'],'DataBase_Onboard_Status': 'Failed'})
                    
                    # Generating CSV report for Failed onboarding
                    try:
                        if(len(failed_onboard_list_awx)!=0 and len(failed_onboard_list_db)!=0):
                            awx_failed_df= pd.DataFrame(failed_onboard_list_awx)
                            db_failed_df= pd.DataFrame(failed_onboard_list_db)
                            df_failed_onboard = awx_failed_df.merge(df_failed_onboard, on=['CustomerID','Hostname','OS','IPAddress'], how='outer')
                            df_failed_onboard['IPAddress']=awx_failed_df['IPAddress'].fillna('None')
                            df_failed_onboard['IPAddress']=db_failed_df['IPAddress'].fillna('None')
                            df_failed_onboard['DataBase_Onboard_Status'] = df_failed_onboard['DataBase_Onboard_Status'].fillna("Passed")
                            df_failed_onboard['AWX_Onboard_Status'] = df_failed_onboard['AWX_Onboard_Status'].fillna("Passed")

                        elif(len(failed_onboard_list_awx)==0 and len(failed_onboard_list_db)!=0):
                            df_failed_onboard = pd.DataFrame(failed_onboard_list_db)
                            df_failed_onboard["AWX_Onboard_Status"] = "Passed"
                        
                        else:
                            if(len(failed_onboard_list_awx)!=0 and len(failed_onboard_list_db)==0):
                               df_failed_onboard = pd.DataFrame(failed_onboard_list_awx)
                               df_failed_onboard["DataBase_Onboard_Status"] = "Passed"
                        
                        # Failure type
                        try:
                            def Failure_type(df_failed_onboard):
                                if(df_failed_onboard["DataBase_Onboard_Status"] == "Passed" and df_failed_onboard["AWX_Onboard_Status"] == "Failed" ):
                                    return("AWX Onboarding")
                                elif(df_failed_onboard["DataBase_Onboard_Status"] == "Failed" and df_failed_onboard["AWX_Onboard_Status"] == "Passed" ):
                                    return("Database Onboarding")
                                else:
                                    return("AWX and Database Onboarding")
                            df_failed_onboard['FailureType']=df_failed_onboard.apply(lambda df_failed_onboard: Failure_type(df_failed_onboard), axis=1)

                        except Exception as err:
                            print("Error occured at determing Failure type:" +str(err))
                        
                        
                        df_failed_onboard=df_failed_onboard[['CustomerID','Hostname','IPAddress','OS','DataBase_Onboard_Status','AWX_Onboard_Status','FailureType']]
                        
                        df_failed_onboard.to_csv(out_csv_full_path_failed,index=False)
                        
                    # Exception for generation of csv report for Failed onboarding
                    except Exception as err:
                        print("Error occured2:" +str(err))
                        return dict(success=False, failed=True, error="Error occurred: " + str(err))
               
                # No Failed Onboarding or update occured
                else:
                    print("No report to be generated for failed onboarding")
                
            
            except Exception as err:
                print("raising error in CSV failure report generation")
                return dict(success=False, failed=True, error="Error occurred: " + str(err))
                    
            return dict(success=True, failed=False, msg="Successful")
        
        except Exception as err:
            print("error in CSV")
            return dict(success=False, failed=True, error="Error occurred: " + str(err))
            