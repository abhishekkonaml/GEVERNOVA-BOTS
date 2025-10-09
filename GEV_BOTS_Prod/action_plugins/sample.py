from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

warnings.filterwarnings("ignore") 


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           current_path="D:\\GEVernova_Ansible\\GEV_BOTS_Prod"+"\\failedcases.txt"
           print(current_path)
           with open(current_path,'w') as file:
                file.write(str({'status':'success'})+"\n")
           return {'status':'success','response':"written successfully"}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}