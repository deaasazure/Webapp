'''
/*CHANGE HISTORY

--CREATED BY--------CREATION DATE--------VERSION--------PURPOSE----------------------

 ****************************************************************************************/

*/
'''
import json
import logging
import traceback
from database import *
from rest_framework.views import APIView
from rest_framework.response import Response
#from ingest.utils import ingestion
#from ingest.utils.ingestion import *
from .utils.database import db
from .utils.logger_handler import custom_logger as cl
from .utils.json_format.json_formater import *
from .utils.activity_timeline import *
from .utils.activity_timeline import activity_timeline
#from .utils.dynamic_dag import dag_utils


#import pymongo
#import gridfs
#from pymongo import MongoClient
import os
from io import BytesIO

user_name = 'admin'
log_enable = True
LogObject = cl.LogClass(user_name,log_enable)
LogObject.log_setting()
logger = logging.getLogger('common_view')

DBObject=db.DBClass()     #Get DBClass object
connection,connection_string=DBObject.database_connection(database,user,password,host,port) #Create Connection with postgres Database which will return connection object,conection_string(For Data Retrival)
timeline_Obj=activity_timeline.ActivityTimelineClass(database,user,password,host,port) #initialize ActivityTimeline Class
json_obj = JsonFormatClass() #initialize JsonFormat Class
#dag_obj = dag_utils.DagUtilsClass()




