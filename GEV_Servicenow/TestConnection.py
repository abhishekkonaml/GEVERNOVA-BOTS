import paramiko
import decoding1
import sys
import time
import pandas as pd
from multiprocessing import Pool
import csv
df=pd.read_csv('hostnames.csv')
hostnames=df['Hostname'].to_list()[0:10]



def test_connection(hostname):
    try:
        cisco_username=decoding1.decoding1('NTAxNTI5NTI4')
        cisco_password=decoding1.decoding1('V2hpejIwMTJDMTBzZQ==')
        hostname=hostname+".gdn.ge.com"
        ChartserverConnection = paramiko.SSHClient()
        ChartserverConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ChartserverConnection.connect(hostname=hostname, username=cisco_username,password=cisco_password)
        channel = ChartserverConnection.invoke_shell()
        out= channel.recv(10000000000000000) 
        command="show clock"  
        channel.send(command+ '\n')
        time.sleep(5)
        out= channel.recv(10000000000000000)
        result=str(out.decode()).replace(command,"")
        
        ChartserverConnection.close()
        print(result)
        result57={'Hostname': hostname, 'Result': 'Success'}
    
            
        with open("Outcome.csv", "a", newline="") as f:
             w = csv.DictWriter(f, result57.keys())
             w.writerow(result57)
    except Exception as e:
        ChartserverConnection.close()
        print("Failed - Error! - {}".format(str(e)))
        result57={'Hostname': hostname, 'Result': 'Failed'}
        with open("Outcome.csv", "a", newline="") as f:
             w = csv.DictWriter(f, result57.keys())
             w.writerow(result57)


import csv

my_dict = {'Hostname': '','Result': ''}

with open("Outcome.csv", "w", newline="") as f:
    w = csv.DictWriter(f, my_dict.keys())
    w.writeheader()
    w.writerow(my_dict)


def pool_handler():
    p = Pool(10)
    p.map(test_connection, hostnames)
    
pool_handler()

