import logging
from .database_op import Database_op
import azure.functions as func
from .explore import *
import json
import os
from io import StringIO
from urllib.request import urlopen
from unidecode import unidecode

database_obj = Database_op()
explore_obj = ExploreClass() #initialize the JsonFormat Class
# salesConfig_obj =SalesforceConfig()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # If the request is a GET request, then fetch the data from the database.
        if req.method == "GET":
            data = {'test'}
            
                    # Resp_data=json_obj.get_json_format(Resp1_data)
                    # status_code,error_msg=json_obj.get_Status_code(data)                    
               
            # data = database_obj.get_data()
            return func.HttpResponse(data)
                    
        # If the request is a POST request, then insert the data into the database.
        else: 
            # account_number = req.params.get('accountnumber')
            user_name=req.params.get('user_name')  #get Username
            project_name=req.params.get('project_name')
            dataset_name=req.params.get('dataset_name')
            if project_name and dataset_name:
                # msg = database_obj.insert_data(account_number, name)  
                project_id=database_obj.get_project_id(project_name)
                user_id=database_obj.get_user_id(user_name) 
                table_name = 'mlaas.dataset_tbl'
                sql_command = "SELECT p.dataset_file_path,p.file_name FROM "+ table_name + " p WHERE p.dataset_name ='"+ str(dataset_name) +"' and p.project_id ='"+ str(project_id) +"'"
                logging.info("datasetGetClass :"+sql_command)
                data=database_obj.select_records(sql_command)
                if len(data) == 0 or data is None:
                    Resp_data={"No Data"}
                    raise "RecordNotFound"
                else:
                    dataset_file_path=data['dataset_file_path'][0]
                    file_name=data['file_name'][0]
                    upload_file_path = dataset_file_path+"/"+file_name
                    logging.info("upload_file_path :"+upload_file_path)
                    dataset_csv_df=database_obj.read_azure_storage(upload_file_path)
                    # stat_data = explore_obj.get_dataset_statistics(dataset_csv_df)
                    logging.info('stat_data:'+dataset_csv_df)
                    Resp_data = dataset_csv_df.to_json()
                return func.HttpResponse(Resp_data)
    
    except Exception as e:
        logging.error(f"{e}")
        return func.HttpResponse(f"{e}")