'''class TestMongoClass(APIView):
        def post(self,request,format=None):
                
                try:
                        myclient = pymongo.MongoClient('mongodb://mongodb:27017/')
                        db=myclient.grid_file1
                        filename=request.POST.get('filename')
                        file=request.FILES['csvfile']
                        data=file.read()
                        fs=gridfs.GridFS(db)
                        fs.put(data,filename =filename)
                        #Upload completed
                         
                        data=db.fs.files.find_one({'filename':filename})
                        my_id=data['_id']
                        logger.info("ids"+str(my_id))
                        outputdata=fs.get(my_id).read()
                       
                        logger.info("outputdata=="+str(type(outputdata)))
                        logger.info("outputdata=="+str(outputdata))
                        return Response({"status_code":"200","error_msg":"Successfull retrival","response":"Successfull retrival"})  
                except Exception as e:
                        logging.error("Common  : LogFileClass : GET Method : Exception :" + str(e))
                        logging.error("Common  : LogFileClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})
'''
class UserLoginClass(APIView):
        
        def get(self,request,format=None):
                """ this class used to check the authorized user login data.

                Args   :
                        user_name[(String)] : [Name of user]
                        password [(String)] : [password value]
                Return :
                        status_code(500 or 200),
                        error_msg(Error message for login successfull & unsuccessfull),
                        Response(return false if failed otherwise true)
                """
                try:
                        logging.info("Common  : UserLoginClass : GET Method : execution start")
                        user_name = request.query_params.get('user_name') #get user_name
                        password = request.query_params.get('password') #get password
                        logging.info("--->"+str(connection))
                        check_user_auth_tbl=DBObject.is_existing_table(connection,'user_auth_tbl','mlaas') #check user_auth_tbl exists
                        if check_user_auth_tbl == "False":
                                user_df=DBObject.read_data('common/user_registration_tbl.csv') #read user_registration_tbl.csv    
                                status=DBObject.load_df_into_db(connection_string,'user_auth_tbl',user_df,'mlaas')   #creare table user_auth_tbl    
                        check_menu_tbl=DBObject.is_existing_table(connection,'menu_tbl','mlaas')#check menu_tbl exists
                        if check_menu_tbl == "False":
                                menu_df=DBObject.read_data('common/Menu.csv') #read Menu.csv
                                status=DBObject.load_df_into_db(connection_string,'menu_tbl',menu_df,'mlaas') #creare table menu_tbl         
                        check_activity_master_tbl=DBObject.is_existing_table(connection,'activity_master_tbl','mlaas')#check activity_master_tbl exists
                        if check_activity_master_tbl == "False":
                                activity_df=DBObject.read_data('common/activity_master_tbl.csv')#read activity_master_tbl.csv
                                status=DBObject.load_df_into_db(connection_string,'activity_master_tbl',activity_df,'mlaas') #creare table activity_master_tbl         
                        check_parent_activity_tbl=DBObject.is_existing_table(connection,'parent_activity_tbl','mlaas')#check activity_master_tbl exists
                        if check_parent_activity_tbl == "False":
                                parent_activity_df=DBObject.read_data('common/parent_activity_tbl.csv')#read parent_activity_tbl.csv
                                status=DBObject.load_df_into_db(connection_string,'parent_activity_tbl',parent_activity_df,'mlaas') #creare table parent_activity_tbl         
                        check_preprocess_tab_tbl=DBObject.is_existing_table(connection,'preprocess_tab_tbl','mlaas')#check activity_master_tbl exists
                        if check_preprocess_tab_tbl == "False":
                                preprocess_tab_df=DBObject.read_data('common/preprocess_tab_tbl.csv')#read parent_activity_tbl.csv
                                status=DBObject.load_df_into_db(connection_string,'preprocess_tab_tbl',preprocess_tab_df,'mlaas') #creare table parent_activity_tbl         
                        user_status = DBObject.user_authentication(connection,user_name,password) #check the user user authenticated or not
                        if user_status != True:
                                status_code,error_msg=json_obj.get_Status_code(user_status)
                                logging.info("Common  : UserLoginClass : GET Method : execution : status_code :"+ status_code)
                                return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"})
                        else: 
                                status = DBObject.create_score_view(connection)
                                logging.info("Common  : UserLoginClass : POST Method : execution stop : status_code : 200 : "+str(status))
                                return Response({"status_code":"200","error_msg":"Login Successfull","response":"true"})
                except Exception as e:
                        logging.error("Common  : UserLoginClass : GET Method : Exception :" + str(e))
                        logging.error("Common  : UserLoginClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})
        
        def post(self,request):
                """ this function used to insert user data into table.

                Args   :
                        csv_file[(CSV)] : [CSV data of authorized user]
                Return :

                        Response(return 1 if failed otherwise 0)
                """
                try:
                        logging.info("Common  : UserLoginClass : POST Method : execution start")
                        
                        user_df=DBObject.read_data('common/user_registration_tbl.csv') #read the data from csv file store into dataframe variable
                        logging.info("get data frame from read data=="+str(user_df))
                        status=DBObject.load_df_into_db(connection_string,'user_auth_tbl',user_df,'mlaas') # this function will insert the csv data into  user_auth table
                        return Response({"Status":status})
                except Exception as e:
                        logging.error("Common  : UserLoginClass : POST Method : Exception :" + str(e))
                        logging.error("Common  : UserLoginClass : POST Method : " +traceback.format_exc())
                        return Response({"Exception":str(e)}) 
class PlayerProfileClass(APIView):
        
        def get(self,request,format=None):
                """ this class used to check the authorized user login data.

                Args   :
                        user_name[(String)] : [Name of user]
                        password [(String)] : [password value]
                Return :
                        status_code(500 or 200),
                        error_msg(Error message for login successfull & unsuccessfull),
                        Response(return false if failed otherwise true)
                """
                try:
                        logging.info("Common  : UserLoginClass : GET Method : execution start")
                        user_name = request.query_params.get('user_name') #get user_name
                        password = request.query_params.get('password') #get password
                        email = request.query_params.get('email') #get email
                        name = request.query_params.get('name') #get name
                        type = request.query_params.get('type') #get type
                        category = request.query_params.get('category') #get email
                        role = request.query_params.get('role') #get name
                        dob = request.query_params.get('dob') #get type
                        team_name = request.query_params.get('team_name') #get type
                        founded_since= request.query_params.get('founded_since')
                        profile_pict_path = request.query_params.get('profile_pict_path')
                        created_on = request.query_params.get('created_on')
                        created_by = request.query_params.get('created_by')
                        
                        logging.info("--->"+str(connection))
                        check_user_auth_tbl=DBObject.is_existing_table(connection,'user_profile_tbl','mlaas') #check user_auth_tbl exists
                        if check_user_auth_tbl == "False":
                                user_df=DBObject.read_data('common/user_registration_tbl.csv') #read user_registration_tbl.csv    
                                status=DBObject.load_df_into_db(connection_string,'user_auth_tbl',user_df,'mlaas')   #creare table user_auth_tbl    
                        check_menu_tbl=DBObject.is_existing_table(connection,'menu_tbl','mlaas')#check menu_tbl exists
                        if check_menu_tbl == "False":
                                menu_df=DBObject.read_data('common/Menu.csv') #read Menu.csv
                                status=DBObject.load_df_into_db(connection_string,'menu_tbl',menu_df,'mlaas') #creare table menu_tbl         
                        check_activity_master_tbl=DBObject.is_existing_table(connection,'activity_master_tbl','mlaas')#check activity_master_tbl exists
                        if check_activity_master_tbl == "False":
                                activity_df=DBObject.read_data('common/activity_master_tbl.csv')#read activity_master_tbl.csv
                                status=DBObject.load_df_into_db(connection_string,'activity_master_tbl',activity_df,'mlaas') #creare table activity_master_tbl         
                        check_parent_activity_tbl=DBObject.is_existing_table(connection,'parent_activity_tbl','mlaas')#check activity_master_tbl exists
                        if check_parent_activity_tbl == "False":
                                parent_activity_df=DBObject.read_data('common/parent_activity_tbl.csv')#read parent_activity_tbl.csv
                                status=DBObject.load_df_into_db(connection_string,'parent_activity_tbl',parent_activity_df,'mlaas') #creare table parent_activity_tbl         
                        check_preprocess_tab_tbl=DBObject.is_existing_table(connection,'preprocess_tab_tbl','mlaas')#check activity_master_tbl exists
                        if check_preprocess_tab_tbl == "False":
                                preprocess_tab_df=DBObject.read_data('common/preprocess_tab_tbl.csv')#read parent_activity_tbl.csv
                                status=DBObject.load_df_into_db(connection_string,'preprocess_tab_tbl',preprocess_tab_df,'mlaas') #creare table parent_activity_tbl         
                        user_status = DBObject.user_authentication(connection,user_name,password) #check the user user authenticated or not
                        if user_status != True:
                                status_code,error_msg=json_obj.get_Status_code(user_status)
                                logging.info("Common  : UserLoginClass : GET Method : execution : status_code :"+ status_code)
                                return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"})
                        else: 
                                status = DBObject.create_score_view(connection)
                                logging.info("Common  : UserLoginClass : POST Method : execution stop : status_code : 200 : "+str(status))
                                return Response({"status_code":"200","error_msg":"Login Successfull","response":"true"})
                except Exception as e:
                        logging.error("Common  : UserLoginClass : GET Method : Exception :" + str(e))
                        logging.error("Common  : UserLoginClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})
        
        def post(self,request):
                """ this function used to insert user data into table.

                Args   :
                        csv_file[(CSV)] : [CSV data of authorized user]
                Return :

                        Response(return 1 if failed otherwise 0)
                """
                try:
                        logging.info("Common  : UserLoginClass : POST Method : execution start")
                        
                        user_df=DBObject.read_data('common/user_registration_tbl.csv') #read the data from csv file store into dataframe variable
                        logging.info("get data frame from read data=="+str(user_df))
                        status=DBObject.load_df_into_db(connection_string,'user_auth_tbl',user_df,'mlaas') # this function will insert the csv data into  user_auth table
                        return Response({"Status":status})
                except Exception as e:
                        logging.error("Common  : UserLoginClass : POST Method : Exception :" + str(e))
                        logging.error("Common  : UserLoginClass : POST Method : " +traceback.format_exc())
                        return Response({"Exception":str(e)}) 

class MenuClass(APIView):
        def post(self, request, format=None):
                """
                this function used to insert  nevigation Menu detail into database. 
                Args:
                       [This function does not take any argument] 
                Return:
                        status_code(500 or 200),
                        error_msg(Error message for Insertion successfull or unsuccessfull),
                        Response(return false if failed otherwise true )  
                """
                try:
                        logging.info("Common  : MenuClass : POST Method : execution start")
                        menu_df=DBObject.read_data('common/Menu.csv')
                        DBObject.create_schema(connection)
                        status=DBObject.load_df_into_db(connection_string,'menu_tbl',menu_df,'mlaas')
                        if status != 0:
                                logging.info("Common  : MenuClass : POST Method : execution stop : status_code :500")
                                return Response({"status_code":"500","error_msg":"Insertion Failed","response":"false"})
                        else:
                                logging.info("Common  : MenuClass : POST Method : execution stop : status_code : 200")
                                return Response({"status_code":"200","error_msg":"Insertion successfull","response":"true"})
                except Exception as e:
                        logging.error("Common  : MenuClass : GET Method : Exception :" + str(e))
                        logging.error("Common  : MenuClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":"Failed","response":str(e)}) 
        
        def get(self, request, format=None):
                """
                this function used to get Navigation menu data from the database and convert into appropriate json format.
                Args:
                       [This function does not take any argument] 
                Return:
                        status_code(500 or 200),
                        error_msg(Error message for retrive successfull or unsuccessfull),
                        Response(return error_msg if failed otherwise Json data )  
                """
                try:
                        logging.info("Common  : MenuClass : POST Method : execution start")
                        sql_command1='select id,modulename,menuname as "label",url as "link",parent_id as "parentId",icon from mlaas.menu_tbl where parent_id is null'
                        
                        dataset_df1=DBObject.select_records(connection,sql_command1) #call show_data_details and it will return dataset detail data in dataframe
                        
                        dataset_json1=json.loads(dataset_df1.to_json(orient='records'))  # convert datafreame into json
                        
                        sql_command2='select id,modulename,menuname as "label",url as "link",parent_id as "parentId",icon from mlaas.menu_tbl where parent_id is not null'
                        
                        dataset_df2=DBObject.select_records(connection,sql_command2) #call show_data_details and it will return dataset detail data in dataframe
                        
                        dataset_json2=json.loads(dataset_df2.to_json(orient='records'))  # convert datafreame into json

                        json_data=json_obj.menu_nested_format(dataset_json1,dataset_json2)   
                        return Response({"status_code":"200","error_msg":"Menu Data","response":json_data})
                except Exception as e:
                                logging.error("Common  : MenuClass : POST Method : Exception :" + str(e))
                                logging.error("Common  : MenuClass : POST Method : "+ traceback.format_exc())
                                return Response({"status_code":"500","error_msg":"Failed","response":str(e)})


class ActivityTimelineClass(APIView):
        
        def post(self,request,formate=None):
                """
                This class will create schema  of master activity table.
                It will take url string as mlaas/activity_timeline/.

                Args  : 
                        None
                        
                Return : 
                        status_code(500 or 200),
                        error_msg(Error message for inserstion failed or successfull),
                        Response(return false if failed otherwise schema will create with msg)
                """
                try:
                        logging.info("Common  : ActivityTimeLine : POST Method : execution start")
                        activity_df=DBObject.read_data('common/activity_master_tbl.csv')
                        status=DBObject.load_df_into_db(connection_string,'activity_master_tbl',activity_df,'mlaas')
                        if status != 0:
                                logging.info("Common  : ActivityTimeLine : POST Method : execution stops: status_code :500")
                                return Response({"status_code":"500","error_msg":"Insertion Failed","response":"false"})
                        else:
                                logging.info("Common  : ActivityTimeLine : POST Method : execution stop : status_code : 200")
                                return Response({"status_code":"200","error_msg":"Insertion successfull","response":"true"})
                except Exception as e:
                        logging.error("Common  : ActivityTimeLine : GET Method : Exception :" + str(e))
                        logging.error("Common  : ActivityTimeLine : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":"Failed","response":str(e)}) 
        
        def get(self,request,format=None):
                """
                This class is used to show the user activity for each of single user.
                It will take url string as mlaas/activity_timeline/.

                Args  : 
                        user_name[(String)]   :[User Name]
                        
                Return : 
                        status_code(500 or 200),
                        error_msg(Error message for retrival failed or successfull),
                        Response(return false if failed otherwise json data)
                """
             
                try:
                        logging.info("Common  : ActivityTimelineClass : GET Method : execution start")
                        user_name = request.query_params.get('user_name')
                        activity_df = timeline_Obj.get_user_activity(user_name)

                        if isinstance(activity_df,str): #check the instance of activity_df
                                status_code,error_msg=json_obj.get_Status_code(activity_df) # extract the status_code and error_msg from activity_df
                                logging.info("Common  : ActivityTimelineClass : GET Method : execution : status_code :"+ status_code)
                                return Response({"status_code":status_code,"error_msg":error_msg,"response":"false"})
                
                        else:
                        
                              return Response({"status_code":"200","error_msg":"Successfull retrival","response":activity_df})  
                except Exception as e:
                        logging.error("Common  : ActivityTimelineClass : GET Method : Exception :" + str(e))
                        logging.error("Common  : ActivityTimelineClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})

class LogFileClass(APIView):
        def get(self,request,format=None):
                """
                This class is used read the text of the admin_debug log file.
                It will take url string as mlaas/common/logfile/.

                Args  : 
                        user_name[(String)]   :[User Name]
                        
                Return : 
                        status_code(500 or 200),
                        error_msg(Error message for retrival failed or successfull),
                        Response(return false if failed otherwise json data)
                """
             
                try:
                        with open('./logs/admin_debug.log','r') as file:
                                log_string = file.read()


                        return Response({"status_code":"200","error_msg":"Successfull retrival","response":str(log_string)})  
                except Exception as e:
                        logging.error("Common  : LogFileClass : GET Method : Exception :" + str(e))
                        logging.error("Common  : LogFileClass : GET Method : " +traceback.format_exc())
                        return Response({"status_code":"500","error_msg":str(e),"response":"false"})





