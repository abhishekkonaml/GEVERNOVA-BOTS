from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
import warnings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from GEV_Prod_Servicenow import CMDB
import math

warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           hostname=self._task.args["hostname"]
           cmdbobj=CMDB()
           
           try: 
               find_wlc_name=cmdbobj.get_ci_full_details(hostname)[0]['Relationships']
               if len(find_wlc_name)>0:
                  return {'status': 'success', 'result': find_wlc_name[0]['child'] }
               else:
                  return {'status': 'failed', 'result': 'Unable to fetch the WLC' }
           except Exception as e:
                 return {'status': 'failed', 'result': "Failed - Error in fetching the WLC - {}".format(str(e)) }
           
                 
        except Exception as e:
            return { 'status': 'failed', 'result': str(e) }