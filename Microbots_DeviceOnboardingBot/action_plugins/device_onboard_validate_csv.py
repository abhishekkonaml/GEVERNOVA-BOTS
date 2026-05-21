from pathlib import Path
import pandas as pd
import shutil, os
import os.path
import pprint

__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        src_type = task_vars["src_type"]
        playb_dir = task_vars["playbook_dir"]
        src_path = task_vars["src_path"]
        check_duplicates_on = self._task.args["check_duplicates_on"]
        check_missing_fields_on = self._task.args["check_missing_fields_on"]
        
        if src_type == "git":
            src_path = playb_dir + "/" + src_path

        try:
            ## Latest csv file to process
            destPath = src_path + '/Processed_CSV_Files/'
            destPath_UP = src_path + '/Unprocessed_CSV_Files/'
            print(src_path)
            print("=-=-=-"*35)
            files = Path(src_path).glob('*.csv')
            latest = max(files, key=lambda f: f.stat().st_mtime)
            deviceDataFile = str(latest)
            if (not os.path.isfile(deviceDataFile)):
                errMsg = "There are no CSV files to process"
                return dict(success=True, failed=False, changed=False, msg=errMsg)

            srcFileName = deviceDataFile.split("/")[-1]
            print(srcFileName)
            print("*"*35)
            destPathWithFile = destPath + srcFileName
            destPathWithFile_UP = destPath_UP + srcFileName
            infoMsg = 'Device data file to process: ' + deviceDataFile
            print(infoMsg)
        except Exception as e:
            errMsg = "There are no CSV files to process : {0}".format(str(e))
            return dict(success=True, failed=False, changed=False, msg=errMsg) 


        ## Read data from csv file
        try:
            df = pd.read_csv(deviceDataFile, encoding='utf-8', skipinitialspace=True)
            df = df.replace(r"^ +| +$", r"", regex=True)
            df.to_csv(deviceDataFile,index=False)

            l=[]    
            
            for elem in check_duplicates_on:
                df["lower-"+elem] = df[elem].str.lower()
                l.append("lower-"+elem)
            try:
                boolean =df.duplicated(subset=l).any()
                if (boolean):
                    df_droplog=pd.DataFrame()
                    mask=df.duplicated(subset=l, keep= 'first')
                    df_keep=df.loc[~mask]
                    for ele in l:
                        df_keep.drop(ele,inplace=True,axis='columns')
                    df_droplog = df.loc[mask]
                    for ele in l:
                        df_droplog.drop(ele,inplace=True,axis='columns')
                    print ("WARNING: data being dropped are -")
                    print (df_droplog["Hostname"])

                    df.drop_duplicates(subset=l,inplace= True)
                    for ele in l:
                        df.drop(ele,inplace=True,axis='columns')
                    infoMsg="Duplicates dropped successfully"
                    
                    df.to_csv(deviceDataFile,index=False)
                    print(infoMsg)

            except Exception as e:
                errMsg = "Error occurred while removing duplicate data : {0}".format(str(e))
                try:
                    shutil.move(deviceDataFile, destPathWithFile_UP)
                except Exception:
                    print("WARNING: Failed to move file")
                return dict(success=False, failed=True, error=errMsg)

            ## missing value in Hostname,customer_id,OS,HostGroup,Status
            try:
                d_list=check_missing_fields_on
                for detail in d_list:
                    for index in df.index:
                        bool_value = pd.isnull(df[detail][index])
                        if(bool_value == True):
                            infoMsg = "Data missing in field: {0}, at row: {1}".format(detail, index+1)
                            print(infoMsg)
                            try:
                                shutil.move(deviceDataFile, destPathWithFile_UP)
                            except Exception:
                                print("WARNING: Failed to move file")
                            return dict(success=False, failed=True, error=infoMsg)

            except Exception as e:
                errMsg = "Error occurred while determining missing data : {0}".format(str(e))
                try:
                    shutil.move(deviceDataFile, destPathWithFile_UP)
                except Exception:
                    print("WARNING: Failed to move file")
                return dict(success=False, failed=True, error=errMsg)

            out_data = {'csv_path': deviceDataFile, 'p_csv_path': destPathWithFile, 'up_csv_path': destPathWithFile_UP, 'csv_file_name': srcFileName}
            return dict(success=True, failed=False, msg="csv file is valid", out_data=out_data)

        except Exception as err:
            try:
                shutil.move(deviceDataFile, destPathWithFile_UP)
            except Exception:
                print("WARNING: Failed to move file")
            return dict(success=False, failed=True, error="Error occurred: " + str(err))
