from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
import warnings
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

warnings.filterwarnings("ignore") 




class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        try: 
           analysis_output=self._task.args['result1']
           status_alert_table_body=''
           down_alert_table_body=''
           for key in analysis_output['StatusAlert']['tickets']:
               status_alert_table_body+='''
               <tr>
                     <td> {} </td>
                     <td> {} </td>
                     <td> {} </td>
                     <td> {} </td>
               </tr>
               
               '''.format(key['Number'],key['Summary'].replace("h3","h6").replace("[code]","").replace("[/code]",""),key['Status'].replace("h3","h6").replace("[code]","").replace("[/code]",""),key['OpenedAt'])
           for key in analysis_output['IdleIntervalAlert']['tickets']:
               down_alert_table_body+='''
               <tr>
                     <td> {} </td>
                     <td> {} </td>
                     <td> {} </td>
                     <td> {} </td>
               </tr>
               
               '''.format(key['Number'],key['Summary'].replace("h3","h6").replace("[code]","").replace("[/code]",""),key['Status'].replace("h3","h6").replace("[code]","").replace("[/code]",""),key['OpenedAt'])
           
           
           template='''
             <!DOCTYPE html>
             <html lang="en">
             <head>
               <meta charset="UTF-8">
               <title>GEV BOT DAILY REPORT</title>
             
               <!-- Bootstrap CSS -->
               <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
                     rel="stylesheet" crossorigin="anonymous">
             
               <!-- DataTables CSS -->
               <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
             
               <!-- jQuery -->
               <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
             
               <!-- Bootstrap JS -->
               <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
                     crossorigin="anonymous"></script>
             
               <!-- DataTables JS -->
               <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
             
               <style>
                 body {
                   background-color: #F5F5F5;
                 }
                 .table-container {
                   max-width: 80%;
                   margin: 0 auto;
                 }
                 .table {
                   background-color: white;
                 }
                 thead, tbody {
                   font-family: Arial, Helvetica, sans-serif;
                   font-size: 13px;
                 }
                 .nav-tabs .nav-link.active {
                   background-color: #008080 !important;
                   color: white !important;
                 }
                 .nav-tabs .nav-link {
                   color: #008080;
                 }
                 .dataTables_filter, .dataTables_length {
                   display: none !important; /* Hide global search and entry count */
                 }
                 .dataTables_info, .dataTables_paginate {
                   font-size: 12px;
                 }
                 th input {
                   width: 100%;
                   box-sizing: border-box;
                   font-size: 12px;
                   padding: 2px;
                 }
               </style>
             </head>
             
             <body>
               <h1 style="color:white;text-align:center;background-color:#008080;padding:10px;">
                 GEV BOT DAILY REPORT - 12-10-2025
               </h1>
               
               
               <!-- STYLE 1 -->
             <div class="container my-4">
               <h5 class="text-center fw-bold" style="color:#008080;">BOT PERFORMANCE SUMMARY</h5>
               <div class="row justify-content-center mt-3">
                 <div class="col-md-2 col-6 mb-3">
                   <div class="card shadow-sm text-center" style="border:none;border-radius:12px;background:linear-gradient(135deg,#E0F7F7,#ffffff);">
                     <div class="card-body py-3">
                       <div class="fs-6 text-uppercase fw-bold" style="color:#008080;">Touched</div>
                       <div class="fs-3 fw-bold"> <bot_touched_count> </div>
                     </div>
                   </div>
                 </div>
                 <div class="col-md-2 col-6 mb-3">
                   <div class="card shadow-sm text-center" style="border:none;border-radius:12px;background:linear-gradient(135deg,#FFF3E0,#ffffff);">
                     <div class="card-body py-3">
                       <div class="fs-6 text-uppercase fw-bold" style="color:#E67E22;">Missed</div>
                       <div class="fs-3 fw-bold"> <bot_not_touched_count> </div>
                     </div>
                   </div>
                 </div>
                 <div class="col-md-2 col-6 mb-3">
                   <div class="card shadow-sm text-center" style="border:none;border-radius:12px;background:linear-gradient(135deg,#E8F5E9,#ffffff);">
                     <div class="card-body py-3">
                       <div class="fs-6 text-uppercase fw-bold" style="color:#27AE60;">Closed</div>
                       <div class="fs-3 fw-bold"> <closed>  </div>
                     </div>
                   </div>
                 </div>
                 <div class="col-md-2 col-6 mb-3">
                   <div class="card shadow-sm text-center" style="border:none;border-radius:12px;background:linear-gradient(135deg,#E3F2FD,#ffffff);">
                     <div class="card-body py-3">
                       <div class="fs-6 text-uppercase fw-bold" style="color:#2980B9;">Efficiency</div>
                       <div class="fs-3 fw-bold"> <efficiency> </div>
                     </div>
                   </div>
                 </div>
               </div>
             </div>
               
               
               
               
               
               
               
             
               <div class="container-fluid">
             
                 <!-- Tabs -->
                 <ul class="nav nav-tabs" id="botTabs" role="tablist">
                   <li class="nav-item" role="presentation">
                     <button class="nav-link active" id="status-tab" data-bs-toggle="tab"
                             data-bs-target="#status" type="button" role="tab">Status Alert</button>
                   </li>
                   <li class="nav-item" role="presentation">
                     <button class="nav-link" id="idle-tab" data-bs-toggle="tab"
                             data-bs-target="#idle" type="button" role="tab">Idle Interval</button>
                   </li>
                 </ul>
             
                 <div class="tab-content" id="botTabsContent">
             
                   <!-- Status Alert Tab -->
                   <div class="tab-pane fade show active" id="status" role="tabpanel">
             
                     <!-- Cards inside tab -->
                     <div class="row mt-4 mb-2 justify-content-center">
                       <div class="col-xl-2 col-md-6 mb-4">
                         <div class="card shadow h-100 py-2">
                           <div class="card-body text-center">
                             <div class="text-xs font-weight-bold text-uppercase mb-1" style="color:#008080;"><b>Touched</b></div>
                             <div class="h5 mb-0 font-weight-bold text-gray-800"> <status_alert_touched_data> </div>
                           </div>
                         </div>
                       </div>
                       <div class="col-xl-2 col-md-6 mb-4">
                         <div class="card shadow h-100 py-2">
                           <div class="card-body text-center">
                             <div class="text-xs font-weight-bold text-uppercase mb-1" style="color:#008080;"><b>Not Touched</b></div>
                             <div class="h5 mb-0 font-weight-bold text-gray-800"> <status_alert_not_touched_data> </div>
                           </div>
                         </div>
                       </div>
                       <div class="col-xl-2 col-md-6 mb-4">
                         <div class="card shadow h-100 py-2">
                           <div class="card-body text-center">
                             <div class="text-xs font-weight-bold text-uppercase mb-1" style="color:#008080;"><b>Closed</b></div>
                             <div class="h5 mb-0 font-weight-bold text-gray-800"> <status_alert_closed_data> </div>
                           </div>
                         </div>
                       </div>
                     </div>
             
                     <!-- Table -->
                     <div class="table-container mt-4">
                       <table class="table table-bordered datatable">
                         <thead class="table-light">
                           <tr>
                             <th>Ticket No</th>
                             <th>Summary</th>
                             <th>Status</th>
                             <th>OpenedAt</th>
                           </tr>
                           <tr>
                             <th><input type="text" placeholder="Search Ticket No"></th>
                             <th><input type="text" placeholder="Search Summary"></th>
                             <th><input type="text" placeholder="Search Status"></th>
                             <th><input type="text" placeholder="Search OpenedAt"></th>
                           </tr>
                         </thead>
                         <tbody>
                           <status_alert_table_body>
                         </tbody>
                       </table>
                     </div>
                   </div>
             
                   <!-- Idle Interval Tab -->
                   <div class="tab-pane fade" id="idle" role="tabpanel">
             
                     <!-- Cards inside tab -->
                     <div class="row mt-4 mb-2 justify-content-center">
                       <div class="col-xl-2 col-md-6 mb-4">
                         <div class="card shadow h-100 py-2">
                           <div class="card-body text-center">
                             <div class="text-xs font-weight-bold text-uppercase mb-1" style="color:#008080;"><b>Touched</b></div>
                             <div class="h5 mb-0 font-weight-bold text-gray-800"> <down_touched_data> </div>
                           </div>
                         </div>
                       </div>
                       <div class="col-xl-2 col-md-6 mb-4">
                         <div class="card shadow h-100 py-2">
                           <div class="card-body text-center">
                             <div class="text-xs font-weight-bold text-uppercase mb-1" style="color:#008080;"><b>Not Touched</b></div>
                             <div class="h5 mb-0 font-weight-bold text-gray-800"> <down_not_touched_data> </div>
                           </div>
                         </div>
                       </div>
                       <div class="col-xl-2 col-md-6 mb-4">
                         <div class="card shadow h-100 py-2">
                           <div class="card-body text-center">
                             <div class="text-xs font-weight-bold text-uppercase mb-1" style="color:#008080;"><b>Closed</b></div>
                             <div class="h5 mb-0 font-weight-bold text-gray-800"> <down_closed_data> </div>
                           </div>
                         </div>
                       </div>
                     </div>
             
                     <!-- Table -->
                     <div class="table-container mt-4">
                       <table class="table table-bordered datatable">
                         <thead class="table-light">
                           <tr>
                             <th>Ticket No</th>
                             <th>Summary</th>
                             <th>Status</th>
                             <th>OpenedAt</th>
                           </tr>
                           <tr>
                             <th><input type="text" placeholder="Search Ticket No"></th>
                             <th><input type="text" placeholder="Search Summary"></th>
                             <th><input type="text" placeholder="Search Status"></th>
                             <th><input type="text" placeholder="Search OpenedAt"></th>
                           </tr>
                         </thead>
                         <tbody>
                           <down_alert_table_body>
                         </tbody>
                       </table>
                     </div>
                   </div>
             
                 </div>
               </div>
             
               <script>
               $(document).ready(function () {
                 // Initialize each DataTable separately when shown
                 function initDataTable(tab) {
                   $(tab).find('.datatable').each(function () {
                     if (!$.fn.dataTable.isDataTable(this)) {
                       let table = $(this).DataTable({
                         pageLength: 10
                       });
             
                       $(this).find('thead tr:eq(1) th').each(function (i) {
                         $('input', this).on('keyup change', function () {
                           if (table.column(i).search() !== this.value) {
                             table.column(i).search(this.value).draw();
                           }
                         });
                       });
                     }
                   });
                 }
             
                 // Initialize first tab
                 initDataTable('#status');
             
                 // Initialize others when opened
                 $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
                   let target = $(e.target).data('bs-target');
                   initDataTable(target);
                 });
               });
               </script>
             </body>
             </html>
             
             
             '''
           html_content=template.replace('<bot_touched_count>',str(analysis_output['Bot touched data']))
           html_content=html_content.replace('<bot_not_touched_count>',str(analysis_output['Bot not touched data']['count']))
           html_content=html_content.replace('<closed>',str(analysis_output['Closed']))
           efficiency=round((analysis_output['Bot touched data']/(analysis_output['Bot touched data']+analysis_output['Bot not touched data']['count']))*100,2)
           html_content=html_content.replace('<efficiency>',str(efficiency)+'%')
           html_content=html_content.replace('<status_alert_touched_data>',str(analysis_output['StatusAlert']['touched_count']))
           html_content=html_content.replace('<status_alert_not_touched_data>',str(analysis_output['StatusAlert']['not_touched_count']))
           html_content=html_content.replace('<status_alert_closed_data>',str(len(analysis_output['StatusAlert']['tickets'])))
           html_content=html_content.replace('<status_alert_table_body>',status_alert_table_body)
           html_content=html_content.replace('<down_touched_data>',str(analysis_output['IdleIntervalAlert']['touched_count']))
           html_content=html_content.replace('<down_not_touched_data>',str(analysis_output['IdleIntervalAlert']['not_touched_count']))
           html_content=html_content.replace('<down_closed_data>',str(len(analysis_output['IdleIntervalAlert']['tickets'])))
           html_content=html_content.replace('<down_alert_table_body>',down_alert_table_body)
           html_content=html_content.replace('<status_alert_closed_data>',str(analysis_output['StatusAlert']['closed']))
           html_content=html_content.replace('<down_closed_data>',str(analysis_output['IdleIntervalAlert']['closed']))
           print("==--"*25)
           print(html_content)
           return {'status': 'success','result': 'Report generated and mail sent successfully'}
        except Exception as e:
            return {'status': 'failed', 'result': str(e)}



