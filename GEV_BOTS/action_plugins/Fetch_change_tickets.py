from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import warnings
from GEV_Stage_Servicenow import Incidents
from datetime import datetime
import pytz
incobj=Incidents()
warnings.filterwarnings("ignore")

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
            query1="short_descriptionLIKEdevice silencing^start_date>=javascript:gs.beginningOfCurrentMinute()/change_request"

            incobj=Incidents()
            fetch_changed_tickets=incobj.get_change_details_by_query(query1)
            
            ch_list=[]
            for change_ticket in fetch_changed_tickets:
                Number=change_ticket['number']
                ch_list.append(Number)
            if(len(ch_list) == 0):
                result='No device silencing tickets'
            else:
                result=ch_list
                
                
                #try:
                #    current_est_time = datetime.now(est_timezone)
                #    tickettime=datetime.strptime(openedAt,"%m-%d-%Y %I:%M:%S %p")
                #    esttime=datetime.strftime(current_est_time,"%m-%d-%Y %I:%M:%S %p")
                #    est_time_now=datetime.strptime(esttime,"%m-%d-%Y %I:%M:%S %p")
                #    time_difference=(est_time_now-tickettime).total_seconds()
                #    if time_difference>3600: 
                #        #print(Number,group)
                #        #print("=-=-"*25)
                #        print(Number,time_difference)
                #        print(incobj.reassignment(Number,group))
                #except Exception as e:
                #       pass
            return {'status': 'success', 'response': result}
        except Exception as e:
            return {'status': 'failed','response':str(e)}