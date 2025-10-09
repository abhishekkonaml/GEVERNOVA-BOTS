import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

current_path=os.getcwd()+"\\failedcases.txt"

with open(current_path,'w') as file:
    file.write(str({'status':'success'})+"\n")