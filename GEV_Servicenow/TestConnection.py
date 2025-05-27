import paramiko
import decoding1
import sys
import time
hostname=sys.argv[1]


try:
    cisco_username=decoding1.decoding1('NTAxNTI5NTI4')
    cisco_password=decoding1.decoding1('V2hpejIwMTJDMTBzZQ==')

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
except Exception as e:
    ChartserverConnection.close()
    print("Failed - Error! - {}".format(str(e)))
