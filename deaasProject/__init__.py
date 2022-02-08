import logging
from .database_op import Database_op
import azure.functions as func
# from .SalesforceUpdate import SalesforceConfig
import json

database_obj = Database_op()
# salesConfig_obj =SalesforceConfig()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # If the request is a GET request, then fetch the data from the database.
        if req.method == "GET":
            data = {'test'}
            # data = database_obj.get_data()
            return func.HttpResponse(f"{data}")
                    
        # If the request is a POST request, then insert the data into the database.
        else: 
            # account_number = req.params.get('accountnumber')
            user_name = req.params.get('user_name')
            project_name=req.params.get('project_name')
            project_desc=req.params.get('project_desc')  #get Username
            
            if (not project_name) and (not project_desc):
                try:
                    req_body = req.get_json()
                except ValueError:
                    pass
                else:
                    project_name=req.params.get('project_name')
                    project_desc=req.params.get('project_desc')

            if project_name and project_desc:
                # msg = database_obj.insert_data(account_number, name)  
                
                user_id=database_obj.get_user_id(user_name) 
                row = project_name,project_desc,user_id
                cols = 'project_name,project_desc,created_by'
                table_name = 'mlaas.project_tbl'
                
                database_obj.insert_records(table_name,row,cols)
                return func.HttpResponse("success")
                # return func.HttpResponse(f"{oportunitydata}")
            else:
                return func.HttpResponse(
                    "Please enter name and quantity in the query string or in the request body.",
                    status_code=200
                )
    
    except Exception as e:
        print(f"{e}")
        return func.HttpResponse(f"{e}")